import discord
import os
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



class nodetree : 
  def __init__(self, question, reponses):
    self.question = question
    self.reponses = reponses
    self.next_nodes = []

class treediscution : 
  def __init__(self,first_question):
    self.first_node = nodetree(first_question,[])
    self.current_node = self.first_node

  def append_question(self,question,reponses,previous_question):
    pass

  def delete_question(self,question):
    pass

  def get_question(self):
    return self.current_node.question

  def send_answer(self, reponse):
    pass


client = commands.Bot(command_prefix="!", intents = intents)
whitelisted_users = []
user_history_index = {}
user_message_count = {}

@client.command(name="history")
async def history(ctx, n: int = 10, offset: int = 0):
    user = ctx.author
    messages_history = DoublyLinkedList()

    user_history_index[user.id] = offset

    counter = 0
    async for message in ctx.channel.history(limit=None):
        if message.author == user and message.content.startswith(client.command_prefix):
            counter += 1
            if counter > offset:
                messages_history.append(message.content)

        if messages_history.size == n:
            break

    last_messages = messages_history.get_last_n_messages(n)
    response = f"Vos {n} dernières commandes valides sont :\n"
    for msg in last_messages:
        cmd_without_prefix = msg.lstrip(client.command_prefix)
        if client.get_command(cmd_without_prefix.split()[0]) is not None:
            response += msg + "\n"
    await ctx.send(response)

@client.command(name="précédent")
async def previous(ctx):
    user_id = ctx.author.id
    if user_id in user_history_index:
        offset = user_history_index[user_id] + 10
        await history(ctx, offset=offset)
    else:
        await ctx.send("Veuillez d'abord utiliser la commande !history.")

@client.command(name="suivant")
async def next(ctx):
    user_id = ctx.author.id
    if user_id in user_history_index:
        offset = max(0, user_history_index[user_id] - 10)
        await history(ctx, offset=offset)
    else:
        await ctx.send("Veuillez d'abord utiliser la commande !history.")

@client.command(name="last_command")
async def last_command(ctx):
    await history(ctx, n=1)


@client.command(name="salut") 
async def salut(ctx):
    await ctx.send("Salut bro")


@client.command(name="Hello")
async def delete(ctx):
    messages = await ctx.channel.history(limit=10)

    for each_message in messages:
        await each_message.delete()

@client.command(name="addwhitelist")
async def add_to_whitelist(ctx, member: discord.Member):
    if member.id not in whitelisted_users:
        whitelisted_users.append(member.id)
        await member.edit(nick=f"[esprit]{member.display_name}")
        await ctx.send(f"{member.display_name} a été ajouté à la liste blanche.")
    else:
        await ctx.send(f"{member.display_name} est déjà dans la liste blanche.")


@client.command(name="removewhitelist")
async def remove_from_whitelist(ctx, member: discord.Member):
    if member.id in whitelisted_users:
        whitelisted_users.remove(member.id)
        await member.edit(nick=member.name)
        await ctx.send(f"{member.display_name} a été retiré de la liste blanche.")
    else:
        await ctx.send(f"{member.display_name} n'est pas dans la liste blanche.")

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

  if message.content == "azerty":
    await message.channel.send("qwerty")

  await client.process_commands(message)

    

client.run("MTA5MTI1OTg5MDQ1MTg5MDIwOA.G-lwKd.lBZaAzBa0y9MXNQd2V8qtUkkpPwMaHX34Ti4t0")