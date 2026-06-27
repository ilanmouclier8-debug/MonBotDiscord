import discord
from discord.ext import commands
import os
from google import genai  # Import du nouveau SDK
from dotenv import load_dotenv

load_dotenv()

# Initialisation avec la clé API
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_CHANNEL_ID = 1520444442631208971 # Remplace par ton ID

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id != ALLOWED_CHANNEL_ID:
        return

    # Remplace ton bloc try/except actuel par celui-ci
    try:
        async with message.channel.typing():
            # Utilisation du client avec le modèle de ta liste
            response = client.models.generate_content(
                model="gemini-1.5-flash", # Utilisons celui-ci qui est très stable
                contents=message.clean_content,
            )
            await message.channel.send(response.text)
    except Exception as e:
        # Affiche l'erreur complète dans les logs Render
        print(f"ERREUR TECHNIQUE RÉELLE : {e}") 
        await message.channel.send(f"Erreur : {e}")

bot.run(os.getenv('DISCORD_TOKEN'))
