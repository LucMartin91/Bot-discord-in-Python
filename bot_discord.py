
import discord 
from discord.ext import commands
intents = discord.Intents.all()

class Node:
    def __init__(self, data):
        self.data = data
        self.next_node = None
        self.prev_node = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0


    def append(self, data):
        new_node = Node(data)
        if self.head is None: #Si la liste est vide, alors le nouveau node est = à la tête et à la queue de la liste
            self.head = self.tail = new_node
        else:
            new_node.prev_node = self.tail
            self.tail.next_node = new_node
            self.tail = new_node
        self.size += 1

    def get_last_n_messages(self, n):
        messages = []
        current_node = self.tail
        while current_node is not None and n > 0:
            messages.append(current_node.data)
            current_node = current_node.prev_node
            n -= 1
        return messages[::-1]
    

client = commands.Bot(command_prefix="!", intents = intents)

@client.command(name="history")
async def history(ctx):
    user = ctx.author
    messages_history = DoublyLinkedList()
    async for message in ctx.channel.history(limit=100):
        if message.author == user:
            messages_history.append(message.content)
            if messages_history.size == 10:
                break
    last_messages = messages_history.get_last_n_messages(10)
    response = f"Vos 10 derniers messages sont :\n"
    for msg in last_messages:
        response += msg + "\n"
    await ctx.send(response)

@client.command(name="salut") 
async def salut(ctx):
    await ctx.send("Salut bro")


@client.command(name="Hello")
async def delete(ctx):
    messages = await ctx.channel.history(limit=10)

    for each_message in messages:
        await each_message.delete()


@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_typing(channel, user, when):
     await channel.send(user.name+" is typing")

@client.event
async def on_member_join(member):
    general_channel = client.get_channel(1044900412551073832)
    await general_channel.send("Bienvenue sur le serveur ! "+ member.name)

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  message.content = message.content.lower()

  if message.content.startswith("hello"):
    await message.channel.send("Hello")

  if "cochon" in message.content:
    await message.channel.send(R)

  if message.content == "azerty":
    await message.channel.send("qwerty")

  await client.process_commands(message)

    

client.run("MTA5MTI1OTg5MDQ1MTg5MDIwOA.GGgAE8.ulXgnZAuDyeLU55Ukd_Vu3ahQ4qxNAytkhgpo4")