import fonctions.util as util
import os
from classes import User, ManageUser, Book, ManageBooks, Emprunt, Gestion_emprunt

def insertion_emprunt():
        EMPRUNT_CSV = "./database/emprunts.csv"
        BOOKS_CSV = "./database/livres.csv"
        USERS_CSV = "./database/utilisateurs.csv"

        # gestionnaire_livres = ManageBooks()

        util.clear_screen()

        choix = input("Veuillez inserer le numero correspondant a l'option desiree: \n\n1. Enregistrement d'un emprunt. \n2. Enregistrer un retour. \n3. Voir les retards de retour. \n\n0. Retour. \n\n-> ")
        while util.choix_valide(choix, 0, 3) != True:
                choix = ("Saisie incorrecte, reesayez: ")  
        choix = int(choix)      
        match choix: 
            case 1:                             # enregistrer un emprunt
                util.clear_screen()
                print("Liste des livres disponibles: \n")
                ManageBooks.list_books(BOOKS_CSV, 0)  
                book_id = input("\nVeuillez inserer l'identifiant du livre qui sera emprunte: \n-> ")
                # controle de saisie ID ... 
                while get_book_info(BOOKS_CSV, book_id) == None:
                    book_id = input("\nErreur, veuillez inserer l'identifiant d'un livre existant dans la base de donnees: ")
                book_title, _, _ = get_book_info(BOOKS_CSV, book_id)

                util.clear_screen()
                user_manager = ManageUser()
                user_manager.list_users(USERS_CSV)
                user_id = input("\nVeuillez inserer l'identifiant de l'emprunteur: \n-> ")
                # controle de saisie ID ... 
                while get_user_info(USERS_CSV, user_id) == None:
                    user_id = input("\nErreur, veuillez inserer l'identifiant d'un utilisateur existant dans la base de donnees: ")
                user_name, _ = get_user_info(USERS_CSV, user_id)
                

                util.clear_screen()
                date_emprunt = str(util.get_date().date())
                date_retour_prevue = str(util.add_days_to_date(date_emprunt, 15).date())

                id_emprunt = util.get_last_identity_id(EMPRUNT_CSV) + 1

                emprunt = Emprunt(id_emprunt, book_id, user_id, date_emprunt, date_retour_prevue)
                
                print("\nEmprunt enregistre avec succes: ", end="\n\n")
                print("ID: \t\t\t", emprunt.id, "\nUtilisateur:\t\t", user_name, "\nLivre:\t\t\t", book_title, "\nDate Emprunt:\t\t", emprunt.date_emprunt, "\nDate Retour Prevue:\t", emprunt.date_retour_prevue, "\nDate Retour:\t\t", emprunt.date_retour)                
                
                # Enregistrement de l'emprunt dans la base de donnees: 
                with open(EMPRUNT_CSV, 'a') as f:
                    if os.path.getsize(EMPRUNT_CSV) == 0:
                        f.write("ID Emprunt, ID Utilisateur, ID Livre, Date Emprunt, Date Retour Prevue, Date Retour\n")
                    line = f"{emprunt.id}, {emprunt.utilisateur}, {emprunt.livre}, {emprunt.date_emprunt}, {emprunt.date_retour_prevue}, {emprunt.date_retour}\n"
                    f.write(line)
                
                util.wait()

            case 2:                 # enregistrer un retour
                # lister les emprunts sans date de retour et choisir l'emprunt a mettre a jour
                util.clear_screen()
                emprunts_sans_date_retour = 0
                with open(EMPRUNT_CSV, 'r') as f:
                    emprunts = f.readlines()
                for emprunt in emprunts[1:]:
                    emprunt = emprunt.replace('\n', '').split(', ')
                    if emprunt[5] == "None":
                        emprunts_sans_date_retour += 1
                        print("ID emprunt:", emprunt[0], "\tID Utilisateur:", emprunt[1], "\tID Livre:", emprunt[2], "\tDate Emprunt:", emprunt[3], "\tDate Retour Prevue:", emprunt[4], "\tDate Retour:", emprunt[5])                            
                            
                if emprunts_sans_date_retour != 0:  # cas ou il y a des emprunts sans date de retour                           
                    id_emprunt = input("\nVeuillez inserer l'identifiant de l'emprunt a mettre a jour: \n-> ")                
                    #controle de saisie id
                    while (get_emprunt_info(EMPRUNT_CSV, id_emprunt) == None) or (get_emprunt_info(EMPRUNT_CSV, id_emprunt)[4] != "None"):
                        id_emprunt = input("Veuillez inserer l'identifiant d'un emprunt faisant partie de la liste: ")

                    # inserer la date de retour
                    date_retour = input("\nVeuillez inserer la date de retour (format: yyyy-mm-dd): ")
                    while util.date_valide(date_retour) != True: 
                        date_retour = input("Veuillez inserer une date valide: ")
                    
                    # Recherche de la ligne a modifier:
                    i = 1                                   # non 0 car on evite la premiere ligne des titres
                    with open(EMPRUNT_CSV, 'r') as f:
                        emprunts = f.readlines()                    
                    for emprunt in emprunts[1:]:
                        emprunt = emprunt.replace('\n', '').split(', ')
                        if emprunt[0] == id_emprunt:
                            date_retour_prevue = emprunt[4]
                            emprunt[5] = date_retour  
                            emprunts[i] = f"{emprunt[0]}, {emprunt[1]}, {emprunt[2]}, {emprunt[3]}, {emprunt[4]}, {emprunt[5]}\n"
                            break
                        i+=1         
                    with open(EMPRUNT_CSV, 'w') as f:
                        f.writelines(emprunts)              # ecrire les donnees modifiees dans le fichier
                                    
                    print("\nRetour enregistre", end='')
                    if date_retour > date_retour_prevue:
                        print(" avec", util.days_diff_between_dates(date_retour, date_retour_prevue), "jour(s) de retard", end='')
                    print(".")
                    util.wait()

                else:       # cas ou il n'y a pas d'emprunt sans date de retour
                    print("Tous les emprunts ont deja ete retournes.")
                    util.wait()

            case 3:             # voir les retards sur retour
                date_du_jour = str(util.get_date().date())
                with open(EMPRUNT_CSV, 'r') as f:
                    emprunts = f.readlines()
                i=0                
                for emprunt in emprunts[1:]:
                    emprunt = emprunt.replace('\n', '').split(', ')
                    if date_du_jour > emprunt[4]:                            
                        print("ID emprunt:", emprunt[0], "\tID Utilisateur:", emprunt[1], "\tID Livre:", emprunt[2], "\tDate Emprunt:", emprunt[3], "\tDate Retour Prevue:", emprunt[4], "\tDate Retour:", emprunt[5])                          
                        i+=1
                if i == 0:
                    print("\nAucun emprunt n'est a terme, verifiez plus tard.")
                util.wait()
                    

def get_user_info(USERS_CSV: str, user_id: str):
    user_exists = False

    with open(USERS_CSV, 'r') as f: 
        users = f.readlines()
    for user in users: 
        user = user.split(", ")
        if user[0] == user_id:
            user_exists = True
            user_name = user[1]
            user_email = user[2]
    if user_exists:
        return user_name, user_email
    else: 
        return None
    
def get_book_info(BOOKS_CSV: str, book_id: str):
    book_exists = False

    with open(BOOKS_CSV, 'r') as f: 
        books = f.readlines()
    for book in books:
        book = book.split(", ")
        if book[0] == book_id:
            book_exists = True
            book_title = book[1]
            book_author = book[2]
            book_genre = book[3]
    if book_exists:
        return book_title, book_author, book_genre
    else:
        return None
    
def get_emprunt_info(EMPRUNTS_CSV: str, id_emprunt: str):
    emprunt_exists = False

    with open(EMPRUNTS_CSV, 'r') as f:
        emprunts = f.readlines()
    for emprunt in emprunts: 
        emprunt = emprunt.replace('\n', '').split(", ")
        if emprunt[0] == id_emprunt:
            emprunt_exists = True
            emprunt_id_user = emprunt[1]
            emprunt_id_book = emprunt[2]
            emprunt_date = emprunt[3]
            emprunt_date_retour_prevue = emprunt[4]
            emprunt_date_retour = emprunt[5]
    if emprunt_exists:
        return emprunt_id_user, emprunt_id_book, emprunt_date, emprunt_date_retour_prevue, emprunt_date_retour
    else:
        return None
