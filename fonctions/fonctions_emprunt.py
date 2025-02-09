import fonctions.util as util
import os
from classes import Utilisateur, Gestion_Utilisateurs, Livre, Gestion_Livres, Emprunt, Gestion_Emprunt

files = util.read_json("config.json")

def menu_emprunt():       
        util.clear_screen()
        choix = input("Veuillez inserer le numero correspondant a l'option desiree: \n\n1. Enregistrement d'un emprunt. \n2. Enregistrer un retour. \n3. Voir les retards de retour. \n\n0. Retour. \n\n-> ")
        while util.choix_valide(choix, 0, 3) != True:
                choix = input("Saisie incorrecte, reesayez: ")  
        choix = int(choix) 

        match choix:             
            case 1:                             # enregistrer un emprunt
                util.clear_screen()
                enregistrement_emprunt()                
                util.wait()

            case 2:                 # enregistrer un retour
                # lister les emprunts sans date de retour et choisir l'emprunt a mettre a jour
                util.clear_screen()
                enregistrement_retour()                

            case 3:             # voir les retards sur retour
                util.clear_screen()
                lister_retards_sur_retours()
                util.wait()    

def enregistrement_emprunt():
    # insertion du livre
    print("Liste des livres disponibles: \n")
    Gestion_Livres.list_books()  

    book_id = input("\nVeuillez inserer l'identifiant du livre qui sera emprunte: \n-> ")
    # controle de saisie ID ... 
    while Gestion_Livres.get_book_info(book_id) == None:
        book_id = input("\nErreur, veuillez inserer l'identifiant d'un livre existant dans la base de donnees: ")
    book, _ = Gestion_Livres.get_book_info(book_id)

    # insertion de l'utilisateur
    util.clear_screen()
    print("Liste des utilisateurs: \n")
    Gestion_Utilisateurs.afficher_utilisateurs()
    user_id = input("\nVeuillez inserer l'identifiant de l'emprunteur: \n-> ")
    # controle de saisie ID ... 
    while Gestion_Utilisateurs.get_user_info(user_id) == None:
        user_id = input("\nErreur, veuillez inserer l'identifiant d'un utilisateur existant dans la base de donnees: ")
    user, _ = Gestion_Utilisateurs.get_user_info(user_id)                                

    util.clear_screen()
    date_emprunt = str(util.get_date().date())
    date_retour_prevue = str(util.add_days_to_date(date_emprunt, 15).date())
    id_emprunt = util.get_last_identity_id(files["EMPRUNTS_CSV"]) + 1
    emprunt = Emprunt(id_emprunt, book_id, user_id, date_emprunt, date_retour_prevue)                
    print("\nEmprunt enregistre avec succes: ", end="\n\n")
    print("ID: \t\t\t", emprunt.id, "\nUtilisateur:\t\t", user.nom_complet, "\nLivre:\t\t\t", book.title, "\nDate Emprunt:\t\t", emprunt.date_emprunt, "\nDate Retour Prevue:\t", emprunt.date_retour_prevue, "\nDate Retour:\t\t", emprunt.date_retour)                
    
    # Enregistrement de l'emprunt dans la base de donnees: 
    with open(files["EMPRUNTS_CSV"], 'a') as f:
        if os.path.getsize(files["EMPRUNTS_CSV"]) == 0:
            f.write("ID Emprunt, ID Utilisateur, ID Livre, Date Emprunt, Date Retour Prevue, Date Retour\n")
        line = f"{emprunt.id}, {emprunt.utilisateur}, {emprunt.livre}, {emprunt.date_emprunt}, {emprunt.date_retour_prevue}, {emprunt.date_retour}\n"
        f.write(line)

def enregistrement_retour():
    emprunts_sans_date_retour = 0
    with open(files["EMPRUNTS_CSV"], 'r') as f:
        emprunts = f.readlines()
    for emprunt in emprunts[1:]:
        emprunt = emprunt.replace('\n', '').split(', ')
        if emprunt[5] == "None":
            emprunts_sans_date_retour += 1
            print("ID emprunt:", emprunt[0], "\tID Utilisateur:", emprunt[1], "\tID Livre:", emprunt[2], "\tDate Emprunt:", emprunt[3], "\tDate Retour Prevue:", emprunt[4], "\tDate Retour:", emprunt[5])                            
                
    if emprunts_sans_date_retour != 0:  # cas ou il y a des emprunts sans date de retour                           
        id_emprunt = input("\nVeuillez inserer l'identifiant de l'emprunt a mettre a jour: \n-> ")                
        #controle de saisie id
        while (Gestion_Emprunt.get_emprunt_info(id_emprunt) == None) or (Gestion_Emprunt.get_emprunt_info(id_emprunt)[4] != "None"):
            id_emprunt = input("Veuillez inserer l'identifiant d'un emprunt faisant partie de la liste: ")

        # inserer la date de retour
        date_retour = input("\nVeuillez inserer la date de retour (format: yyyy-mm-dd): ")
        while util.date_valide(date_retour) != True: 
            date_retour = input("Veuillez inserer une date valide: ")
        
        # Recherche de la ligne a modifier:
        i = 1                                   # non 0 car on evite la premiere ligne des titres
        with open(files["EMPRUNTS_CSV"], 'r') as f:
            emprunts = f.readlines()                    
        for emprunt in emprunts[1:]:
            emprunt = emprunt.replace('\n', '').split(', ')
            if emprunt[0] == id_emprunt:
                date_retour_prevue = emprunt[4]
                emprunt[5] = date_retour  
                emprunts[i] = f"{emprunt[0]}, {emprunt[1]}, {emprunt[2]}, {emprunt[3]}, {emprunt[4]}, {emprunt[5]}\n"
                break
            i+=1         
        with open(files["EMPRUNTS_CSV"], 'w') as f:
            f.writelines(emprunts)              # ecrire les donnees modifiees dans le fichier
                        
        print("\nRetour enregistre", end='')
        if date_retour > date_retour_prevue:
            print(" avec", util.days_diff_between_dates(date_retour, date_retour_prevue), "jour(s) de retard", end='')
        print(".")
        util.wait()

    else:       # cas ou il n'y a pas d'emprunt sans date de retour
        print("Tous les emprunts ont deja ete retournes.")
        util.wait()

def lister_retards_sur_retours():
    print("Listes des retards sur paiement: \n")
    date_du_jour = str(util.get_date().date())
    with open(files["EMPRUNTS_CSV"], 'r') as f:
        emprunts = f.readlines()                
    i=0                
    for emprunt in emprunts[1:]:
        emprunt = emprunt.replace('\n', '').split(', ')
        user, _ = Gestion_Utilisateurs.get_user_info(emprunt[1])
        book, _ = Gestion_Livres.get_book_info(emprunt[2])
        if date_du_jour > emprunt[4]:                            
            print("Date Emprunt:", emprunt[3], "\tDate Retour Prevue:", emprunt[4], "\t\tUtilisateur:", user.nom_complet, "\tLivre:", book.title)                          
            i+=1
    if i == 0:
        util.clear_screen()
        print("\nAucun emprunt n'est a terme, verifiez plus tard.")
