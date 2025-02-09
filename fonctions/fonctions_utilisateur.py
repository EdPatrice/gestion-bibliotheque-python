from classes import Utilisateur, Gestion_Utilisateurs
import fonctions.util as util


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
    print("Ajout d'un nouvel utilisateur:\n")
    nom = input("Entrez le nom de l'utilisateur -> ")
    while not nom:
        nom = input("Nom invalide. Entrez le nom de l'utilisateur -> ")
    prenom = input("Entrez le prénom de l'utilisateur -> ")
    while not prenom:
        prenom = input("Prénom invalide. Entrez le prénom de l'utilisateur -> ")
    contact = input("Entrez le contact de l'utilisateur -> ")    
    while not contact:
        contact = input("Contact invalide. Entrez le contact de l'utilisateur -> ")
    user = Utilisateur(0, nom, prenom, contact)
    user.id_utilisateur = Gestion_Utilisateurs.generate_id(user)
    Gestion_Utilisateurs.enregistrer_utilisateur(user)
    util.clear_screen()
    print(user)
    print("\nUtilisateur ajouté avec succès.")
    util.wait()

# Fonction pour afficher le menu de gestion des utilisateurs
def menu_utilisateur(retour_au_menu_principal: bool = False):
    if retour_au_menu_principal:
        return
    print("Options:", end="\n\n")
    print("1. Ajouter un utilisateur")
    print("2. Afficher la liste des utilisateurs")
    print("3. Mettre à jour les informations d'un utilisateur")
    print("4. Supprimer un utilisateur")    
    print("\n0. Retour")

    choix = input("\nChoisissez une option -> ")
    while not util.choix_valide(choix, 0, 4):
        choix = input("\nSaisie incorrecte, reessayez -> ")
    choix = int(choix)
    options_menu_utilisateur(choix)

# Fonction pour gérer les choix de l'utilisateur
def options_menu_utilisateur(choix: int):
    util.clear_screen()
    match choix:
        case 0:
            menu_utilisateur(True)
            return
        case 1:
            saisir_informations_utilisateur()

        case 2:            
            Gestion_Utilisateurs.afficher_utilisateurs(1)
            util.wait()

        case 3:            
            print("Liste des utilisateurs:\n")
            Gestion_Utilisateurs.afficher_utilisateurs()
            id_utilisateur = input("\nEntrez l'ID de l'utilisateur à mettre à jour -> ")
            while Gestion_Utilisateurs.get_user_info(id_utilisateur)[0] == None:
                id_utilisateur = input("ID invalide. Entrez l'ID de l'utilisateur à mettre à jour -> ")                       
            util.clear_screen()
            Gestion_Utilisateurs.modifier_utilisateur(id_utilisateur)
            util.wait()

        case 4:
            print("Liste des utilisateurs:\n")
            Gestion_Utilisateurs.afficher_utilisateurs()
            id_utilisateur = input("\nEntrez l'ID de l'utilisateur à supprimer -> ")
            while not Gestion_Utilisateurs.get_user_info(id_utilisateur)[0]:
                id_utilisateur = input("Sasie incorrecte. Entrez l'ID de l'utilisateur à supprimer -> ")
            Gestion_Utilisateurs.supprimer_utilisateur(id_utilisateur)
            util.wait()                        

    util.clear_screen()
    menu_utilisateur()                   
