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
            # On précise bien le nom complet du modèle
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=message.clean_content,
            )
            await message.channel.send(response.text)
    except Exception as e:
        # Ajoute ce print pour voir l'erreur réelle dans les logs Render
        print(f"ERREUR DÉTAILLÉE : {e}") 
        await message.channel.send("Erreur de connexion au modèle.")

bot.run(os.getenv('DISCORD_TOKEN'))
