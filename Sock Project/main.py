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
user_emojis = {}  # Store emojis sent by each user in a list


    

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
                                                "stat levelreset - Reset your level to 1\n")


# Define the custom bot behavior
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    channel = bot.get_channel(1286194781168603177)  # Replace with your actual channel ID
    embed = discord.Embed(title="Welcome", description="Hello World!", color=0x00ff00)
    view = MyView()  # Create the view with buttons
    await channel.send(embed=embed, view=view)


# Function to extract emojis from a message
def extract_emojis(message_content):
    # Regex to capture both unicode emojis and custom emojis (e.g., <:emoji:ID>)
    emoji_pattern = re.compile(r'(<:.*?:\d+>|[\U00010000-\U0010ffff])')
    return emoji_pattern.findall(message_content)


# Handle commands and custom messages
@bot.event
async def on_message(message):
    # Don't let the bot respond to its own messages
    if message.author == bot.user:
        return

    # Extract emojis from the message
    emojis = extract_emojis(message.content)

    # Store the emojis in a list for each user
    if emojis:
        if message.author.id not in user_emojis:
            user_emojis[message.author.id] = []
        user_emojis[message.author.id].extend(emojis)  # Add new emojis to the user's list

    # Handle custom messages manually (non-command)
    if len(message.content) > 5:
        if message.author.id not in user_message_count:
            user_message_count[message.author.id] = 0
        user_message_count[message.author.id] += 1

        # Check if the user has sent 5 messages
        if user_message_count[message.author.id] >= 5:
            global level
            level += 1
            await message.channel.send(f'You have leveled up! You are now on level {level}')
            user_message_count[message.author.id] = 0  # Reset the count after leveling up

    # Process commands
    if message.content.lower() == 'stat levelcheck':
        await message.channel.send(f'You are on level {level}')

    if message.content.lower() == 'stat improve':
        await message.channel.send('I am a bot that can help you improve your messages!')

    # Example: Print the emojis sent by the user in a list format
    if message.content.lower() == 'stat showemojis':
        user_emoji_list = user_emojis.get(message.author.id, [])
        if user_emoji_list:
            emoji_str = ', '.join(user_emoji_list)  # Join the emojis in a comma-separated string
            await message.channel.send(f"{message.author.name} has sent these emojis: {emoji_str}")
        else:
            await message.channel.send(f"{message.author.name} hasn't sent any emojis yet.")

    # Call the commands extension's on_message so that commands are processed
    await bot.process_commands(message)
    print (user_emojis)

# Override the default aiohttp session with custom SSL context
async def run_bot():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl_context=ssl_context)) as session:
        bot._session = session  # Attach the session to the bot
        token = os.getenv('DISCORD_BOT_TOKEN')
        await bot.start(token)


# Start the bot with custom session
import asyncio
asyncio.run(run_bot())
