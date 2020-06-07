import discord

c=discord.Client()
with open("token.txt")as f:
    jrr=f.read()
print("using token",jrr)
    
@c.event
async def on_ready():
    print("reafy")

@c.event
async def on_message(m):
    if m.author==c.user:
        return
    await m.channel.send("fuck you")


c.run(jrr)
