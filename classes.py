import json
import fonctions.util as util

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

    # def __str__(self):
    #     return "ID: {} - {}".format(self.id, self.nom)
    
class Gestion_Utilisateurs: 

    def __init__(self):
        self.users: list[Utilisateur] = []

    @classmethod
    def afficher_utilisateurs(self, get_all_detail: bool= 0):
        with open(files["USERS_CSV"], 'r') as f:
            utilisateurs = f.readlines()        
        for utilisateur in utilisateurs[1:]:
            utilisateur = utilisateur.split(", ")
            if not get_all_detail:
                print("ID:", utilisateur[0], "\t Nom:", utilisateur[1], utilisateur[2])
            else:
                print("ID:", utilisateur[0], "\tPrenom:", utilisateur[1], "\tNom:", utilisateur[2], "\tContact:", utilisateur[3])            

    @classmethod
    def write_headers():
        with open(files["USERS_CSV"], 'w') as f: 
            f.write("Id, Nom, Prenom, Contact")

    def enregistrer_utilisateur(self):
        import os
        if os.path.getsize(files["USERS_CSV"]) == 0:
            self.write_headers()            
        with open(files["USERS_CSV"], 'w') as f:
            f.write(f"{self.id_utilisateur}, {self.nom}, {self.prenom}, {self.contact} \n")

    @classmethod
    def get_user_info(self, user_id: str) -> tuple[Utilisateur, int]:
        utilisateur_existe = False
        with open(files["USERS_CSV"], 'r') as f: 
            users = f.readlines()
        index_utilisateur = 0
        for user in users: 
            user = user.replace('\n', '').split(", ")
            if user[0] == user_id:
                utilisateur_existe = True
                id_utilisateur = user_id
                prenom = user[1]
                nom = user[2]
                contact = user[3]
                utilisateur = Utilisateur(id_utilisateur, prenom, nom, contact)
            index_utilisateur += 1
        if utilisateur_existe:
            return utilisateur, index_utilisateur
        else: 
            return None

    @classmethod
    def modifier_utilisateur(self):
        self, index_utilisateur = self.get_user_info(files["USERS_CSV"], self.id_utilisateur)
        if self != None: 
            print('Utilisateur a modifier: \n')
            print("Nom:\t", self.nom)
            print("Prenom:\t", self.prenom)
            print("Contact:\t", self.contact, '\n')
            nouveau_nom = input("Entrer un nouveau nom (Pressez ENTRER pour n'effectuer aucune modification): ")
            nouveau_prenom = input("Entrer un nouveau prenom (Pressez ENTRER pour n'effectuer aucune modification): ")
            nouveau_contact = input("Entrer un nouvel email (Pressez ENTRER pour n'effectuer aucune modification): ")
            self.nom = nouveau_nom
            self.prenom = nouveau_prenom
            self.contact = nouveau_contact

            # effectuer les modifications
            with open(files["USERS_CSV"], 'r') as f:
                utilisateurs = f.readlines()
            utilisateur_a_modifier = utilisateurs[index_utilisateur]
            utilisateur_a_modifier[1] = self.nom
            utilisateur_a_modifier[2] = self.prenom
            utilisateur_a_modifier[3] = self.contact
            utilisateurs[index_utilisateur] = utilisateur_a_modifier

            # ecrire les donnees modifiees dans le fichier
            with open(files["USERS_CSV"], 'w') as f:
                f.writelines(utilisateurs)

            print("\nModifications effectuees avec succes. \nLes nouvelles donnees sont: \n")
            print("Nom:\t", self.nom)
            print("Prenom:\t", self.prenom)
            print("Contact:\t", self.contact, '\n')
   
class Livre: 
    
    def __init__(self, id, title, author, genre):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre    

class Gestion_Livres: 
    
    def __init__(self):
        self.books: list[Livre] = []

    def add_book(self, books: list[Livre]):
        for book in books: 
            self.books.append(book)

    def search_book(self, id) -> Livre: 
        for book in self.books: 
            if book.id == id: 
                return book
        return None
    
    @classmethod
    def get_book_info(self, book_id: str) -> tuple[Livre, int]:
        book_exists = False
        with open(files["BOOKS_CSV"], 'r') as f: 
            books = f.readlines()
        index_livre = 0
        for book in books:
            book = book.replace('\n', '').split(", ")
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
            return None
    
    @classmethod
    def list_books(self, get_all_details: bool= 0):
        with open(files["BOOKS_CSV"], 'r') as f:
            books = f.readlines()        
        for book in books[1:]: 
            book = book.split(', ')
            if not get_all_details: 
                print("ID:", book[0], "\tTitle:", book[1])
            else:
                print("ID:", book[0], "\tTitle:", book[1], "Author:", book[2], "Genre:", book[3])                

class Emprunt: 

    def __init__(self, id, livre, utilisateur, date_emprunt, date_retour_prevue, date_retour = None):
        self.id = id
        self.livre = livre
        self.utilisateur = utilisateur
        self.date_emprunt = date_emprunt
        self.date_retour_prevue = date_retour_prevue
        self.date_retour = date_retour

class Gestion_Emprunt:

    def __init__(self):
        self.emprunts: list[Emprunt] = []

    def enregistrement_emprunt(self, livre: Livre, emprunt: Emprunt, date_emprunt, date_retour_prevue, date_retour):
        self.emprunts.append(emprunt)

    @classmethod
    def get_emprunt_info(self, id_emprunt: str) -> tuple[Emprunt, int]:
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
            return emprunt_id_user, emprunt_id_book, emprunt_date, emprunt_date_retour_prevue, emprunt_date_retour
        else:
            return None

