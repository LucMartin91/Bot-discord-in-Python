# Bot-discord-in-Python


LAST_COMMAND

-Commande permettant de renvoyer votre dernière commande


COMMANDE SALUT

-Commande basique qui quand on fait !salut renvoie une réponse du bot.


COMMANDE PURGE_ALL

-Commande d'admin qui supprime tous les messages d'un channel textuel. Demande une réponse 'oui' ou 'non' pour être sûr de supprimer. Message de confirmation envoyé dans le channel par le bot après la suppression réussie.


HISTORIQUE

-Commande d'historique avec un argument @ possible en plus pour regarder dans l'historique des commandes d'un joueur en particulier et pas uniquement le sien.
-Protection de l'historique via deux variables globales (un booleen qui sert de verrou pour savoir si l'historique est en cours d'utilisation, et une variable qui prend le nom de l'user en cours d'utilisation).
-un utilisateur possible à la fois pour l'historique.
-Possibilité de se déplacer dans l'historique (!suivant @user, !précédent) de l'user mentionné ou bien dans le vôtre (dans ce cas !suivant sans argument si c'est pour vous.) , Avec un index qui nous situe et le nombre total de commandes totales entrées par cet utilisateur pour se retrouver dans l'historique.
-Possibilité de purger l'historique via un purge_all (demande les permissions d'administrateur).


ARBRE DE DISCUSSION 

-Possibilité d'utiliser l'arbre binaire à l'aide de la commande !helpme (système de discussion en oui/non par l'utilisateur)
-Possibilité de reset notre position dans l'arbre grace à une commande !reset


SPEAK_ABOUT (Version améliorée du speak about classique demandé par lénoncé)

-Utilisation : !speak_about (ce que tu cherches)
-Utilisation de l'API Wikipedia pour un bot ayant le plus de connaissances possibles !
-Paramètre de langue de l'API update en français.
-Précision demandée en cas déchec de recherche par le bot dans l'API.
-Suggestion de différents sujets trouvés par l'API (les 10 premiers) si la question débouche sur plusieurs sujets (exemple Apple peut donner Apple Inc. Ou bien la pomme (fruit)).

WHITELIST

-Whitelist donnant accès à un grade invisible qui empêche d'être banni via le !ban
-utilisable uniquement par un admin
-Deux commandes, !addwhitelist et !removewhitelist pour gérer la whitelist
-Stockage et update de la whitelist à chaque changement dans un TXT pour pouvoir éteindre le bot sereinement tout en ayant un fichier mémoire qui sera re-chargé, ou re-créé s'il n'existe pas.

!BAN

-Commande basique qui requiert le pouvoir d'administrateur pour bannir un user (uniquement pas whitelisté)

PENDU

-Jeu du pendu utilisable via !pendu avec un message qui s'update à chaque tour pour éviter le spam, un timer et une liste de mots dans laquel le mot caché est choisi aléatoirement.

PROTECTION DU TOKEN

-Stockage du token dans un .ENV non divulgué ici pour garder une sécurité totale sur mon BOT personnel et éviter de laisser le token à la vue de tous.


