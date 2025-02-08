class User:

    def __init__(self, id, name, contact):
        self.id = id
        self.name = name
        self.contact = contact
    
class ManageUser: 

    def __init__(self):
        self.users: list[User] = []

    def add_user(self, users: User):
        for user in users: 
            self.users.append(user)

    def search_user(self, id) -> User: 
        for user in self.users: 
            if user.id == id: 
                return user
        return None
    
    @classmethod
    def list_users(self, USERS_CSV: str, get_all_details: bool= 0):
        with open(USERS_CSV, 'r') as f:
            users = f.readlines()
        for user in users[1:]:
            user = user.split(", ")
            if get_all_details != True:
                print("ID:", user[0], "\tNom:", user[1])
            else:
                print("ID:", user[0], "\tNom:", user[1], "\tEmail:", user[2])
   
class Book: 
    
    def __init__(self, id, title, author, genre):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre    

class ManageBooks: 
    
    def __init__(self):
        self.books: list[Book] = []

    def add_book(self, books: list[Book]):
        for book in books: 
            self.books.append(book)

    def search_book(self, id) -> Book: 
        for book in self.books: 
            if book.id == id: 
                return book
        return None
    
    @classmethod
    def list_books(self, BOOKS_CSV: str, get_all_details: bool= 0):
        with open(BOOKS_CSV, 'r') as f:
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

class Gestion_emprunt:

    def __init__(self):
        self.emprunts: list[Emprunt] = []

    def enregistrement_emprunt(self, livre: Book, emprunt: Emprunt, date_emprunt, date_retour_prevue, date_retour):
        self.emprunts.append(emprunt)

class Utilisateur:
    def __init__(self, id_utilisateur, nom, prenom, contact):
        # Initialiser les attributs de l'utilisateur
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.contact = contact
        self.emprunts = []  # Liste pour suivre les emprunts de l'utilisateur

    @classmethod
    def afficher_utilisateurs(self, USERS_CSV: str, get_all_detail: bool= 0):
        with open(USERS_CSV, 'r') as f:
            utilisateurs = f.readlines()        
        for utilisateur in utilisateurs[1:]:
            utilisateur = utilisateur.split(", ")
            if not get_all_detail:
                print("ID:", utilisateur[0], "\t Nom:", utilisateur[1], " ", utilisateur[2])
            else:
                print("ID:", utilisateur[0], "\tPrenom:", utilisateur[1], "\tNom:", utilisateur[2], "\tContact:", utilisateur[3])            


    def write_headers(USERS_CSV: str):
        with open(USERS_CSV, 'w') as f: 
            f.write("Id, Nom, Prenom, Contact")

    def enregistrer_utilisateur(self, USERS_CSV: str):
        import os
        if os.path.getsize(USERS_CSV) == 0:
            self.write_headers()            
        with open(USERS_CSV, 'w') as f:
            f.write(f"{self.id_utilisateur}, {self.nom}, {self.prenom}, {self.contact} \n")

    def get_user_info(self, USERS_CSV: str, user_id: str):
        utilisateur_existe = False

        with open(USERS_CSV, 'r') as f: 
            users = f.readlines()
        index_utilisateur = 0
        for user in users: 
            user = user.replace('\n', '').split(", ")
            if user[0] == user_id:
                utilisateur_existe = True
                self.id_utilisateur = user_id
                self.nom = user[1]
                self.prenom = user[2]
                self.contact = user[3]
            index_utilisateur += 1
        if utilisateur_existe:
            return self, index_utilisateur
        else: 
            return None

    def modifier_utilisateur(self, USERS_CSV: str):
        self, index_utilisateur = self.get_user_info(USERS_CSV, self.id_utilisateur)
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
            with open(USERS_CSV, 'r') as f:
                utilisateurs = f.readlines()
            utilisateur_a_modifier = utilisateurs[index_utilisateur]
            utilisateur_a_modifier[1] = self.nom
            utilisateur_a_modifier[2] = self.prenom
            utilisateur_a_modifier[3] = self.contact
            utilisateurs[index_utilisateur] = utilisateur_a_modifier

            # ecrire les donnees modifiees dans le fichier
            with open(USERS_CSV, 'w') as f:
                f.writelines(utilisateurs)

            print("\nModifications effectuees avec succes. \nLes nouvelles donnees sont: \n")
            print("Nom:\t", self.nom)
            print("Prenom:\t", self.prenom)
            print("Contact:\t", self.contact, '\n')


