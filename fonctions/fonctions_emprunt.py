import fonctions.util as util
from classes import Gestion_Utilisateurs, Gestion_Livres, Emprunt, Gestion_Emprunt

files = util.read_json("config.json")

def menu_emprunt(retour_au_menu_principal = False):    
        if not retour_au_menu_principal:   
            util.clear_screen()
            choix = input("Veuillez inserer le numero correspondant a l'option desiree: \n\n1. Enregistrement d'un emprunt. \n2. Enregistrer un retour. \n3. Voir les retards de retour. \n\n0. Retour. \n\n-> ")
            while util.choix_valide(choix, 0, 3) != True:
                    choix = input("Saisie incorrecte, reesayez -> ")  
            choix = int(choix) 
            options_menu_emprunt(choix)

def options_menu_emprunt(choix):
    match choix:             
        case 0:            
            menu_emprunt(True) 
            return
        case 1:                             # enregistrer un emprunt
            util.clear_screen()
            Gestion_Emprunt.enregistrement_emprunt()                
            util.wait()

        case 2:                 # enregistrer un retour
            # lister les emprunts sans date de retour et choisir l'emprunt a mettre a jour
            util.clear_screen()
            Gestion_Emprunt.enregistrement_retour()                

        case 3:             # voir les retards sur retour
            util.clear_screen()
            Gestion_Emprunt.lister_retards_sur_retours()
            util.wait()    
    util.clear_screen()
    menu_emprunt()