import discord
import os
from discord.ext import commands
import asyncio

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

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def get_last_n_messages(self, n):
        messages = []
        current_node = self.tail
        while current_node is not None and n > 0:
            messages.append(current_node.data)
            current_node = current_node.prev_node
            n -= 1
        return messages[::-1]

class DecisionTree:
    def __init__(self, question=None, yes_branch=None, no_branch=None, answer=None):
        self.question = question
        self.yes_branch = yes_branch
        self.no_branch = no_branch
        self.answer = answer

    def is_leaf(self):
        return self.yes_branch is None and self.no_branch is None

help_tree = DecisionTree(
    "Avez-vous besoin d'aide pour les commandes ?",
    yes_branch=DecisionTree(
        "Cherchez-vous des commandes pour les administrateurs ?",
        yes_branch=DecisionTree(answer="Voici la liste des commandes pour les administrateurs :\n```!purge_all\n!addwhitelist\n!removewhitelist```"),
        no_branch=DecisionTree(answer="Voici la liste des commandes pour les utilisateurs :\n```\n!helpme\n!speak about\n!lastcmd\n!history\n!précédant\n!suivant\n!quitterhistory```"),
    ),
    no_branch=DecisionTree(
        "Avez-vous besoin d'aide pour jouer à un jeu ?",
        yes_branch=DecisionTree(answer="Voici comment jouer au Puissance 4 : \n /puissance4 and enjoy :)"),
        no_branch=DecisionTree(answer="D'accord, si vous avez besoin d'aide ultérieurement, tapez simplement /helpme."),
    ),
)





client = commands.Bot(command_prefix="!", intents = intents)
whitelisted_users = []
user_history_index = {}
user_message_count = {}

#Sécurité pour qu'un seul utilisateur puisse utiliser l'historique en même temps !
is_history_locked = False
history_locked_by = None

@client.command(name="quitterhistory")
async def clear_history(ctx, user_id: discord.Member = None):
    global is_history_locked
    global history_locked_by

    if history_locked_by == ctx.author:
        history_locked_by = None
        is_history_locked = False
    if user_id is None:
        user_id = ctx.author
    if user_id.id in user_history_index.keys():
        # Supprimer l'historique de l'utilisateur
        user_history_index.pop(user_id.id)
        await ctx.send("Historique quitté.")

@client.command(name="history")
async def history(ctx, user: discord.Member = None, n: int = 10, offset: int = 0):
    # Créer une nouvelle liste chaînée doublement liée pour stocker l'historique des messages
    messages_history = DoublyLinkedList()
    global is_history_locked
    global history_locked_by
    if is_history_locked:
        if history_locked_by != ctx.author:
            await ctx.send("Un utilisateur utilise déjà l'historique. Réssaie plus tard.")
            return
    else:
        is_history_locked = True
        history_locked_by = ctx.author

    # Si aucun utilisateur n'est spécifié, l'utilisateur courant sera utilisé
    if user is None:
        user = ctx.author
    
    # compter tous ses messages dans le canal courant qui commencent par "!" (préfixe de commande)
        message_total = 0   
        async for message in ctx.channel.history(limit=None):
            if message.author == user and message.content.startswith("!"):
                message_total += 1
        # Ajouter le nombre total de messages de l'utilisateur dans le dictionnaire "user_message_count"
        user_message_count[user.id] = message_total

    # Définir l'index de départ de l'historique de l'utilisateur
    is_history_locked = True
    user_history_index[user.id] = offset

    # Parcourir tous les messages dans le canal courant
    counter = 0
    async for message in ctx.channel.history(limit=None):
        # Si le message a été envoyé par l'utilisateur et commence par le préfixe de commande
        if message.author == user and message.content.startswith(client.command_prefix):
            # Si le compteur est supérieur ou égal à l'offset, ajouter le message à l'historique des messages
            if counter >= offset:
                messages_history.append(message.content)
                # Si l'historique des messages est égal au nombre souhaité, arrêter la boucle
                if messages_history.size == n:
                    break
            counter += 1

    # Récupérer les dernières n commandes de l'historique des messages
    last_messages = messages_history.get_last_n_messages(n)
    
    # Créer une réponse qui affiche l'index de départ, l'index de fin, le nombre total de messages de l'utilisateur et les n dernières commandes valides
    response = f"Index de l'historique : {offset}-{offset + len(last_messages)} / {message_total}\n"
    response += f"Vos {n} dernières commandes valides sont :\n"
    for msg in last_messages:
        # Retirer le préfixe de commande du message
        cmd_without_prefix = msg.lstrip(client.command_prefix)
        # Si la commande existe, l'ajouter à la réponse
        if client.get_command(cmd_without_prefix.split()[0]) is not None:
            response += msg + "\n"
    
    # Envoyer la réponse dans le canal courant
    await ctx.send(response)


@client.command(name="précédent")
async def previous(ctx, user_id: discord.Member = None):
    
    if user_id is None:
        user_id = ctx.author
    if user_id.id in user_history_index.keys():
        offset = max(0, user_history_index[user_id.id] - 10)
        if offset < user_history_index[user_id.id]:
            await history(ctx, user_id, offset=offset)
        else:
            await ctx.send("Vous êtes déjà au début de votre historique !")
    else:
        await ctx.send("Veuillez d'abord utiliser la commande !history.")

@client.command(name="suivant")
async def next(ctx, user_id: discord.Member = None):
    if user_id is None:
        user_id = ctx.author
    if user_id.id in user_history_index.keys():
        offset = user_history_index[user_id.id] + 10
        if offset < user_message_count[user_id.id]:
            await history(ctx, user_id, offset=offset)
        else:
            await ctx.send("Vous ne pouvez pas aller plus loin !")
    else:
        await ctx.send("Veuillez d'abord utiliser la commande !history.")

        
@client.command(name="helpme")
async def help_command(ctx):
    current_node = help_tree

    while not current_node.is_leaf():
        await ctx.send(current_node.question)

        def check(m):
            return m.author == ctx.author and m.content.lower() in ["oui", "non"]

        msg = await client.wait_for("message", check=check)
        answer = msg.content.lower()

        if answer == "oui":
            current_node = current_node.yes_branch
        else:
            current_node = current_node.no_branch

    await ctx.send(current_node.answer)

@client.command(name="reset")
async def reset_command(ctx):
    await help_command(ctx)

@client.command(name="speak_about")
async def speak_about_command(ctx, *, subject: str):
    subjects_handled = ["python", "java", "javascript", "ruby", "c++", "c#"]
    if subject.lower() in subjects_handled:
        await ctx.send(f"Oui, je peux parler de {subject}.")
    else:
        await ctx.send(f"Non, je ne peux pas parler de {subject}.")

spam_tracker = {}
        

@client.command(name="last_command")
async def last_command(ctx):
    await history(ctx, n=1)


@client.command(name="salut") 
async def salut(ctx):
    await ctx.send("Salut bro")

@client.command(name="purge_all")
@commands.has_permissions(administrator=True)
async def purge_all(ctx):
    # Demander confirmation avant de supprimer tous les messages
    await ctx.send("Êtes-vous sûr de vouloir supprimer tous les messages sur le serveur ? Cette action est irréversible. Répondez avec 'oui' pour confirmer.")
    
    # Attendre une réponse de confirmation pendant 30 secondes
    try:
        response = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.content.lower() == "oui", timeout=30)
    except asyncio.TimeoutError:
        # Si aucune réponse n'est donnée avant la fin du délai, annuler la commande
        await ctx.send("Temps écoulé. La commande a été annulée.")
        return
    
    # Supprimer tous les messages dans le serveur
    await ctx.send("Suppression de tous les messages en cours...")
    await ctx.channel.purge()
        
    # Confirmer que tous les messages ont été supprimés
    await ctx.send("Tous les messages ont été supprimés du serveur.")

@client.command(name="addwhitelist")
@commands.has_permissions(administrator=True)
async def add_to_whitelist(ctx, member: discord.Member):
    if member.id not in whitelisted_users:
        whitelisted_users.append(member.id)
        await member.edit(nick=f"[esprit]{member.display_name}")
        await ctx.send(f"{member.display_name} a été ajouté à la liste blanche.")
    else:
        await ctx.send(f"{member.display_name} est déjà dans la liste blanche.")


@client.command(name="removewhitelist")
@commands.has_permissions(administrator=True)
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

    
client.run("TOKEN")