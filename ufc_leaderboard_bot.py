import os
from bs4 import BeautifulSoup
import requests 
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

URL = 'http://statleaders.ufc.com/'

def ufc_table(ID): 
    mes = ''
    mes += '```'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    total_fight_table = soup.find('article', id= ID, class_='results-group Fights-group')
    rows = total_fight_table.find_all('div', class_='results-table--tr')[1::]
    headers = total_fight_table.find_all('div', class_='results-table--tr')[0]
    row_titles = headers('span')
    header_text = [row_titles[0].get_text(), row_titles[1].get_text(),row_titles[2].get_text()]
    mes += '\n' + header_text[0]
    for head in header_text[1:]: 
        mes += '\t' + head 
    for fighter in rows: 
        name = fighter.a.text
        link = fighter.a['href']
        stats = fighter('span')
        rank = stats[0].get_text()
        points = stats[2].get_text()
        mes += '\n' + rank + '\t' + name + '\t' + points
    mes += '\n' + '```'
    return mes

@client.command(name = 'totalfights')
async def total_fights_display(com): 
    table = ufc_table("TotalFights-group")
    await com.send(table)

@client.command(name = 'wins')
async def wins_display(com): 
    table = ufc_table("Wins-group")
    await com.send(table)

@client.command(name = "fin")
async def finish_display(com): 
    table = ufc_table("Finishes-group")
    await com.send(table)

@client.command(name = "ko")
async def ko_display(com): 
    table = ufc_table("KOTKOWins-group")
    await com.send(table)

@client.command(name = "sub")
async def sub_display(com): 
    table = ufc_table("SubmissionWins-group")
    await com.send(table)

@client.command(name = "decision")
async def decision_display(com): 
    table = ufc_table("DecisionWins-group")
    await com.send(table)

@client.command(name = "streak")
async def streak_display(com): 
    table = ufc_table("WinStreak-group")
    await com.send(table)

@client.command(name = "titles")
async def titles_display(com): 
    table = ufc_table("TitleFightWins-group")
    await com.send(table)

@client.command(name = "awards")
async def awards_display(com): 
    table = ufc_table("TotalAwards-group")
    await com.send(table)

JBPATH = os.getenv('GIF_PATH')

@client.command()
async def jb(ctx): 
    file = discord.File(JBPATH, filename = 'justbleedguy.gif')
    bleed = discord.Embed(
        title = 'JUST BLEEEEED', 
        colour = discord.Colour.red()
    )
    bleed.set_image(url = 'attachment://justbleedguy.gif') 
    await ctx.send(file = file, embed=bleed)

client.run(TOKEN)