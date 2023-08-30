from turtle import pos
import asycnpraw, asyncio, config
import discord
from discord.ext import commands
import string
import json
import os, sqlite3
intents=discord.Intents().all()
bot=commands.Bot(command_prefix='!', intents=intents)
reddit=asycnpraw.Reddit(client_id=config.settings['ID'],\
    client_secret=config.settings['SECRET'],  user_agent='reddit_bot')
posts=[]
TIMEOUT=10
NAME='memes'                                        #имя поста
LIMIT=1
async def start(ctx):
    for ch in bot.get_guild(ctx.author.guild.id).channels:                     #цикл
        if ch.name=='основной':
            channel=ch
    while True:#ьесконечный ц икл
        await asyncio.sleep(TIMEOUT)
        posts_submissions=await reddit.subreddit(NAME)                             #паблик с мемами 
        posts_submissions=posts_submissions.new(limit=LIMIT)
        item=await posts_submissions.__anext__()
        if item.title not in posts:
            posts.append(item.title)
            await channel.send(item.url)

        



 
@bot.event
async def on_ready():
    print('GG')
    global base, cur
    base=sqlite3.connect('data.db')
    cur=base.cursor()
    if base:
        print('Vse ok')
@bot.command()
async def test(ctx):
    await ctx.send('тута')
    
@bot.command()
async def info(ctx, arg= None):
    author=ctx.message.author
    if arg==None:
        await ctx.send(f'{author} Введите:\n!info общ\n!info кмд')
    elif arg =='общ':
        await ctx.send(f'{author} ЭТО ОБЖ  o(￣┰￣*)ゞ')
    elif arg == 'кмд':
        await ctx.send(f'{author} Я- бот, слежу за порядком в чате.')
    else:
        await ctx.send(f'{author} Такой КМД нет ')
@bot.command()
async def status(ctx):
    base.execute(f"CREATE TABLE IN NOT EXISTS '{ctx.message.guild.name}'(userid INT, countINT)")
    base.commit()
    warnings=cur.execute(f"SELECT*FROM'{ctx.message.guild.name}'WHERE userd==?", (ctx.message.author.id)).fetchone()
    if warnings==None:
        await ctx.send(f'{ctx.message.author.mention}, Анонимусов нету')
    else:
        await ctx.send(f'{ctx.message.author.mention}, ага вот он анонимус, у тебя {warnings[1]} предупреждений  Я СЛИЖУ ЗА ТОБОЙ!!!!!!666')
    

@bot.event
async def on_message(message):    #GG
    if 'колобок' in message.content.lower():
            await message.channel.send('Коммунизм не одобряет(⌐■_■)')
            await message.delete()
@bot.command()
@commands.has_permissions(manage_messages=True)
async def BAN(ctx, member:discord.Member):
    BAN=discord.utils.get(member.guild.roles, name='BAN')
    MEOWMEOW=discord.utils.get(member.guild.roles, name='MEOWMEOW')
    await member.add_roles(BAN)
    await member.remove_roles(MEOWMEOW)
    await ctx.send(f'{member.mention}потерял дар мяукать ╯︿╰')
    await member.send(f'Лови ФЛЭШБЭК/BAN, ты больше не можешь поддерживать высокоинтелектуальные диологи XD')


@bot.event
async def on_message(message):
   if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.content.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.channel.send(f'{message.author.mention},ЭЭЭЭЭЭЭ не делай так за это я дам бан(T_T)')
        await message.delete()
        name=message.guild.name
        base.execute(f"CREATE TABLE IF NOT EXISTS '{message.guild.name}'(userid INT, count INT)")
        base.commit()
        warnings=cur.execute(f"SELECT*FROM'{message.guild.name}'WHERE userid==?", (message.author.id,)).fetchone()
        if warnings==None:
            cur.execute(f"INSERT INTO'{message.guild.name}'VALUES(?, ?)", (message.author.id, 1))
            base.commit()
            await message.channel.send(f'{message.author.mention}, 1-е чаладой маловек хватит камнятся брасами, еще 2 и я тебя чик чурык из сообщества')
        elif warnings[1]==1:
            cur.execute(f"UPDATE '{message.guild.name}' SET count == ? WHERE userid == ?",(2,message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, 2-e ты по мойму перепутал ')
        elif warnings[1]==2:
            cur.execute(f"UPDATE'{message.guild.name}'SET count==? WHERE userid==?", (3, message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, 3-e ТЫ  ЗА МЕНЯ ПРИДУРКА НЕ ДЕРЖИ, ЛОВИ БАНАН!!! ')
            await message.author.ban(reason='Этот сервер для порядочных жителей XD')
            
            

@bot.command()
async def send(ctx):
    await ctx.author.send('я плачу налоги')
async def test(ctx):
    await ctx.author.send('ага')

@bot.command()
async def send_member(ctx, member:discord.Member):
    await member.send(f'{member.name},привет от {ctx.author.name}')
@bot.command()
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
@bot.event
async def on_member_join(member):
    await member.send('поздравляю с тем ,что ты не знаешь статью 3 26.1 закон о защите прав потребителя ')


    BAN=discord.utils.get(member.guild.roles, name='BAN')
    MEOWMEOW=discord.utils.get(member.guild.roles, name='MEOWMEOW')
    #await member.add_roles(MEOWMEOW) на будушие
    base.execute(f"CREATE TABLE IF NOT EXISTS '{member.guild.name}'(userid INT, count INT, mute INT)")
    check=cur.execute(f"SELECT * FROM '{member.guild.name}' WHERE userid==?",(member.id,)).fetchone()
    if check == None:
        cur.execute(f"INSERT INTO '{member.guild.name}' VALUES(?, ?, ?)",(member.id, 0, 0))
        base.commit()
        await member.add_roles(MEOWMEOW)
    elif check[2] == 0:
        await member.add_roles(MEOWMEOW)
    else:
        await member.add_roles(BAN)


    for ch in bot.get_guild(member.guild.id).text_channels:
        if ch.name=='общее':
            await bot.get_channel(ch.id).send(f'{member.name}, новый житель ссср добавлен')
@bot.event
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name=='общее':
            await bot.get_channel(ch.id).send(f'{member}, житель  умер от депрессии')

bot.run(os.getenv('TOKEN'))