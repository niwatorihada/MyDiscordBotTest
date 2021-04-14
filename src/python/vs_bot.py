import discord
import sys
import random

filename = "../../setting.env"
f = open(filename)
envs = f.read().split()
for env in envs:
    if env.startswith('TOKEN'):
        token = env.split(':')[1]
    if env.startswith('CHANNEL_ID'):
        bot_channel_id = int(env.split(':')[1])
client = discord.Client()

# 起動時の処理
async def start():
    channel = client.get_channel(bot_channel_id)
    embed = discord.Embed(title='duel bot 起動', description='対戦を管理するbotです', color=0x00ff00)
    await channel.send(embed=embed)

# 終了時の処理
async def end():
    channel = client.get_channel(bot_channel_id)
    embed = discord.Embed(title='duel bot 終了', description='さよなら', color=0xff0000)
    await channel.send(embed=embed)
    await client.logout()
    await sys.exit()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await start()

@client.event
async def on_message(message):
    # 自分に反応しないように
    if message.author == client.user:
        return

    # 埋め込みテキストで参戦者を決める
    if message.content.startswith('!duel'):
        players = []

        embed = discord.Embed(title='対戦カード', description='対戦者はリアクションを押してください', color=0xff0000)
        embed.add_field(name='対戦者1', value='募集中...\n__', inline=True)
        embed.add_field(name='対戦者2', value='募集中...\n__', inline=True)
        msg = await message.channel.send(embed=embed)

        # リアクションをつける
        await msg.add_reaction('💪')
        await msg.add_reaction('👋')
        await msg.add_reaction('🆗')
        await msg.add_reaction('❌')

        def check(reaction, user):
            emoji = str(reaction.emoji)
            if user.bot == True:
                pass
            else:
                return emoji == '💪' or emoji == '🆗' or emoji == '👋' or emoji == '❌'

        while True:
            target_reaction, user = await client.wait_for('reaction_add', check=check)

            # 参加表明
            if target_reaction.emoji == '💪':
                if len(players) < 2:
                    players.append(user.name)
                if len(players) == 1:
                    embed.set_field_at(0, name='対戦者1', value=players[0]+'\n__', inline=True)
                    embed.set_field_at(1, name='対戦者2', value='募集中...\n__', inline=True)
                elif len(players) == 2:
                    embed.set_field_at(0, name='対戦者1', value=players[0]+'\n__', inline=True)
                    embed.set_field_at(1, name='対戦者2', value=players[1]+'\n__', inline=True)
                else:
                    pass

            # 先行後攻を決める
            elif target_reaction.emoji == '🆗':
                if len(players) == 2:
                    if random.randint(1, 2) == 1:
                        order = ['先行', '後攻']
                    else:
                        order = ['後攻', '先行']

                    embed.set_field_at(0, name='対戦者1', value=players[0]+'\n__', inline=True)
                    embed.set_field_at(1, name='対戦者2', value=players[1]+'\n__', inline=True)
                    await msg.edit(embed=embed)

                    embed.set_field_at(0, name='対戦者1', value=players[0]+'\n'+order[0], inline=True)
                    embed.set_field_at(1, name='対戦者2', value=players[1]+'\n'+order[1], inline=True)

            # 参加を取り消す
            elif target_reaction.emoji == '👋':
                if len(players) > 0:
                    players.remove(user.name)
                    if len(players) == 0:
                        embed.set_field_at(0, name='対戦者1', value='募集中...\n__', inline=True)
                        embed.set_field_at(1, name='対戦者2', value='募集中...\n__', inline=True)
                    elif len(players) == 1:
                        embed.set_field_at(0, name='対戦者1', value=players[0]+'\n__', inline=True)
                        embed.set_field_at(1, name='対戦者2', value='募集中...\n__', inline=True)

            # botを終了する
            elif target_reaction.emoji == '❌':
                await end()

            else:
                pass

            await msg.edit(embed=embed)

    # 終了コマンド
    if message.content.startswith('!bye'):
        await end()

client.run(token)
