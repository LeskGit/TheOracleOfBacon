#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code diffusé aux étudiants de BUT1 dans le cadre de la SAE 2.02: Exploration algorithmique d'un problème.

IUT d'Orleans BUT1 Informatique 2021-2022 
"""

import networkx as nx

def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    print(collaborateurs)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs



def transformation(fichier):
    res = []
    f = open(fichier, "r")
    for ligne in f:
        fic = eval(ligne) #transforme en dico
        res.append(fic) #création d'une liste de dictionnaires
    for dic in res:
        for i in range(len(dic["cast"])):
            nom = dic["cast"][i].strip("[]")
            dic["cast"][i] = nom
    return res


test = transformation("jeux de données réduits-20240506/data_100.txt")
for dic in test:
    print(dic["cast"])
