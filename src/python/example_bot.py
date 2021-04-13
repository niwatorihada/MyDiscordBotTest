import discord
import sys

filename = "../../setting.env"
f = open(filename)
envs = f.read().split()
for env in envs:
    if env.startswith('TOKEN'):
        token = env.split(':')[1]
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!bye'):
        await message.channel.send('Bye!')
        await client.logout()
        await sys.exit()

client.run(token)
