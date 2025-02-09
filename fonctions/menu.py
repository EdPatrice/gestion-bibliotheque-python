import fonctions.fonctions_utilisateur as u
import fonctions.fonctions_emprunt as e
import fonctions.fonctions_statistiques as s
import fonctions.util as util

def menu_principal():
    util.clear_screen()
    print("------------BIENVENUE------------\n\n")

    print("\n1. Gestion des livres. \n2. Gestion des utilisateurs. \n3. Gestion des emprunts et des retours. \n4. Rapports et statistiques. \n\n0. Exit.")
    choix = input("\n\nChoisissez une option -> ")
    while util.choix_valide(choix, 0, 4) != True:    
        choix = input("\nChoix incorrect, reessayez -> ")
    options_menu_principal(int(choix))

def options_menu_principal(choix: int):
    util.clear_screen()
    match choix:
        #fermer le programme 
        case 0: 
            exit()

        # gestion livres
        case 1: 
            pass
        
        # gestion utilisateurs
        case 2:             
            u.menu_utilisateur()

        # gestion emprunts
        case 3:            
            e.menu_emprunt()

        # rapports
        case 4:             
            s.menu_statistiques()

    util.clear_screen()
    menu_principal()
        