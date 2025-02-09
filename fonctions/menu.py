import fonctions.fonctions_utilisateur as u
import fonctions.fonctions_emprunt as e
import fonctions.fonctions_statistiques as s
import fonctions.fonctions_livres as l
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
    match choix:
        #fermer le programme 
        case 0: 
            util.clear_screen()
            exit()

        # gestion livres
        case 1: 
            util.clear_screen()
            l.menu_livre()
        
        # gestion utilisateurs
        case 2: 
            util.clear_screen()
            u.menu_utilisateur()

        # gestion emprunts
        case 3:
            util.clear_screen()
            e.menu_emprunt()

        # rapports
        case 4: 
            util.clear_screen()
            s.menu_statistiques()

    util.clear_screen()
    menu_principal()
        