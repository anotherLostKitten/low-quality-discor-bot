from time import time
from urllib import request, parse
from urllib.error import HTTPError
import json #tongue
from random import randint, choice

import discord

import db_stuff as dbs

c=discord.Client()
with open("token.txt")as f:
    jrr=f.read()
#print("using token",jrr)
ping_history={}
steal_history={}

@c.event
async def on_ready():
    print(c.user.name,c.user.id,c.user.mention)

@c.event
async def on_message(m):
    if m.author==c.user:
        return
    #print(m.content)
    if(m.content.startswith(c.user.mention)or m.content.startswith("<@!"+str(c.user.id)+">")):
        await cmd_parse(m.content[1+m.content.find(">"):].strip(" \n"),m)
    elif(c.user.mentioned_in(m)):
        await m.channel.send("stop fucking pinging me like holy shit")
def mbr(uid,m):
    try:
        return discord.utils.get(m.guild.members,id=int(uid.strip("<>!@")))
    except ValueError:
        return None
        
async def ping(r,m):
    print(r)
    member=mbr(r[0],m)
    if member==None:
        await m.channel.send(choice(("yo idk who the frick that is","???????? literally no? ur stupid?","fun fact: im not fucking pinging whatever the fuck that is supposed to be you actual ritardando")))
    elif member.id==c.user.id:
        await m.channel.send("im not fucking pinging myself retar")
    else:
        if len(r)>1 and r[1].isdigit():
            n=int(r[1])
            if(n>12):
                await m.channel.send(choice(("im literally not doing that its too much effort","tbh i can only count to 12 (get it because pedophilia)","holy shit if you want to ping them so bad do it yourszzelf")))
            elif okping(m.author.id):
                txt=member.mention+" "+" ".join(r[2:])
                for i in range(0,n):
                    await m.channel.send(txt)
            else:
                await m.channel.send("yo i literally just did that retard")
        elif okping(m.author.id):
            await m.channel.send(member.mention+" "+" ".join(r[1:]))
        else:
            await m.channel.send("yo i literally just did that retard")
def okping(uid,thing=ping_history,dt=60):
    e=not uid in thing or time()-thing[uid]>dt
    if e:
        thing[uid]=time()
    return e
async def fact(r,m):
    try:
        url=request.urlopen("https://api.jokes.one/jod")
        wdict=json.loads(url.read())
        #print(wdict)
        txt=wdict['contents']['jokes'][0]['joke']['text'].lower().replace("\r","").replace(",","").replace(".","")
        for e in txt.splitlines():
            if(e!=""):
                await m.channel.send(e)
        if randint(0,5)==0:
            await m.channel.send(choice(("haha get it its funny because fuck you", m.author.mention+" do you agree", m.author.mention+" ^")))
    except HTTPError:
        await m.channel.send(choice(("idk there was a fuckign http error? maybe next time try not being retar?","yo actually tho imagine rate limiting your shitty jokes api","for some reasoin there's a fuckign rate limit of 10 requests an hour like lmao you cant fucking return a fucking tiny ass sentence on demand??? nice fuyckign dial up retarr","uhhh maybe try again in fuck you")))
async def insult(r,m):
    await m.channel.send("yo i havent implemented this feature yet holy shit")
async def bazinga(r,m):
    await m.channel.send("yo i havent implemented this feature yet holy shit")

async def bp_give(r,m):
    try:
        v=int(r[1])
    except ValueError:
        await m.channel.send("literally not a number dumbass")
        return
    if v<0:
        await m.channel.send("haha look at you your going to give him a negative number so you steal his benson points haha waht an actual fucking gneious except no you fucking arnt you fucking stupid of subhuman filth")
    else:
        e=mbr(r[0],m)
        if(e==None):
            await m.channel.send("yo idk who that is? retar? idyo? stupi?")
        elif v==0 or e==m.author:
            await m.channel.send("nice noop")
        elif dbs.mod_bp(m.author.id,-v,False):
            dbs.mod_bp(e.id,v,True)
            await m.channel.send("after ur generous donation {} has {} benson points adn you have {}".format(e.mention,dbs.get_bp(e.id),dbs.get_bp(m.author.id)))
        else:
            await m.channel.send("yuoure to poor check kiting looking ass")
async def bp_steal(r,m):
    try:
        v=int(r[1])
    except ValueError:
        await m.channel.send("literally not a number dumbass")
        return
    if v<0:
        await m.channel.send("basically use the give command instead dumbass")
    else:
        e=mbr(r[0],m)
        if(e==None):
            await m.channel.send("yo idk who that is? retar? idyo? stupi?")
        elif v==0 or e==m.author:
            await m.channel.send("nice noop")
        elif dbs.get_bp(e.id)/7<v:
            await m.channel.send("you cant steal that much money tho he too poor this isnt like fucking income tax or smthn")
        elif okping(m.author.id,steal_history,300):
            if randint(0,1)==0:
                dbs.mod_bp(m.author.id,v,True)
                dbs.mod_bp(e.id,-v,True)
                await m.channel.send("yo congrats fricking james bomd or whatever {} has {} benson points adn you have {}".format(e.mention,dbs.get_bp(e.id),dbs.get_bp(m.author.id)))
            else:
                dbs.mod_bp(m.author.id,-v,True)
                dbs.mod_bp(e.id,v,True)
                await m.channel.send("ok so youre so frimcking bad at stealign shit you accidentally stole your own moneyt and gave it to {} who now has {} besnogne poisnt while you have {}".format(e.mention,dbs.get_bp(e.id),dbs.get_bp(m.author.id)))
                if(dbs.get_bp(m.author.id)<0):
                    await m.channel.send("hahahahahaha holy shit you're so fucking bad at this you literally have negative benson points lmao be careful if you have too much negative benson points you might just get beaned for no reason")
        else:
            await m.channel.send("do to ur reacent theft attempt ur on the fbi most wanted list rn so try again laterr")
async def bp_shop(r,m):
    await m.channel.send("yo i havent implemented this benson points feature yet holy shit")
async def bp_mod(r,m):
    if(not m.author.guild_permissions.administrator):    
        await m.channel.send("yarnt admin frick off")
    try:
        v=int(r[1])
    except ValueError:
        await m.channel.send("nice retar math")
        return
    e=mbr(r[0],m)
    if(e==None):
        await m.channel.send("yo idk who that is? retar? idyo? stupi?")
        return
    dbs.mod_bp(e.id,v,True)
    await m.channel.send("ok so basically {} now has {} besnos poiusnt".format(e.mention,dbs.get_bp(e.id)))
async def bp_show(r,m):
    if len(r)>0:
        e=mbr(r[0],m)
        if(e!=None):
            await m.channel.send("{} literally has {} benson points like wtfrick".format(e.mention,dbs.get_bp(e.id)))
        else:
            await m.channel.send("i have no idea waht you want")
    else:
        await m.channel.send("yuou have {} benson poitns woa".format(dbs.get_bp(m.author.id)))
async def bp_parse(r,m):
    cmds={"give":bp_give,
          "steal":bp_steal,
          "shop":bp_shop,
          "modify":bp_mod,
          "show":bp_show
    }
    if(len(r)==0 or not r[0]in cmds):
        await bp_show(r,m)
    else:
        await cmds[r[0]](r[1:],m)
async def gh(r,m):
    await m.channel.send("not that its any of yuour fuckign business but https://github.com/anotherLostKitten/low-quality-discor-bot")
async def cmd_parse(t,m):
    ta=t.split()
    cmds={"ping":ping,
          "insult":insult,
          "bazinga":bazinga,
          "bensonpoints":bp_parse,
          "bp":bp_parse,
          "fact":fact,
          "github":gh}
    if ta[0]in cmds:
        await cmds[ta[0]](ta[1:],m)
    else:
        await m.channel.send(choice(("yo im literally not going to do that that thats gay","haha good one just kidding no it wasnt fukc you","yo actually stfu","holy shit just fucking bing it","@Mohammed Uddin\nhad a very red penis\nsadly it fell off","idk ask benson","literally noone cares","oh true","gOOD point")))
    
c.run(jrr)
