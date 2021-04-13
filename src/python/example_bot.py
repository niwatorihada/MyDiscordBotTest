import discord
import sys
import random

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
    # 自分に反応しないように
    if message.author == client.user:
        return
    
    # 挨拶を返す
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    # サイコロ
    if message.content.startswith('!diceroll'):
        await message.channel.send(str(random.randint(1,6)))

    # 終了コマンド
    if message.content.startswith('!bye'):
        await message.channel.send('Bye!')
        await client.logout()
        await sys.exit()

client.run(token)
