import discord
from discord.ext import commands
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configuration
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Utilisation d'un modèle très stable
model = genai.GenerativeModel('gemini-1.5-flash')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# REMPLACE PAR TON ID DE SALON RÉEL
ALLOWED_CHANNEL_ID = 1520444442631208971 

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.event
async def on_message(message):
    # 1. Sécurité : ne jamais répondre à soi-même
    if message.author == bot.user:
        return

    # 2. Restriction : on ne traite que le salon autorisé
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    # 3. Traitement
    try:
        async with message.channel.typing():
            # On envoie uniquement le texte du message pour éviter les erreurs de format
            response = model.generate_content(message.clean_content)
            await message.channel.send(response.text)
    except Exception as e:
        print(f"Erreur : {e}")
        # On évite d'envoyer des messages trop longs ou complexes en cas d'erreur
        await message.channel.send("Erreur de connexion au modèle.")

bot.run(os.getenv('DISCORD_TOKEN'))
