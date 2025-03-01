import discord
import os
import ssl
import certifi
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View
import aiohttp
import re
import asyncio # Import asyncio for sleep
from model import use_deepseek_api

# Custom SSL context setup
ssl_context = ssl.create_default_context(cafile=certifi.where())  # Set custom SSL context with certificates
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
# Load environment variables
load_dotenv()
# Initialize some global variables
level = 1
with open('cusswords.txt') as f:
    bad_words = f.read().splitlines()
user_message_count = {}
user_emojis = {}  # Store emojis sent by each user in a list
bad_words_list = {}
user_messages = {} # Changed messages_list to user_messages
# Custom View with buttons
class MyView(View):
    def _init_(self):
        super()._init_()
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
                                                "stat showemojis - Show the emojis you've sent\n"
                                                "stat show\n"
                                                "stat send_msgs - Get your message history sent to your DMs") # Added send_msgs to command list
# Define the custom bot behavior
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    channel = bot.get_channel(1286194781168603177)  # Replace with your actual channel ID
    embed = discord.Embed(title="Welcome", description="Hello World!", color=0x00ff00)
    view = MyView()  # Create the view with buttons
    await channel.send(embed=embed, view=view)

    # --- Send Test DM to all Members on Bot Ready ---
    print("Starting to send test DMs to all members...")
    guild = bot.guilds[0] # Assuming bot is in at least one server, get the first one. You might need to adjust if bot is in multiple servers.
    members = guild.members
    sent_dm_count = 0
    failed_dm_count = 0

    for member in members:
        if member.bot: # Skip bots
            continue

        try:
            dm_channel = member.dm_channel
            if dm_channel is None:
                dm_channel = await member.create_dm()

            test_message_content = "Hello! This is a test DM sent to all server members when the bot starts up.  If you received this, it means the bot is functioning correctly and can send DMs. You can ignore this message. - Bot Team"
            await dm_channel.send(test_message_content)
            print(f"Test DM sent to: {member.name}#{member.discriminator}")
            sent_dm_count += 1
            await asyncio.sleep(1) # Add a small delay to avoid rate limits (adjust as needed)

        except discord.errors.Forbidden:
            print(f"Could not send DM to: {member.name}#{member.discriminator} (DMs likely disabled or user blocked bot)")
            failed_dm_count += 1
        except Exception as e:
            print(f"Error sending DM to {member.name}#{member.discriminator}: {e}")
            failed_dm_count += 1

    print(f"Test DM sending to all members COMPLETED.")
    print(f"Total DMs sent successfully: {sent_dm_count}")
    print(f"Total DMs failed: {failed_dm_count}")
    # --- End of Test DM Sending ---


# Function to extract emojis from a message
def extract_emojis(message_content):
    # Regex to capture both unicode emojis and custom emojis (e.g., <:emoji:ID>)
    emoji_pattern = re.compile(r'(<:.*?:\d+>|[\U00010000-\U0010ffff])')
    return emoji_pattern.findall(message_content)
# Handle commands and custom messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # --- Message Storage Logic (Add this right after "if message.author == bot.user: return") ---
    user_id = message.author.id
    message_content = message.content

    if user_id not in user_messages:
        user_messages[user_id] = [] # Initialize an empty list for the user if not already there

    user_messages[user_id].append(message_content) # Append the message content to the user's list

    print(user_messages) # Optional: Print the user_messages dictionary to console for debugging


    emojis = extract_emojis(message.content)

    if emojis:
        if message.author.id not in user_emojis:
            user_emojis[message.author.id] = []
        user_emojis[message.author.id].extend(emojis)

    if len(message.content) > 5:
        if message.author.id not in user_message_count:
            user_message_count[message.author.id] = 0
        user_message_count[message.author.id] += 1

        if user_message_count[message.author.id] >= 5:
            global level
            level += 1
            await message.channel.send(f'You have leveled up! You are now on level {level}')
            user_message_count[message.author.id] = 0

    if message.content.lower() == 'stat levelcheck':
        await message.channel.send(f'You are on level {level}')

    if message.content.lower() == 'stat improve':
        await message.channel.send('I am a bot that can help you improve your messages!')

    if message.content.lower() == 'stat showemojis':
        user_emoji_list = user_emojis.get(message.author.id, [])
        if user_emoji_list:
            emoji_str = ', '.join(user_emoji_list)
            await message.channel.send(f"{message.author.name} has sent these emojis: {emoji_str}")
        else:
            await message.channel.send(f"{message.author.name} hasn't sent any emojis yet.")

    if message.content.lower() == 'stat levelup':
        messages_needed = 5 - user_message_count.get(message.author.id, 0)
        await message.channel.send(f'You need {messages_needed} more messages to level up')

    if message.content.lower() == 'stat showallemojis':
        if len(user_emojis) >= 2:
            for user_id, emojis in user_emojis.items():
                user = bot.get_user(user_id)
                if user:
                    emoji_str = ', '.join(emojis)
                    await message.channel.send(f"{user.name} sent these emojis: {emoji_str}")
                else:
                    await message.channel.send(f"Could not find user with ID: {user_id}")
        else:
            await message.channel.send("There are fewer than 2 users who have sent emojis.")

    if message.content.lower() == 'stat showcuss':
        user_cuss_words = bad_words_list.get(message.author.id)
        if user_cuss_words:
            cuss_string = ", ".join(user_cuss_words)
            await message.channel.send(f"{message.author.name} has used these cuss words: {cuss_string}")
        else:
            await message.channel.send(f"{message.author.name} has not used any cuss words.")
    
    user = message.author
    user_id = user.id
    dm_channel = user.dm_channel
    
    if dm_channel is None:
        dm_channel = await user.create_dm()
    
    print(f"Received command: {message.content.lower()} from {user.name}")

    if message.content.lower() == 'stat eval_msgs':
        messages_list = user_messages.get(user_id, [])
        print(f"Evaluating messages for {user.name}: {messages_list}")  # Debug log
        
        response = use_deepseek_api("messages_eval", "C", messages_list)
        await dm_channel.send(response)

    elif message.content.lower() == 'stat improve_msg':
        user_message = message.content
        messages_list = user_messages.get(user_id, [])
        
        print(f"Improving message for {user.name}: {user_message}")  # Debug log
        
        response = use_deepseek_api("improve_message", user_message, messages_list)
        await dm_channel.send(response)

    elif message.content.lower() == 'stat msgstats':
        messages_list = user_messages.get(user_id, [])
        
        print(f"Getting message stats for {user.name}: {messages_list}")  # Debug log
        
        response = use_deepseek_api("messages_eval_level", "C", messages_list)
        await dm_channel.send(response)


    if message.content.lower() == 'stat sendmsgs':
        """Sends the user their message history via DM."""
        print("send_msgs command START")  # Debug print to see if the command is even being triggered

        user = message.author
        user_id = user.id
        messages_list = user_messages.get(user_id, [])  # Get the user's message list

        print(f"Messages List retrieved: {messages_list}")  # Debug print to check if messages_list is being populated

        if not messages_list:
            await message.channel.send(f"{user.mention}, you haven't sent any messages yet, or your message history is empty.")
            print("No messages to send, command END")  # Debug print for this condition
            return

        message_str = "\n".join(messages_list)  # Format messages into a single string

        dm_channel = user.dm_channel
        if dm_channel is None:
            dm_channel = await user.create_dm()
            print("DM channel created (or retrieved)")  # Debug print

        if dm_channel is None:  # Double check if DM channel is still None after creation attempt - CRITICAL DEBUG CHECK
            print("ERROR: DM channel is STILL None after creation/retrieval!")
            await message.channel.send(f"{user.mention}, Sorry, I couldn't establish a DM channel with you. Something is wrong on my end.")
            print("Command END due to DM Channel failure")
            return  # STOP if DM channel is still None

        print(f"DM Channel object: {dm_channel}")  # Print the DM Channel OBJECT to console - Inspect it. Is it valid?

        print("Attempting to send DM...")
        try:
            # Split messages if they are too long for a single DM
            message_parts = split_message(message_str)  # Define this function below

            for part in message_parts:
                print(f"Sending DM part: {part[:50]}...")  # Print the first 50 chars of each part to see if it's trying to send
                send_result = await dm_channel.send(part)  # Capture the send result - crucial for debugging!
                print(f"DM send attempt result: {send_result}")  # Print the result of the send operation - what is Discord returning?
                if send_result:
                    print(f"DM part sent successfully. Message ID: {send_result.id}")  # If successful, log the message ID
                else:
                    print("WARNING: DM send returned None/False but no exception!")  # Strange case, log a warning

            await message.channel.send(f"{user.mention}, I've sent your message history to your DMs!")
            print("DM sending SUCCESS, command END")  # Debug print for success

        except discord.errors.Forbidden as forbidden_error:  # Capture the Forbidden Error Specifically with a variable name
            await message.channel.send(f"{user.mention}, I couldn't DM you your message history. Please check your DM privacy settings.")
            print(f"DM Forbidden error, command END. Error details: {forbidden_error}")  # Print error details
        except Exception as e:
            print(f"Exception during DM sending: {e}")
            await message.channel.send(f"{user.mention}, an error occurred while trying to DM you. Check bot logs.")
            print("DM sending ERROR, command END")  # Debug print for general error

        print("send_msgs command FUNCTION END REACHED")

    for word in bad_words:
        if word in message.content.lower():
            await message.channel.send("Level lowered by 1 for using a potty word!")
            if level > 0:
                level -= 1
                # Initialize the list if it doesn't exist for this user
                if message.author.id not in bad_words_list:
                    bad_words_list[message.author.id] = []
                bad_words_list[message.author.id].append(word)
                print(bad_words_list)
            else:
                return
            break

    await bot.process_commands(message)


def split_message(long_message, max_len=2000):
    """Splits a long message into parts that fit within Discord's character limit."""
    parts = []
    current_part = ""
    for line in long_message.splitlines(keepends=True):  # Split by lines and keep newline chars
        if len(current_part) + len(line) <= max_len:
            current_part += line
        else:
            parts.append(current_part)
            current_part = line  # Start new part with the line that didn't fit
    if current_part:  # Append any remaining part
        parts.append(current_part)
    return parts

# Override the default aiohttp session with custom SSL context
async def run_bot():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl_context=ssl_context)) as session:
        bot._session = session  # Attach the session to the bot
        token = os.getenv('DISCORD_BOT_TOKEN')
        await bot.start(token)
# Start the bot with custom session
import asyncio
asyncio.run(run_bot())