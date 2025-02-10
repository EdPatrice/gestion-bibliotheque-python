import fonctions.util as util
#importation du module 
import os 
#importation du module csv
import csv
#importation du module de regex
import re
from classes import  Livre, Gestion_Livres


#fonction option 1 
manager = Gestion_Livres()

def menu_livre(retour_au_menu_principal = False):
    
    if retour_au_menu_principal:
        return
    else:
        print("------------Gestion des livres------------\n\n")
        print("1. Enregistrer un livre.")
        print("2. Mise à jour d'un livre.")
        print("3. Recherche d'un livre.")
        print("4. Supprimer un livre.")
        print("5. La liste des livres.")
        print("\n0. Retour au menu principal.")

        choix = input("\nChoisissez une option -> ")
        while not util.choix_valide(choix, 0, 5):
            choix = input("Veuillez insérer une valeur se trouvant dansa la liste -> ")
        choix = int(choix)
        options_menu_livre(choix)

def options_menu_livre(choix: int):  

    util.clear_screen()
    match choix : 
        case 0:
            menu_livre(True)
            return

        case 1 : 
            util.clear_screen()
            id = demander_id()
            titre = input("Quel est le titre du livre \t-> ").strip()
            auteur = input("Quel(le) est l'auteur(e) \t-> ").strip()
            genre = input("Quel est le genre du livre \t-> ").strip()
            manager.ajouter(id, titre, auteur, genre)  # Ajoute le livre à la liste
            ajouter(id, titre, auteur, genre)  # Sauvegarde le livre dans le fichier CSV
            util.wait()            

        case 2 :
            util.clear_screen()
            lecture_csv()
            id = input("\nVeuillez insérer l'ISBN pour faire la modification : -> ")
            util.clear_screen()
            modification(id)
            util.wait()            

        case 3 : 
            util.clear_screen()
            lecture_csv()
            valeur = input("\nVeuillez insérer le titre, l'auteur ou le genre du livre à rechercher -> ")
            search(valeur)
            util.wait()            
        
        case 4 : 
            util.clear_screen()
            lecture_csv()
            id = input("\nEntrer l'ISBN du livre -> ")
            sup(id)
            util.wait()             

        case 5 :
            util.clear_screen()
            lecture_csv()
            util.wait() 
    
    util.clear_screen()
    menu_livre()           


# Chemin vers le fichier CSV
files = util.read_json("config.json")
BOOKS_CSV = files["BOOKS_CSV"]

# Instancier la gestion des livres
gestion_livres = Gestion_Livres()

# Fonction d'ajout
def ajouter(id: str, titre: str, auteur: str, genre: str):
    livre = Livre(id, titre, auteur, genre)
    gestion_livres.ajouter(id, titre, auteur, genre)

    # Vérification de l'existence du fichier et s'il est vide
    fichier_existe = os.path.isfile(BOOKS_CSV)
    fichier_vide = fichier_existe and os.stat(BOOKS_CSV).st_size == 0

    with open(BOOKS_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=livre.__dict__.keys())

        # Si le fichier est vide ou n'existe pas, écrire l'en-tête
        if not fichier_existe or fichier_vide:
            writer.writeheader()

        writer.writerow(livre.__dict__)
        print("Livre enregistré avec succès.")



#verification du format et l'unicité de l'id 
def format(id):
    pattern = r'^\d{3}-\d{1}-\d{2}-\d{6}-\d{1}$'
    
    # Vérification de la chaîne de caractères (ISBN)
    if not re.match(pattern, id):
        print(f"Erreur : L'ISBN {id} ne respecte pas le format 'xxx-x-xx-xxxxxx-x'. Veuillez réessayer !!")
        return False
    
    id_existants = set()
    
    try:
        with open(BOOKS_CSV, mode="r", newline="") as file:
            reader = csv.DictReader(file)  # Lire le fichier sous forme de dictionnaire
            for row in reader:
                if "id" in row and row["id"]:  # Vérifier si la colonne ISBN existe et n'est pas vide
                    id_existants.add(row["id"])
    except FileNotFoundError:
        print("Erreur : Le fichier 'livres.csv' n'a pas été trouvé.")
        return False
    
    # Vérification de l'unicité
    if id in id_existants:
        print(f"Erreur : L'ISBN {id} existe déjà.")
        return False
    
    return True



def demander_id():
    while True:
        id = input("Veuillez entrer un ISBN au format 'xxx-x-xx-xxxxxx-x' : ")
        if format(id):  
            return id  


#fonction lecture du fichier csv
def lecture_csv():
    with open(BOOKS_CSV, 'r', newline='') as f:
        lire = csv.DictReader(f)
        
        print("La liste des livres enregistrées : \n")
        print(f"{'ID':<20}{'Titre':<30}{'Auteur':<30}{'Genre':<20}")
        print("-" * 100)
        
        for ligne in lire:
            # Vérifiez que les clés existent dans le dictionnaire ligne
            if 'id' in ligne and 'title' in ligne and 'author' in ligne and 'genre' in ligne:
                print(f"{ligne['id']:<20}{ligne['title']:<30}{ligne['author']:<30}{ligne['genre']:<20}")
            else:
                print("Erreur : En-tête manquant ou incorrect dans le fichier CSV.")




#fonction de mise à jour
def modification(id):
    # Vérifie si le fichier existe
    if not os.path.isfile(BOOKS_CSV):
        print("Aucun livre enregistré.")
        return

    while True:
        # Lire le fichier CSV et stocker les lignes dans une liste
        lignes = []
        trouve = False

        with open(BOOKS_CSV, 'r', newline='') as f:
            lire = csv.DictReader(f)
            for ligne in lire:
                if ligne['id'] == id:
                    # Afficher les informations actuelles du livre
                    print("Informations actuelles du livre : \n")
                    print(f"{'id':<20} {'title':<20} {'author':<20} {'genre':<20} ")
                    print("-" * 100)
                    print(f"{ligne['id']:<20} {ligne['title']:<20} {ligne['author']:<20} {ligne['genre']:<20}")


                    # Demander les nouvelles valeurs pour chaque champ
                    print("\nEntrez les nouvelles valeurs (laissez vide pour ne pas modifier) :")
                    nouveau_titre = input("Nouveau titre -> ").strip() or None
                    nouvel_auteur = input("Nouvel auteur -> ").strip() or None
                    nouveau_genre = input("Nouveau genre -> ").strip() or None

                    # Mettre à jour les champs si une nouvelle valeur est fournie
                    if nouveau_titre:
                        ligne['title'] = nouveau_titre
                    if nouvel_auteur:
                        ligne['author'] = nouvel_auteur
                    if nouveau_genre:
                        ligne['genre'] = nouveau_genre

                    trouve = True
                lignes.append(ligne)

        if not trouve:
            print(f"Livre avec l'ISBN {id} non trouvé.")
            id = input("Veuillez réessayer avec un autre ISBN  ->  ").strip()
            continue  # Revenir au début de la boucle pour réessayer

        # Réécrire le fichier CSV avec les modifications
        with open(BOOKS_CSV, 'w', newline='') as f:
            champs = ['id', 'title', 'author', 'genre']
            ecrivain = csv.DictWriter(f, fieldnames=champs)
            ecrivain.writeheader()
            ecrivain.writerows(lignes)

        print("Livre mis à jour avec succès.")
        return True


   
#foction de recherche titre
def search(valeur):
    # Vérifie si le fichier existe
    if not os.path.isfile(BOOKS_CSV):
        print("Aucun livre enregistré.")
        return

    while True:
        trouve = False

        # Ouvrir le fichier CSV en mode lecture
        with open(BOOKS_CSV, 'r', newline='') as f:
            lire = csv.DictReader(f)
            # Afficher l'en-tête du tableau
            print(f"{'id':<15} {'title':<20} {'author':<20} {'genre':<15} ")
            print("-" * 100)  

            # Champs à rechercher
            champs_recherche = ['title', 'author', 'genre']

            for ligne in lire:
                # Vérifier si la valeur est dans l'un des champs de recherche
                for champ in champs_recherche:
                    if valeur.lower() in ligne[champ].lower():  # Comparaison insensible à la casse
                        # Afficher les détails du livre
                        print(f"{ligne['id']:<15} {ligne['title']:<20} {ligne['author']:<20} {ligne['genre']:<15}")
                        trouve = True

            if trouve:
                break  # Sortir de la boucle si un livre est trouvé

            print(f"Aucun livre trouvé contenant '{valeur}' dans le titre, l'auteur ou le genre.")
            valeur = input("Veuillez insérer le nom d'un autre titre, un auteur ou un genre (ou appuyez sur Entrée pour quitter) : ").strip()

            # Sortir de la boucle si l'utilisateur appuie sur Entrée sans saisir de valeur
            if not valeur:
                break

    

#fonction de suppression par id
def sup(id):
    # Vérifie si le fichier existe
    if not os.path.isfile(BOOKS_CSV):
        print("Aucun livre enregistré.")
        return

    while True:
        trouve = False
        lignes = []

        # Lire le fichier CSV
        with open(BOOKS_CSV, 'r', newline='') as f:
            lire = csv.DictReader(f)
            for ligne in lire:
                if ligne['id'] == id:
                    trouve = True  # Marquer que le livre a été trouvé
                else:
                    lignes.append(ligne)  # Ajouter la ligne à la liste si l'ISBN ne correspond pas

        if not trouve:
            print(f"Livre avec l'ISBN {id} non trouvé.")
            id = input("Veuillez réessayer avec un autre ISBN (ou appuyez sur Entrée pour quitter) : ").strip()
            continue  # Revenir au début de la boucle pour réessayer

        # Réécrire le fichier CSV avec les lignes restantes
        with open(BOOKS_CSV, 'w', newline='') as f:
            champs = ['id', 'title', 'author', 'genre']
            ecrivain = csv.DictWriter(f, fieldnames=champs)
            ecrivain.writeheader()
            ecrivain.writerows(lignes)

        print("Livre supprimé avec succès.")
        return True





