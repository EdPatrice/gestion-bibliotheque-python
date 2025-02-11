import json
import fonctions.util as util
import os

files = util.read_json("config.json")

class Utilisateur:
    def __init__(self, id_utilisateur, prenom, nom, contact):
        # Initialiser les attributs de l'utilisateur
        self.id_utilisateur = id_utilisateur
        self.prenom = prenom
        self.nom = nom
        self.nom_complet = f"{self.prenom} {self.nom}"
        self.contact = contact
        self.emprunts = []  # Liste pour suivre les emprunts de l'utilisateur

    def __str__(self):        
        return "Nom:\t\t{} \nPrenom:\t\t{} \nContact:\t{}".format(self.nom, self.prenom, self.contact)        
    
class Gestion_Utilisateurs: 

    def __init__(self):
        self.users: list[Utilisateur] = []
    
    @classmethod
    # Generer l'identifiant de l'utilisateur
    def generate_id(self, user: Utilisateur) -> str:
        import random
        first_letter = user.nom[0].upper()
        last_letter = user.prenom[0].upper()
        random_digits = random.randint(100000, 999999)
        user_id = f"U{first_letter}{last_letter}{random_digits}"
        if self.get_user_info(user_id)[0] != None:
            return self.generate_id(user)
        return user_id

    @classmethod
    def afficher_utilisateurs(self, get_all_detail: bool= 0):
        with open(files["USERS_CSV"], 'r') as f:
            utilisateurs = f.readlines()        
        for utilisateur in utilisateurs[1:]:
            utilisateur = utilisateur.replace('\n', '').split(", ")
            if not get_all_detail:
                print("ID:", utilisateur[0], "\tNom:", utilisateur[1], utilisateur[2])
            else:
                print("ID:", utilisateur[0], "\tPrenom:", utilisateur[1], "\t\tNom:", utilisateur[2], "\t\t\tContact:", utilisateur[3])            

    @classmethod
    def write_headers():
        with open(files["USERS_CSV"], 'w') as f: 
            f.write("Id, Nom, Prenom, Contact\n")

    @classmethod
    def enregistrer_utilisateur(self, user: Utilisateur):
        import os
        if os.path.getsize(files["USERS_CSV"]) == 0:
            self.write_headers()            
        with open(files["USERS_CSV"], 'a') as f:
            f.write(f"{user.id_utilisateur}, {user.nom}, {user.prenom}, {user.contact}\n")

    @classmethod
    def get_user_info(self, user_id: str) -> tuple[Utilisateur, int]:
        user_id = user_id.strip()
        utilisateur_existe = False
        with open(files["USERS_CSV"], 'r') as f: 
            users = f.readlines()
        index_utilisateur = 0
        for user in users[1:]: 
            user = user.replace('\n', '').split(", ")
            if user[0] == user_id:
                utilisateur_existe = True
                prenom = user[1]
                nom = user[2]
                contact = user[3]
                utilisateur = Utilisateur(user_id, prenom, nom, contact)
            index_utilisateur += 1
        if utilisateur_existe:
            return utilisateur, index_utilisateur
        else: 
            return None, None

    @classmethod
    def modifier_utilisateur(self, user_id: str):
        user, index_utilisateur = self.get_user_info(user_id)
        if user and index_utilisateur: 
            print('Utilisateur a modifier: \n')
            print("Nom:\t\t", user.nom)
            print("Prenom:\t\t", user.prenom)
            print("Contact:\t", user.contact, '\n')
            nouveau_nom = input("\nEntrez le nouveau nom (laissez vide pour ne pas changer) -> ")
            nouveau_prenom = input("\nEntrez le nouveau prénom (laissez vide pour ne pas changer) -> ")
            nouveau_contact = input("\nEntrez le nouveau contact (laissez vide pour ne pas changer) -> ")
            if nouveau_nom:
                user.nom = nouveau_nom
            if nouveau_prenom:
                user.prenom = nouveau_prenom
            if nouveau_contact:
                user.contact = nouveau_contact

            # effectuer les modifications
            with open(files["USERS_CSV"], 'r') as f:
                utilisateurs = f.readlines()
            utilisateur_a_modifier = utilisateurs[index_utilisateur]
            utilisateur_a_modifier = utilisateur_a_modifier.replace('\n', '').split(", ")
            utilisateur_a_modifier[1] = user.prenom
            utilisateur_a_modifier[2] = user.nom
            utilisateur_a_modifier[3] = user.contact
            utilisateurs[index_utilisateur] = f"{utilisateur_a_modifier[0]}, {utilisateur_a_modifier[1]}, {utilisateur_a_modifier[2]}, {utilisateur_a_modifier[3]}\n"

            # ecrire les donnees modifiees dans le fichier
            with open(files["USERS_CSV"], 'w') as f:
                f.writelines(utilisateurs)

            util.clear_screen()
            print("\nModifications effectuees avec succes. \n\nLes nouvelles donnees sont: \n")
            print("Nom:\t\t", user.nom)
            print("Prenom:\t\t", user.prenom)
            print("Contact:\t", user.contact, '\n')
   
    @classmethod
    def supprimer_utilisateur(self, user_id: str):
        user, index_utilisateur = self.get_user_info(user_id)

        if user and index_utilisateur:
            util.clear_screen()
            print("Utilisateur a supprimer: \n")
            print(user)
            confirmation = input("\nEtes-vous sur de vouloir supprimer cet utilisateur? (O/N) -> ")
            # controle de saisie
            while not util.message_de_confirmation_valide(confirmation, 'O', 'N'):
                confirmation = input("Veuillez repondre par O ou N -> ")
            if confirmation.lower() == 'o': # suppression de l'utilisateur
                with open(files["USERS_CSV"], 'r') as f:
                    utilisateurs = f.readlines()
                utilisateurs.pop(index_utilisateur)
                with open(files["USERS_CSV"], 'w') as f:
                    f.writelines(utilisateurs)
                print("\nUtilisateur supprime avec succes.")
            else:
                print("\nSuppression annulee.")    

class Livre: 
    def __init__(self, id, title, author, genre):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre

    def __str__(self):
        return f"id: {self.id}\ntitle: {self.title}\nauthor: {self.author}\ngenre: {self.genre}"

class Gestion_Livres:
    def __init__(self):
        self.books: list[Livre] = []

    def ajouter(self, id, title, author, genre):
        book = Livre(id, title, author, genre)
        self.books.append(book)
    
    @classmethod
    def get_book_info(self, book_id: str) -> tuple[Livre, int]:
        book_exists = False
        with open(files["BOOKS_CSV"], 'r') as f: 
            books = f.readlines()
        index_livre = 1
        for book in books[1:]:
            book = book.replace('\n', '').split(",")
            if book[0] == book_id:
                book_exists = True
                book_title = book[1]
                book_author = book[2]
                book_genre = book[3]
                livre = Livre(book_id, book_title, book_author, book_genre)
            index_livre += 1
        if book_exists:
            return livre, index_livre
        else:
            return None, None

    @classmethod
    def list_books(self, get_all_details: bool= 0):
        with open(files["BOOKS_CSV"], 'r') as f:
            books = f.readlines()        
        for book in books[1:]: 
            book = book.split(',')
            if not get_all_details: 
                print("ID:", book[0], "\tTitle:", book[1])
            else:
                print("ID:", book[0], "\tTitle:", book[1], "Author:", book[2], "Genre:", book[3])

    @classmethod
    def modifier_livre(self, book_id: str, new_title: str = None, new_author: str = None, new_genre: str = None):
        book, index = self.get_book_info(book_id)
        if book:
            if new_title:
                book.title = new_title
            if new_author:
                book.author = new_author
            if new_genre:
                book.genre = new_genre
            self.books[index] = book
            print("\nModifications effectuées avec succès.\n")
        else:
            print("\nLivre non trouvé.\n")

    @classmethod
    def supprimer_livre(self, book_id: str):
        book, index = self.get_book_info(book_id)
        if book:
            self.books.pop(index)
            print("\nLivre supprimé avec succès.\n")
        else:
            print("\nLivre non trouvé.\n")
              

class Emprunt: 

    def __init__(self, id, id_livre, id_utilisateur, date_emprunt, date_retour_prevue, date_retour = None):
        self.id = id
        self.livre = id_livre
        self.utilisateur = id_utilisateur
        self.date_emprunt = date_emprunt
        self.date_retour_prevue = date_retour_prevue
        self.date_retour = date_retour

    def __str__(self):
        user, _ = Gestion_Utilisateurs.get_user_info(self.utilisateur)
        book, _ = Gestion_Livres.get_book_info(self.livre)
        if user and book:
            return f"ID: \t\t\t{self.id}\nLivre: \t\t\t{book.title}\nAuteur: \t\t{book.author}\nDate Emprunt: \t\t{self.date_emprunt}\nDate Retour Prevue: \t{self.date_retour_prevue}\nDate Retour: \t\t{self.date_retour}\n"        
        else: 
            return ""
    
class Gestion_Emprunt:

    def __init__(self):
        self.emprunts: list[Emprunt] = []   

    @classmethod
    def write_headers():
        with open(files["EMPRUNTS_CSV"], 'w') as f: 
            f.write("ID Emprunt, ID Utilisateur, ID Livre, Date Emprunt, Date Retour Prevue, Date Retour\n")

    @classmethod
    def get_emprunt_info(self, id_emprunt: str) -> tuple[Emprunt, int, Utilisateur]:
        emprunt_exists = False
        with open(files["EMPRUNTS_CSV"], 'r') as f:
            emprunts = f.readlines()
        index_emprunt = 0
        for emprunt in emprunts: 
            emprunt = emprunt.replace('\n', '').split(", ")
            if emprunt[0] == id_emprunt:
                emprunt_exists = True
                emprunt_id_user = emprunt[1]
                emprunt_id_book = emprunt[2]
                emprunt_date = emprunt[3]
                emprunt_date_retour_prevue = emprunt[4]
                emprunt_date_retour = emprunt[5]
                emprunt = Emprunt(id_emprunt, emprunt_id_book, emprunt_id_user, emprunt_date, emprunt_date_retour_prevue, emprunt_date_retour)
                user, _ = Gestion_Utilisateurs.get_user_info(emprunt_id_user)
            
        if emprunt_exists:
            return emprunt, index_emprunt, user
        else:
            return None
        
    @classmethod
    def get_emprunts_utilisateur(self, user_id: str) -> list[Emprunt]:
        emprunts = []
        with open(files["EMPRUNTS_CSV"], 'r') as f:
            emprunts_csv = f.readlines()
        for emprunt in emprunts_csv[1:]:
            emprunt = emprunt.replace('\n', '').split(", ")
            if emprunt[1] == user_id:
                emprunt = Emprunt(emprunt[0], emprunt[2], emprunt[1], emprunt[3], emprunt[4], emprunt[5])
                emprunts.append(emprunt)
        return emprunts
        
        
    @classmethod
    def enregistrement_emprunt(self):
        # insertion du livre
        print("Liste des livres disponibles: \n")
        Gestion_Livres.list_books()  
        book_id = input("\nVeuillez inserer l'identifiant du livre qui sera emprunte: \n-> ")
        # controle de saisie ID ... 
        while Gestion_Livres.get_book_info(book_id)[0] == None:
            book_id = input("\nErreur, veuillez inserer l'identifiant d'un livre existant dans la base de donnees -> ")
        book, _ = Gestion_Livres.get_book_info(book_id)

        # insertion de l'utilisateur
        util.clear_screen()
        print("Liste des utilisateurs: \n")
        Gestion_Utilisateurs.afficher_utilisateurs()
        user_id = input("\nVeuillez inserer l'identifiant de l'emprunteur: \n-> ")
        # controle de saisie ID ... 
        while Gestion_Utilisateurs.get_user_info(user_id)[0] == None:
            user_id = input("\nErreur, veuillez inserer l'identifiant d'un utilisateur existant dans la base de donnees -> ")
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
                # f.write("ID Emprunt, ID Utilisateur, ID Livre, Date Emprunt, Date Retour Prevue, Date Retour\n")
                self.write_headers()
            line = f"{emprunt.id}, {emprunt.utilisateur}, {emprunt.livre}, {emprunt.date_emprunt}, {emprunt.date_retour_prevue}, {emprunt.date_retour}\n"
            f.write(line)

    @classmethod
    def enregistrement_retour(self):
        print("Liste des emprunts qui n'ont pas encore ete retournes: \n")
        emprunts_sans_date_retour = 0
        with open(files["EMPRUNTS_CSV"], 'r') as f:
            emprunts = f.readlines()
        for emprunt in emprunts[1:]:
            emprunt = emprunt.replace('\n', '').split(', ')
            if emprunt[5] == "None":
                emprunts_sans_date_retour += 1
                user, _ = Gestion_Utilisateurs.get_user_info(emprunt[1])
                book, _ = Gestion_Livres.get_book_info(emprunt[2])
                if user and book:
                    print(f"\n********************** {emprunts_sans_date_retour} ***************************\n")
                    print("Date Emprunt:", emprunt[3], "\tDate Retour Prevue:", emprunt[4], "\nID emprunt:", emprunt[0])
                    print( "Utilisateur:", user.nom_complet, "\nLivre:", book.title)                            
                    
        if emprunts_sans_date_retour != 0:  # cas ou il y a des emprunts sans date de retour                           
            id_emprunt = input("\nVeuillez inserer l'identifiant de l'emprunt a mettre a jour: \n-> ")                
            #controle de saisie id
            while (Gestion_Emprunt.get_emprunt_info(id_emprunt) == None) or (Gestion_Emprunt.get_emprunt_info(id_emprunt)[0].date_retour != "None"):
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

    @classmethod
    def lister_retards_sur_retours(self):
        print("Listes des retards sur paiement: \n")
        date_du_jour = str(util.get_date().date())
        with open(files["EMPRUNTS_CSV"], 'r') as f:
            emprunts = f.readlines()                
        i=0                
        for emprunt in emprunts[1:]:
            emprunt = emprunt.replace('\n', '').split(', ')
            user, _ = Gestion_Utilisateurs.get_user_info(emprunt[1])
            book, _ = Gestion_Livres.get_book_info(emprunt[2])
            if date_du_jour > emprunt[4] and user and book:                            
                print("Date Emprunt:", emprunt[3], "\tDate Retour Prevue:", emprunt[4], "\t\tUtilisateur:", user.nom_complet, "\tLivre:", book.title)                          
                i+=1
        if i == 0:
            util.clear_screen()
            print("\nAucun emprunt n'est a terme, verifiez plus tard.")

