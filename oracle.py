
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
         "|   C - 100 (par défault)      |\n"
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
         "|                              |\n"
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
                  print(acteur , "à une centralité de :",rq.centralite_acteur(data, acteur)[1])
             case "H":
                  print("Le centre d'Holywood est :", rq.centre_hollywood(data)[0])
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
         "|                              |\n"
         "| C - collaborateurs communs   |\n"
         "| P - Collaborateurs proches   |\n"
         "|                              |\n"
         "|                              |\n"
         "|                              |\n"
         "|______________________________|\n")

        lettre = input("Veuillez entrer une lettre majuscule ici : ")
        match lettre:
             case "C":
                  actor1 = input()
                  actor2 = input()
                  print("Les collaborateurs de ", actor1, "et ", actor2, "sont : ", rq.collaborateurs_communs(data, actor1, actor2))
             case "P":
                  actor1 = input()
                  print("Les collaborateurs de ", actor1, "sont : ", rq.collaborateurs_proches(data, actor1, 1))
                
print(menu_principal())