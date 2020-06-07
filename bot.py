import discord

c=discord.Client()
with open("token.txt")as f:
    jrr=f.read()
print("using token",jrr)
    
@c.event
async def on_ready():
    print(c.user.name, c.user.id, c.user.mention)

@c.event
async def on_message(m):
    if m.author==c.user:
        return
    #print(m.content)
    if(m.content.startswith(c.user.mention)or m.content.startswith("<@!"+str(c.user.id)+">")):
        await cmd_parse(m.content[1+m.content.find(">"):].strip(" \n"),m.channel)
    elif(c.user.mentioned_in(m)):
        await m.channel.send("stop fucking pinging me like holy shit")

async def ping(r,h):
    print(r)
    member=discord.utils.get(h.guild.members,id=int(r[0].strip("<>!@")))
    if member==None:
        await h.send("yo idk who the frick that is")
    elif member.id==c.user.id:
        await h.send("im not fucking pinging myself retar")
    else:
        txt=member.mention+" "+" ".join(r[2:]if len(r)>1 and r[1].isdigit()else r[1:])
        for i in range(0,int(r[1])if len(r)>1 and r[1].isdigit()else 1):
            await h.send(txt)
async def insult(r,h):
    await h.send("yo i havent implemented this feature yet holy shit")
async def bazinga(r,h):
    await h.send("yo i havent implemented this feature yet holy shit")
async def bp_parse(r,h):
    await h.send("yo i havent implemented this feature yet holy shit")
async def cmd_parse(t,h):
    ta=t.split()
    cmds={"ping":ping,
          "insult":insult,
          "bazinga":bazinga,
          "bensonpoints":bp_parse}
    if ta[0]in cmds:
        await cmds[ta[0]](ta[1:],h)
    else:
        await h.send("yo im literally not going to do that thats gay")
    
c.run(jrr)
