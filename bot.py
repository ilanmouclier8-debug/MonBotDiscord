import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import google.generativeai as genai
import PIL.Image # Nécessaire pour traiter les images
import requests # Nécessaire pour télécharger l'image depuis Discord
from io import BytesIO # Pour gérer l'image en mémoire

load_dotenv()

# Configuration IA
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# Note : 'gemini-3.5-flash' est excellent pour analyser les images rapidement
model = genai.GenerativeModel(
    model_name='models/gemini-3.5-flash',
    system_instruction="Tu es Eclipse Studio, un assistant Discord intelligent. Tu réponds toujours en français. Tu es capable d'analyser des images de manière détaillée."
)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# REMPLACE PAR TON ID (SANS GUILLEMETS)
SALON_IA_ID = 1520422861318127777 

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    # ... message d'intro ...

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Debug : affiche le texte reçu dans le terminal
    print(f"Message détecté dans salon {message.channel.id} : {message.content}")

    # --- NOUVEAU LOGIQUE : ANALYSE D'IMAGES ---
    if message.channel.id == SALON_IA_ID:
        # 1. Vérifier si on mentionne le bot (ou le rôle, comme avant)
        if bot.user.mentioned_in(message) or len(message.role_mentions) > 0:
            
            # Nettoyage du texte (texte d'explication de l'image)
            question_texte = message.content
            for mention in message.mentions + message.role_mentions:
                question_texte = question_texte.replace(f'<@{mention.id}>', '').replace(f'<@&{mention.id}>', '').replace(f'<@!{mention.id}>', '')
            question_texte = question_texte.strip() or "Peux-tu m'expliquer ce que tu vois dans cette image ?"

            # 2. Vérifier s'il y a une pièce jointe (une image)
            # On prend la première (message.attachments[0])
            if len(message.attachments) > 0 and message.attachments[0].content_type.startswith('image/'):
                attachment = message.attachments[0]
                
                # Message temporaire pour faire patienter (le téléchargement prend du temps)
                status_message = await message.reply("⏳ *Analyse de l'image en cours...*")
                
                try:
                    # Étape cruciale : télécharger l'image depuis Discord
                    # On le fait en "streaming" pour ne pas bloquer le bot
                    response = requests.get(attachment.url, stream=True)
                    response.raise_for_status() # Vérifie si le téléchargement a réussi
                    
                    # Convertir les données brutes en une image PIL
                    img_data = BytesIO(response.content)
                    pil_image = PIL.Image.open(img_data)
                    
                    async with message.channel.typing():
                        # Étape 3 : Envoyer l'image ET le texte à Gemini pour analyse
                        # C'est cette ligne magique qui active la vision
                        ia_response = model.generate_content([question_texte, pil_image])
                        
                        # Remplacer le message de statut par la vraie réponse
                        await status_message.edit(content=ia_response.text)
                        
                except Exception as e:
                    print(f"Erreur Vision : {e}")
                    await status_message.edit(content="Oups, je n'ai pas pu analyser cette image. Problème technique.")
            
            # 4. Si c'est juste du texte (pas de pièce jointe)
            else:
                try:
                    async with message.channel.typing():
                        # Mode texte uniquement
                        ia_response = model.generate_content(question_texte)
                        await message.reply(ia_response.text)
                except Exception as e:
                    print(f"Erreur Texte : {e}")
                    await message.reply("Oups, j'ai eu un bug.")

    await bot.process_commands(message)

# Lancer le bot
bot.run(os.getenv('DISCORD_TOKEN'))