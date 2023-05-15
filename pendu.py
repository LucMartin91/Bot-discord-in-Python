import random

# Classe représentant le jeu de pendu
class Pendu:
    def __init__(self, mot):
        self.mot = mot.lower()
        self.lettres_trouvees = set()
        self.lettres_fausses = set()
        self.vies = 8

    def get_mot_masque(self):
        mot_masque = ""
        for lettre in self.mot:
            if lettre in self.lettres_trouvees:
                mot_masque += lettre
            else:
                mot_masque += "-"
        return f"{mot_masque} ({len(self.mot)} lettres)"


    def est_fini(self):
        return self.vies == 0 or set(self.mot) == self.lettres_trouvees

    def jouer(self, lettre):
        lettre = lettre.lower()
        if lettre in self.mot:
            self.lettres_trouvees.add(lettre)
        else:
            self.lettres_fausses.add(lettre)
            self.vies -= 1
