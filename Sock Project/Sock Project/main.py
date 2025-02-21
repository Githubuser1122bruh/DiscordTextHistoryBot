import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View

load_dotenv()
level = 1
user_message_count = {}

class MyView(View):
    @discord.ui.button(label="Click me for a full list of commands!", style=discord.ButtonStyle.secondary)
    async def button_callback(self, button: Button, interaction: discord.Interaction):
        # This line should correctly respond to the interaction, not the button
        @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, custom_id="my_button")
        async def my_button_callback(self, button, interaction):
            await interaction.response.send_message("Here is a list of commands you can use:\n"
                                            "stat levelcheck - Check your current level\n"   
                                            "stat levelup - Check how many messages you need to level up\n"
                                            "stat level - Check your current level\n"
                                            "stat levelreset - Reset your level to 1\n")

class Client(discord.Client):
    async def on_ready(self):
        print(f'logged on as {self.user}!')
        channel = self.get_channel(1286194781168603177)
        embed = discord.Embed(title="Welcome", description="Hello World!", color=0x00ff00)
        view = MyView()
        await channel.send(embed=embed, view=view)

    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return

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

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
