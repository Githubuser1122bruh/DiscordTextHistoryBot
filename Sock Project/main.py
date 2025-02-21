#IMport statements
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View

load_dotenv()
level = 1
user_message_count = {}
def use_deepseek_api(type_of_data, data):
    #This function uses the deepseek API that is provided by hack club to do all the actual work. Thanks, hack club!
    url = "https://ai.hackclub.com/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    if type_of_data =="messages_eval":
        data = data + "based on this messaging history, critique the user's messages and suggest improvements. Make sure to stay positive and constructive, but don't be afraid to be honest. Here are some examples of things you could critique: tone, use of insults/cuss words, use of emojis, helpfulness, etc."
    
    elif type_of_data == "messages_eval_level":
        data = data + "based on this messaging history, critique the user's messages and suggest improvements. Make sure to stay positive and constructive, but don't be afraid to be honest. Here are some examples of things you could critique: tone, use of insults/cuss words, use of emojis, helpfulness, etc. Make this level out of 10, 1 being like an internet troll messaging at 12:00 in the night and 10 being J.K Rowling"
    
    elif type_of_data == "improve_message":
        data = data + "Critique this message, but based on past history, explain what the user did better or worse. Also, provide a refined message in it's place."
    data = {"messages":[{"role":"user", "content":data}]}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    json_response = response.json()

class MyView(View):
    @discord.ui.button(label="Click me for a full list of commands!", style=discord.ButtonStyle.secondary)
    async def button_callback(self, button: Button, interaction: discord.Interaction):
        # This line should correctly respond to the interaction, not the button
        @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, custom_id="my_button")
        async def my_button_callback(self, button, interaction):
            await interaction.response.send_message("Here is a list of commands you can use:\n"
                                            "stat levelcheck - Check your current level\n" 
                                            "stat improve - Get feedback on your message and get a more refined version of it\n"  
                                            "stat levelup - Check how many messages you need to level up\n"
                                            "stat eval_msgs - Evaluate a user's message history\n"
                                            "stat improve_msg - get feedback on your message and a refined version of it\n"
                                            "stat msgstats - Check your message history stats\n"
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
