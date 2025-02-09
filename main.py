from fonctions.menu import menu_principal
import fonctions.util as util 
import json

# essayer d'ouvrir le fichier de configuration
files = json.load(open("config.json"))

# creer le fichier de configuration s'il n'existe pas
if files == None: 
    with open("config.json", 'w') as f:
        f.write('{\n"USERS_CSV": "./database/utilisateurs.csv", \n"BOOKS_CSV": "./database/livres.csv", \n"EMPRUNTS_CSV": "./database/emprunts.csv"}')

menu_principal()