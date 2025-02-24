import discord
import os
import ssl
import certifi
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View
import aiohttp
import re

# Custom SSL context setup
ssl_context = ssl.create_default_context(cafile=certifi.where())  # Set custom SSL context with certificates

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
# Load environment variables
load_dotenv()

# Initialize some global variables
level = 1
user_message_count = {}
def load_words_from_file(filename):
    with open(filename, "r") as file:
        return [line.strip().lower() for line in file]

bad_words = load_words_from_file("cusswords.txt")

# Custom View with buttons
class MyView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Click me for a full list of commands!", style=discord.ButtonStyle.primary, custom_id="button")
    async def button_callback(self, interaction: discord.Interaction, button: Button):
        # Respond to the first button
        print("clicked")
        await interaction.response.send_message("Here is a list of commands you can use:\n"
                                                "stat levelcheck - Check your current level\n"
                                                "stat improve - Get feedback on your message and get a more refined version of it\n"
                                                "stat levelup - Check how many messages you need to level up\n"
                                                "stat eval_msgs - Evaluate a user's message history\n"
                                                "stat improve_msg - Get feedback on your message and a refined version of it\n"
                                                "stat msgstats - Check your message history stats\n"
                                                "stat level - Check your current level\n"
                                                "stat levelreset - Reset your level to 1\n"
                                                "stat cusswords - Check the number of cuss words you have used\n")
        
    

# Define the custom Discord client
class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(1286194781168603177)  # Replace with your actual channel ID
        embed = discord.Embed(title="Welcome", description="Hello World!", color=0x00ff00)
        view = MyView()  # Create the view with buttons
        await channel.send(embed=embed, view=view)

    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return
        print()
        # Track user messages if they are over 5 characters
        if len(message.content) > 5:
            if message.author.id not in user_message_count:
                user_message_count[message.author.id] = 0
            user_message_count[message.author.id] += 1

            # Check if user has sent 5 messages
            if user_message_count[message.author.id] >= 5:
                global level
                level += 1
                await message.channel.send(f'You have leveled up! You are now on level {level}')
                user_message_count[message.author.id] = 0  # Reset the count after leveling up

        if message.content.lower() == 'stat levelcheck':
            await message.channel.send(f'You are on level {level}')
            print('levelcheck')
        if message.content.lower() == 'stat improve':
            await message.channel.send('I am a bot that can help you improve your messages!')
        #checks for cuss words and lowers
            
# Override the default aiohttp session with custom SSL context
async def run_bot():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl_context=ssl_context)) as session:
        client = Client(intents=discord.Intents.default(), loop=session._loop)
        token = os.getenv('DISCORD_BOT_TOKEN')
        await client.start(token)
        for word in bad_words:
            if word in message.content.lower():
                await message.channel.send("Level lowered by 1 for using a potty word!")
                level -= 1
                break
# Start the bot with custom session
import asyncio
asyncio.run(run_bot())
