import csv
from datetime import datetime
from collections import defaultdict, Counter
# from fonctions import util
import fonctions.util as util

files = util.read_json("config.json")

def List_Book():
    
    with open(files["BOOKS_CSV"], 'r') as file:
        
        List = csv.DictReader(file)
        
        for count, line in enumerate(List, start=1):
            
            print(f"\n********************** Livre {count} ***************************\n")
            
            for key, value in line.items():
                print(f"{key} : {value}")
                
def search_user(id:str):
    
    with open(files["USERS_CSV"], 'r') as f:
                users = f.readlines()
                
                for user in users:
                    user = user.strip().split(', ')
                    if user[0] == id:
                        return user
                else:
                    return None
                
def search_book(id:str):
    
    with open(files["BOOKS_CSV"], 'r') as f:
                books = f.readlines()
                
                for book in books:
                    book = book.strip().split(', ')
                    if book[0] == id:
                        return book
                else:
                    return None


def History_Emprunt():

    with open(files["EMPRUNTS_CSV"], 'r') as file:
        reader = file.readlines()
        
    # Extraire les dates d'emprunt et de retour
    dates = []
    for line in reader[1:]:
        line = line.split(', ')
        
        date_emprunt = datetime.strptime(line[3], '%Y-%m-%d')
        date_retour = datetime.strptime(line[4], '%Y-%m-%d')
        
        dates.append((date_emprunt, 'Emprunt', line))
        dates.append((date_retour, 'Retour', line))
    
    # Trier les dates par ordre décroissant
    dates.sort(reverse=True, key=lambda x: x[0])
    
    # Afficher les dates triées
    
    print(f"\n********************** HISTORIQUE ***************************\n")

    for date, type_date, lines in dates:
        print(f"{date.strftime(('%Y-%m-%d'))}, Type: {type_date}")
        
        User_name = search_user(lines[1])
        Book_Title = search_book(lines[2])

        if type_date == 'Emprunt':
            print(f"  Nom Utilisateur: {User_name[1]}, Titre du livre: {Book_Title[1]}, Date Retour Prévue: {lines[4]}")
        
        else:
            print(f"  Nom Utilisateur: {User_name[1]}, Titre du livre: {Book_Title[1]}")
        print()



# Fonction pour obtenir les genres les plus empruntés
def genres_plus_empruntes():
    
    counter_genres = defaultdict(int)

 
# Parcourir les emprunts pour compter les livres
    with open(files["EMPRUNTS_CSV"], 'r') as file:
        reader = file.readlines()

        for emprunt in reader:
            emprunt = emprunt.strip().split(', ')
            if len(emprunt) >= 3: 
                id_book = emprunt[2] 

                # Trouver le livre correspondant 
                with open(files["BOOKS_CSV"], 'r') as file:
                    books = file.readlines()
                    
                    for book in books:
                        book = book.strip().split(', ')
                        
                        if len(book) >= 4 and book[0] == id_book: 
                            genre = book[3]
                            counter_genres[genre] += 1
                            break 

    # Trouver et retourner les 3 genres les plus empruntés
    most_borrowed = Counter(counter_genres).most_common(3) 
    return most_borrowed


# Fonction pour afficher les livres associés aux genres les plus empruntés
def afficher_livres_par_genre(most_borrowed):
    
    # Charger les livres
    with open(files["BOOKS_CSV"], 'r') as file:
        books = [book.strip().split(', ') for book in file.readlines()]

    # Charger les emprunts
    with open(files["EMPRUNTS_CSV"], 'r') as file:
        emprunts = [emprunt.strip().split(', ') for emprunt in file.readlines()]

    print(f"\n********************** LES GENRES LES PLUS EMPRUNTES ***************************\n")

    for genre, count in most_borrowed:
        print(f"Genre: {genre} (emprunté {count} fois)")
        print("Livres empruntés associés :")

        # Livres correspondants à ce genre
        for book in books:
            if len(book) >= 4 and book[3] == genre:
                id_livre = book[0]

                # Vérification si ce livre a été emprunté
                for emprunt in emprunts:
                    if len(emprunt) >= 3 and emprunt[2] == id_livre:
                        print(f"  - Titre: {book[1]}, Auteur: {book[2]}, ID: {book[0]}")
                        break  
        print("\n")

def menu_statistiques():       
        # util.clear_screen()
        
        choix = input("Veuillez inserer le numero correspondant a l'option desiree: \n\n1. Rapport des Livres disponibles et empruntes.\n2. Historique des emprunts et retours. \n3. Rapport des trois(3) genres de livres les plus empruntes. \n\n0. Retour. \n\n-> ")
        while util.choix_valide(choix, 0, 3) != True:
                choix = input("Saisie incorrecte, reesayez: ")  
        choix = int(choix) 

        match choix:             
            case 1:                      # rapport de livres dispo et empruntes
                util.clear_screen()
                List_Book()                
                util.wait()

            case 2:                 # Historique des emprunts et retours
                util.clear_screen()
                History_Emprunt()                
                util.wait()
                
            case 3:             # Rapports sur les genres les plus empruntes
                util.clear_screen()
                most_borrowed = genres_plus_empruntes()
                afficher_livres_par_genre(most_borrowed)                
                util.wait() 
