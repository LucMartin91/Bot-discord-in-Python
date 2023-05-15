
import discord
import os
import random
import string
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from decisiontree import DiscussTree
from linkedlist import Node, DoublyLinkedList
from pendu import Pendu

intents = discord.Intents.all()
help_tree = DiscussTree(
    "Avez-vous besoin d'aide pour les commandes ?",
    yes_branch=DiscussTree(
        "Cherchez-vous des commandes pour les admins ?",
        yes_branch=DiscussTree(answer="Voici la liste des commandes pour les administrateurs :\n```!purge_all\n!addwhitelist\n!removewhitelist```"),
        no_branch=DiscussTree(answer="Voici la liste des commandes pour les utilisateurs :\n```\n!helpme\n!speak_about\n!last_command\n!history\n!précédent\n!suivant\n!quitterhistory```"),
    ),
    no_branch=DiscussTree(
        "Avez-vous besoin d'aide pour jouer à un jeu ?",
        yes_branch=DiscussTree(answer="Voici comment jouer au pendu : \n !pendu , puis tentez de trouver le mot caché ! Vous aurez 8 vies."),
        no_branch=DiscussTree(answer="Très bien, si vous avez besoin d'aide ultérieurement, tapez simplement !helpme."),
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
# compter tous ses messages dans le canal courant qui commencent par "!" (préfixe de commande)
    message_total = 0   
    async for message in ctx.channel.history(limit=None):
        if message.author == user and message.content.startswith("!"):
            message_total += 1
        # Ajouter le nombre total de messages de l'utilisateur dans le dictionnaire "user_message_count"
    user_message_count[user.id] = message_total
    
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
        

@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_user(ctx, member: discord.Member):
    # Vérifier si l'utilisateur à bannir est dans la liste blanche
    if member.id in whitelisted_users:
        await ctx.author.send(f"L'utilisateur {member.mention} ne peut pas être banni car il est dans la liste blanche.")
    else:
        await member.ban()
        await ctx.send(f"L'utilisateur {member.mention} a été banni.")

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
        await ctx.send(f"{member.display_name} a été ajouté à la liste blanche.")
    else:
        await ctx.send(f"{member.display_name} est déjà dans la liste blanche.")


@client.command(name="removewhitelist")
@commands.has_permissions(administrator=True)
async def remove_from_whitelist(ctx, member: discord.Member):
    if member.id in whitelisted_users:
        whitelisted_users.remove(member.id)
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

# Liste des mots possibles
mots = ["python", "programmation", "discord", "bot", "jouer", "pendu", "projet"]

# Fonction pour récupérer un mot aléatoire
def get_mot_aleatoire():
    return random.choice(mots)

# Commande de jeu de pendu
@client.command(name="pendu")
async def pendu(ctx):
    mot = get_mot_aleatoire()
    pendu = Pendu(mot)
    mot_masque = pendu.get_mot_masque()

    message = await ctx.send(f"Le mot à deviner est : {mot_masque}. Vous avez {pendu.vies} vies.")
    while not pendu.est_fini():
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and len(message.content) == 1 and message.content.lower() in string.ascii_lowercase and message.content.lower() not in pendu.lettres_trouvees.union(pendu.lettres_fausses)

        try:
            lettre = await client.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé, le jeu est terminé.")
            return

        pendu.jouer(lettre.content)
        mot_masque = pendu.get_mot_masque()
        message = await message.edit(content=f"Le mot à deviner est : {mot_masque}. Vous avez {pendu.vies} vies.\nLettres fausses : {', '.join(sorted(pendu.lettres_fausses))}")
        
    if pendu.vies > 0:
        await ctx.send(f"Bravo, vous avez trouvé le mot '{mot}' !")
    else:
        await ctx.send(f"Dommage, vous avez perdu. Le mot était '{mot}'.")

#récupération du token dans le .env et lancement du bot !
load_dotenv()
token = os.getenv('TOKEN')
client.run(token)