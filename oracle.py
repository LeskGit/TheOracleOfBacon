
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

    lettre = input()
    match lettre:
        case "I":
            menu_choix()
        case "Q":
            print("Adieu")
            return None
    
    
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

        nb = input()
        match nb:
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
                
                
                
                
print(menu_principal())