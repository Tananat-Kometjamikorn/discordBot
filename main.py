import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.ext.commands import has_permissions

load_dotenv('token.env')
discord_token = os.environ.get("DISCORD_TOKEN")     #get token from token.env
client = commands.Bot(command_prefix='!')  # กำหนด Prefix


@client.event
async def on_ready():  # เมื่อระบบพร้อมใช้งาน
    print('Ready. Logged in as: {0.user}'.format(client))  # แสดงผลในcmdว่าพร้อมใช้


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.event
async def on_message(message):  # ตัวประมวลผลข้อความ
    await client.process_commands(message)


@client.command()
async def hi(ctx):  # ดักรอข้อความใน Chat
    await ctx.reply('Hi, {}'.format(ctx.author.name))  # ข้อความที่ต้องการตอบกลับ


@client.command()
async def shout(ctx, *, message):  # ดักรอข้อความใน Chat
    await ctx.channel.send(message)  # ข้อความที่ต้องการส่ง


@client.command()
async def whoami(ctx):  # ส่งชื่อคนที่ถามกลับไป
    await ctx.channel.send('You are {}'.format(ctx.author.name))  # ข้อความที่ต้องการตอบกลับ


@client.command()
async def question(ctx): #ถามคำถามง่ายๆ
    await ctx.channel.send("1+1 = 2? [yes/no]")
    ans = await client.wait_for("message")
    if ans.content.lower() == "yes":
        await ctx.channel.send("You're right")
    else:
        await ctx.channel.send("Wrong answer, try again")


@client.command()
async def randpic(ctx):  # ส่งรูปแบบสุ่ม ต้องใส่รูปเข้าไปก่อนใน folder img
    indexRandom = random.randint(0, 1)  # กำหนด range ของการสุ่ม 0 ถึง จำนวนรูป - 1
    location = 'img/meme' + str(indexRandom) + '.PNG'  # ตัวอย่างชื่อรูป meme0.png meme1.png
    await ctx.channel.send(file=discord.File(location))


@client.command(pass_context=True)
async def join(ctx):  # บอทเข้าห้องเสียงและเล่นเพลง
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('music/Senbonzakura.mp3')
        voice.play(source)
        await ctx.channel.send('Music played')
    else:
        await ctx.channel.send('Enter the voice channel')


@client.command(pass_context=True)
async def leave(ctx):   #บอทออกห้องเสียง
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.channel.send('I left')
    else:
        await ctx.channel.send('Not in voice channel')


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send(f'{member} has been kicked')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("You don't have permission to do that!")


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f'{member} has been banned')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("You don't have permission to do that!")


@client.command()
async def goodbye(ctx):  # stop bot
    await ctx.channel.send("goodbye")
    await client.logout()


@client.command()
async def delete(ctx, limit=3):  #ลบข้อความ X ข้อความ default = 3 (รวมถึงบรรทัดที่พิมพ์คำสั่ง)
    await ctx.channel.purge(limit=limit)


client.run(discord_token)  # รันบอท (โดยนำ TOKEN จากบอทที่เราสร้างไว้นำมาวาง)
