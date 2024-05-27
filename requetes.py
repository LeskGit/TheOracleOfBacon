#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code diffusé aux étudiants de BUT1 dans le cadre de la SAE 2.02: Exploration algorithmique d'un problème.

IUT d'Orleans BUT1 Informatique 2021-2022 
"""

import networkx as nx
import matplotlib.pyplot as plt

# Q1

def transformation_dic(chemin):
    res = []
    f = open(chemin, "r")
    for ligne in f:
        fic = eval(ligne) #transforme en dico
        res.append(fic) #création d'une liste de dictionnaires
    return res

def suppression(liste):
    for dico in liste:
        for i in range(len(dico["cast"])):
            nom = dico["cast"][i].strip("[]")
            dico["cast"][i] = nom.strip() #on enlève les espaces
    return liste

def json_vers_nx(chemin):
    transfo = suppression(transformation_dic(chemin))
    G = nx.Graph()
    for dico in transfo:
        liste_temp = []
        for actor in dico["cast"]:
            liste_temp.append(actor)
            if actor not in G.nodes():
                G.add_node(actor)
        for actor_temp in liste_temp:
            for all_actor_temp in liste_temp:
                if actor_temp != all_actor_temp and (actor_temp, all_actor_temp) not in G.edges():
                    G.add_edge(actor_temp, all_actor_temp)
            print(G)
    return G

# Q2
    
def collaborateurs_communs(G, u, v):
    ensemble_acteurs = set()
    collab_u = collaborateurs_proches(G, u, 1)
    collab_v = collaborateurs_proches(G, v, 1)
    for actor in collab_u:
        if actor in v:
            ensemble_acteurs.add(actor)
    return ensemble_acteurs

# Q3

def collaborateurs_proches(G, u, k):
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

def est_proche(G, u, v, k = 1):
    pass
def distance_naive(G, u, v):
    pass
def distance(G, u, v):
    pass
# Q4

#Utilitaire

def stack_init():
    return []

def stack_top(S):
    return S[-1]

def stack_pop(S):
    return S.pop()

def stack_push(S,u):
    S.append(u)

def graph_init(G,u):
    for v in G.nodes:
        G.nodes[v]["color"] = "white"
        G.nodes[v]["father"] = None
    for u, v in G.edges:
        G.edges[u,v]["color"] = "black"
    G.nodes[u]["color"] = "red"

def visiter(G,v,w):
    G.nodes[w]["color"] = "red"
    G.nodes[w]["father"] = v

def traiter(G, u):
    G.nodes[u]["color"] = "green"

def arete_arbre(G, v, w):
    G.edges[(v,w)]["color"] = "green"

def voisin_blanc(G, u):
    for w in G.adj[u]:
        if G.nodes[w]["color"] == "white":
            return w
    return None

def DFS(G,u):
    """
    Implémentation de l'algorithme du parcours en profondeur (DFS) en utilisant une pile.
    
    Paramètres:
    G -- le graphe que l'on veut parcourir
    u -- le sommet de départ du parcours
    """
    
    # initialisation
    
    S = stack_init()
    stack_push(S,u)
    graph_init(G,u)
    yield G #  pour l'animation
    visiter(G,None,u)
    
    # boucle principale
    while len(S) > 0:
        yield G #  pour l'animation
        v = stack_top(S)
        w = voisin_blanc(G,v) # on recherche un voisin non visité
        if w != None:
            stack_push(S,w)
            visiter(G,v,w)
            arete_arbre(G,v,w)
        else:
            traiter(G,v)
            stack_pop(S)
        yield G # pour animation


graphe = json_vers_nx("jeux de données réduits-20240506/data_100.txt")                     
graph_init(graphe,0)
parcours_g = DFS(graphe,0)

i = 0
for etat_de_G in parcours_g:
    print("etape", i, etat_de_G.nodes[3])
    i+=1

def centralite(G, u):
    pass


def centre_hollywood(G):
    pass
# Q5

def eloignement_max(G:nx.Graph):
    pass
# Bonus

def centralite_groupe(G, S):
    pass

#plt.figure(figsize=(12, 8))
#pos = nx.spring_layout(test, k=0.15, scale = 2)  # Utilisation de spring_layout avec un paramètre de ressort k ajusté

#nx.draw(test, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=200, font_size=10)  # Taille de nœud et police réduites
#plt.show()

#transfo = transformation("jeux de données réduits-20240506/data_100.txt")
#graphe = transformation_graphe(transfo)
#print(collaborateurs_communs(graphe, "Lew Horn", "Al Pacino"))