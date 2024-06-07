
import requetes as rq
import networkx as nx
import matplotlib.pyplot as plt
import time


global data
data = rq.json_vers_nx("jeux de données réduits-20240506/data_100.txt")

def  menu_principal():
    
    print(" ______________________________\n"
         "|==============================|\n"
         "|       TheOracleOfBacon       |\n"
         "|==============================|\n"
         "|                              |\n"
         "|   I - Choix des données      |\n"
         "|   G - Afficher le graphe     |\n"
         "|   C - Centralité             |\n"
         "|   V - Collaborateurs         |\n"
         "|   D - Distance               |\n"
         "|   Q - Quitter                |\n"
         "|                              |\n"
         "|______________________________|\n")

    lettre = input("Veuillez entrer une lettre majuscule ici : ")
    match lettre:
        case "I":
            menu_choix()
        case "G":
            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(data, k=0.15, scale = 2)  # Utilisation de spring_layout avec un paramètre de ressort k ajusté

            nx.draw(data, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=200, font_size=10)  # Taille de nœud et police réduites
            plt.show()
            menu_principal()
        case "C":
              menu_centralite()
        case "V":
              menu_collaborateur()
        case "D":
              menu_distance()
        case "Q":
            print("Adieu")
            return None
        case _:
                print("Saisi invalide")
                menu_principal()
        
    
    
def menu_choix():
    
        print(" ______________________________\n"
         "|==============================|\n"
         "|       Choix des données      |\n"
         "|==============================|\n"
         "|                              |\n"
         "|   C - 100                    |\n"
         "|   M - 1000                   |\n"
         "|   D - 10 000                 |\n"
         "|   F - Toute les données      |\n"
         "|   Q - Quitter                |\n"
         "|                              |\n"
         "|                              |\n"
         "|______________________________|\n")

        lettre = input("Veuillez entrer une lettre majuscule ici : ")
        match lettre:
            case "C":
                data = rq.json_vers_nx("jeux de données réduits-20240506/data_100.txt")
                print("Data initialisé à 100")
                menu_principal()
            case "M":
                data = rq.json_vers_nx("jeux de données réduits-20240506/data_1000.txt")
                print("Data initialisé à 1000")
                menu_principal()
            case "D":
                data = rq.json_vers_nx("jeux de données réduits-20240506/data_10000.txt")
                print("Data initialisé à 10 000")
                menu_principal()
            case "F":
                data = rq.json_vers_nx("data.txt/data.txt")
                print("Data initialisé à FULL")
                menu_principal()
            case "Q":
                menu_principal()
            case _:
                print("Saisi invalide")
                menu_choix()
                
def menu_centralite():
    
        print(" ______________________________\n"
         "|==============================|\n"
         "|          Centralité          |\n"
         "|==============================|\n"
         "|                              |\n"
         "|                              |\n"
         "|     I - Information          |\n"
         "|     A - Centralité acteur    |\n"
         "|     H - Centre Holywood      |\n"
         "|     Q - Quitter              |\n"
         "|                              |\n"
         "|                              |\n"
         "|______________________________|\n")

        lettre = input("Veuillez entrer une lettre majuscule ici : ")
        match lettre:
             case "A":
                  print("Veuillez entrer le prenom nom de l'acteur souhaité (avec majuscule)")
                  acteur = input()
                  try:
                      print(acteur , "à une centralité de :",rq.centralite(data, acteur)[1])
                      menu_centralite()
                  except:
                      print("Acteur introuvable")
                      menu_centralite()
             case "H":
                  print("Le centre d'Holywood est : ", rq.centre_hollywoodOpti(data))
                  menu_centralite()
             case "I":
                 print("=============================INFORMATION=========================================")
                 print("Voici les informations des différentes fonctions présentes dans ce menu : ")
                 print("- Centralité_acteur : Prend en paramètre 1 acteurs, renvoie sa centralité.")
                 print("- Centre_Holywood  : Renvoie l'acteur le plus central du graphe.")
                 print("=================================================================================")
                 menu_centralite()
             case "Q":
                menu_principal()
             case _:
                print("Saisi invalide")
                menu_centralite()

def menu_collaborateur():
    
        print(" ______________________________\n"
         "|==============================|\n"
         "|         Collaborateurs       |\n"
         "|==============================|\n"
         "|                              |\n"
         "|                              |\n"
         "| I - Information              |\n"
         "| C - Collaborateurs communs   |\n"
         "| P - Collaborateurs proches   |\n"
         "| Q - Quitter                  |\n"
         "|                              |\n"
         "|                              |\n"
         "|______________________________|\n")

        lettre = input("Veuillez entrer une lettre majuscule ici : ")
        match lettre:
             case "C":
                  actor1 = input("Veuillez entrer le prenom nom de l'acteur 1  (avec majuscule) : ")
                  actor2 = input("Veuillez entrer le prenom nom de l'acteur 2 (avec majuscule) : ")
                  try:
                      print("Les collaborateurs communs de ", actor1, "et ", actor2, "sont : ", rq.collaborateurs_communs(data, actor1, actor2))
                      menu_collaborateur()
                  except:
                      print("L'un des acteurs est introuvable")
                      menu_collaborateur()
             case "P":
                  actor1 = input("Veuillez entrer le prenom nom de l'acteur souhaité (avec majuscule) : ")
                  if rq.collaborateurs_proches(data, actor1, 1) != None:
                     print("Les collaborateurs de ", actor1, "sont : ", rq.collaborateurs_proches(data, actor1, 1))
                     menu_collaborateur()
                  else:
                      print("Acteur introuvable")
                      menu_collaborateur()
             case "Q":
                menu_principal()
             case "I":
                print("=============================INFORMATION=========================================")
                print("Voici les informations des différentes fonctions présentes dans ce menu : ")
                print("- Collaborateurs_communs : Prend en paramètre 2 acteurs, \n renvoie l'ensemble de leurs collaborateurs en communs.")
                print("- Collaborateurs_proches : Prend en paramètre 1 acteurs et une distance k, \n renvoie l'ensemble des acteurs à distance au plus k de l'acteur u.")
                print("=================================================================================")
                menu_collaborateur()
             case _:
                print("Saisi invalide")
                menu_collaborateur()

def menu_init():
    
        print(" ______________________________\n"
         "|==============================|\n"
         "| Veuillez choisir des données |\n"
         "|==============================|\n"
         "|                              |\n"
         "|   C - 100                    |\n"
         "|   M - 1000                   |\n"
         "|   D - 10 000                 |\n"
         "|   F - Toutes les données     |\n"
         "|                              |\n"
         "|                              |\n"
         "|                              |\n"
         "|______________________________|\n")

        lettre = input("Veuillez entrer une lettre majuscule ici : ")
        match lettre:
            case "C":
                data = rq.json_vers_nx("jeux de données réduits-20240506/data_100.txt")
                print("Data initialisée à 100")
                menu_principal()
            case "M":
                data = rq.json_vers_nx("jeux de données réduits-20240506/data_1000.txt")
                print("Data initialisée à 1000")
                menu_principal()
            case "D":
                data = rq.json_vers_nx("jeux de données réduits-20240506/data_10000.txt")
                print("Data initialisée à 10 000")
                menu_principal()
            case "F":
                data = rq.json_vers_nx("data.txt/data.txt")
                print("Data initialisée à FULL")
                menu_principal()
            case _:
                print("Saisi invalide")
                menu_choix()

def menu_distance():
    
        print(" ______________________________\n"
         "|==============================|\n"
         "|           Distance           |\n"
         "|==============================|\n"
         "|                              |\n"
         "|                              |\n"
         "|      I - Information         |\n"
         "|      D - Distance            |\n"
         "|      E - Eloignement max     |\n"
         "|      Q - Quitter             |\n"
         "|                              |\n"
         "|                              |\n"
         "|______________________________|\n")

        lettre = input("Veuillez entrer une lettre majuscule ici : ")
        match lettre:
            case "I":
                print("=============================INFORMATION=========================================")
                print("Voici les informations des différentes fonctions présentes dans ce menu : ")
                print("- Distance : Prends en paramètre 2 acteurs et retourne la distance les séparants")
                print("=================================================================================")
                menu_distance()
            case "D":
                acteur1 = input("Veuillez entrer le prenom nom de l'acteur souhaité (avec majuscule) : ")
                acteur2 = input("Veuillez entrer le prenom nom de l'acteur souhaité (avec majuscule) : ")
                if rq.distanceOpti(data, acteur1, acteur2) != None:
                    print("La distance entre ces deux acteurs est : ", rq.distanceOpti(data, acteur1, acteur2))
                    menu_distance()
                else:
                    print("L'un des acteurs est introuvable")
                    menu_distance()
            case "E":
                print("L'éloignement maximum entre deux noeuds est de : ", rq.eloignement_maxOpti(data))
                menu_distance()
            case "Q":
                menu_principal()
            case _:
                print("Saisi invalide")
                menu_distance()
                
print(menu_init())