import discord
from discord.ext import commands
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Charge les variables d'environnement (token et clé API)
load_dotenv()

# Configuration des clés
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configuration de Gemini
genai.configure(api_key=GEMINI_API_KEY)
# Utilise ceci pour le modèle Gemini 3.5 Flash
model = genai.GenerativeModel('Gemini 3.1 Flash-Lite')
# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- ID DU SALON AUTORISÉ ---
# Remplace ce chiffre par l'ID que tu as copié lors de l'étape 3
ALLOWED_CHANNEL_ID = 1520444442631208971 

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Affiche l'ID dans les logs pour être sûr qu'on est au bon endroit
    print(f"Message reçu dans salon ID: {message.channel.id}, Attendu: {ALLOWED_CHANNEL_ID}")

    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    try:
        async with message.channel.typing():
            response = model.generate_content(message.content)
            await message.channel.send(response.text)
    except Exception as e:
        # Affiche l'erreur réelle dans les logs Render
        print(f"Erreur détaillée : {e}")
        await message.channel.send(f"Erreur technique : {str(e)}")
# Lancement du bot
bot.run(DISCORD_TOKEN)
