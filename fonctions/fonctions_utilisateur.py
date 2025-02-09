from classes import Utilisateur
import fonctions.util as util
import fonctions.menu as menu


# Liste pour stocker les utilisateurs
utilisateurs = []
compteur_id = 1  # Compteur pour générer des IDs uniques
USERS_CSV = "./database/utilisateurs.csv"

# Fonction pour ajouter un utilisateur
def ajouter_utilisateur(nom, prenom, contact):
    global compteur_id
    # Créer un nouvel utilisateur avec un ID unique
    nouvel_utilisateur = Utilisateur(compteur_id, nom, prenom, contact)
    # Ajouter l'utilisateur à la liste
    utilisateurs.append(nouvel_utilisateur)
    print(f"Utilisateur {prenom} {nom} ajouté avec succès avec l'ID {compteur_id}.")
    compteur_id += 1  # Incrémenter le compteur d'ID pour le prochain utilisateur

# Fonction pour afficher la liste des utilisateurs
def afficher_utilisateurs():
    # Vérifier si la liste est vide
    if not utilisateurs:
        print("Aucun utilisateur trouvé.")
    else:
        # Afficher les informations de chaque utilisateur
        for utilisateur in utilisateurs:
            print(f"ID: {utilisateur.id_utilisateur}, Nom: {utilisateur.nom}, Prénom: {utilisateur.prenom}, Contact: {utilisateur.contact}")
            if utilisateur.emprunts:
                print(f"Emprunts: {', '.join(utilisateur.emprunts)}")
            else:
                print("Aucun emprunt en cours.")

# Fonction pour mettre à jour les informations d'un utilisateur
def mettre_a_jour_utilisateur(id_utilisateur, nouveau_nom=None, nouveau_prenom=None, nouveau_contact=None):
    # Chercher l'utilisateur par ID
    for utilisateur in utilisateurs:
        if utilisateur.id_utilisateur == id_utilisateur:
            # Mettre à jour les informations si elles sont fournies
            if nouveau_nom:
                utilisateur.nom = nouveau_nom
            if nouveau_prenom:
                utilisateur.prenom = nouveau_prenom
            if nouveau_contact:
                utilisateur.contact = nouveau_contact
            print(f"Utilisateur {id_utilisateur} mis à jour.")
            return
    print("Utilisateur non trouvé.")

# Fonction pour supprimer un utilisateur
def supprimer_utilisateur(id_utilisateur):
    # Chercher l'utilisateur par ID et le supprimer
    for utilisateur in utilisateurs:
        if utilisateur.id_utilisateur == id_utilisateur:
            utilisateurs.remove(utilisateur)
            print(f"Utilisateur {id_utilisateur} supprimé.")
            return
    print("Utilisateur non trouvé.")

# Fonction pour demander à l'utilisateur d'entrer ses informations
def saisir_informations_utilisateur():
    nom = input("Entrez le nom de l'utilisateur : ")
    prenom = input("Entrez le prénom de l'utilisateur : ")
    contact = input("Entrez le contact de l'utilisateur : ")
    ajouter_utilisateur(nom, prenom, contact)

# Fonction pour afficher le menu de gestion des utilisateurs
def menu_utilisateur():
    print("Options:", end="\n\n")
    print("1. Ajouter un utilisateur")
    print("2. Afficher la liste des utilisateurs")
    print("3. Mettre à jour les informations d'un utilisateur")
    print("4. Supprimer un utilisateur")
    # print("5. Ajouter un emprunt à un utilisateur")
    print("\n0. Retour")

    choix = input("\nChoisissez une option -> ")
    while not util.choix_valide(choix, 0, 5):
        choix = input("\nSaisie incorrecte, reessayez -> ")
    
    options_menu_utilisateur(choix)

# Fonction pour gérer les choix de l'utilisateur
def options_menu_utilisateur(choix: int):
    match choix:
        case 0:
            util.clear_screen()
            menu.menu()
        case 1:
            saisir_informations_utilisateur()
        case 2:
            # afficher_utilisateurs()
            Utilisateur.afficher_utilisateurs(USERS_CSV, 1)
        case 3:
            try:
                id_utilisateur = int(input("Entrez l'ID de l'utilisateur à mettre à jour : "))
                nouveau_nom = input("Entrez le nouveau nom (laissez vide pour ne pas changer) : ")
                nouveau_prenom = input("Entrez le nouveau prénom (laissez vide pour ne pas changer) : ")
                nouveau_contact = input("Entrez le nouveau contact (laissez vide pour ne pas changer) : ")
                mettre_a_jour_utilisateur(id_utilisateur, nouveau_nom or None, nouveau_prenom or None, nouveau_contact or None)
            except ValueError:
                print("ID invalide.")
        case 4:
            try:
                id_utilisateur = int(input("Entrez l'ID de l'utilisateur à supprimer : "))
                supprimer_utilisateur(id_utilisateur)
            except ValueError:
                print("ID invalide.")
        # elif choix == "5":
        #     try:
        #         id_utilisateur = int(input("Entrez l'ID de l'utilisateur pour ajouter un emprunt : "))
        #         emprunt = input("Entrez le titre de l'emprunt : ")
        #         ajouter_emprunt(id_utilisateur, emprunt)
        #     except ValueError:
        #         print("ID invalide.")                    

def write_headers(USERS_CSV):
    import os

    if os.path.getsize(USERS_CSV) == 0:
        with open(USERS_CSV, 'w') as f: 
            f.write("Id, Nom, Prenom, Contact")

def generer_id(nom_utilisateur: str) -> str:
    pass
