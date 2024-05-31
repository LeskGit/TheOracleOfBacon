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






#Pile pour le parcours en profondeur

import networkx as nx

def graph_init(G):
    """
    Initialisation des attributs des nœuds et des arêtes du graphe.
    
    Paramètres:
    G -- le graphe à initialiser
    """
    for v in G.nodes:
        G.nodes[v]["color"] = "white"
        G.nodes[v]["father"] = None
    for u, v in G.edges:
        G.edges[u, v]["color"] = "black"

def visiter(G, v, w):
    """
    Met à jour les attributs d'un nœud lors de sa visite.
    
    Paramètres:
    G -- le graphe contenant le nœud
    v -- le nœud parent
    w -- le nœud en cours de visite
    """
    G.nodes[w]["color"] = "red"
    G.nodes[w]["father"] = v

def arete_arbre(G, v, w):
    """
    Met à jour la couleur d'une arête pour indiquer qu'elle appartient à l'arbre de parcours.
    
    Paramètres:
    G -- le graphe contenant l'arête
    v -- le nœud de départ de l'arête
    w -- le nœud d'arrivée de l'arête
    """
    G.edges[v, w]["color"] = "green"

def traiter(G, v):
    """
    Met à jour les attributs d'un nœud après son traitement.
    
    Paramètres:
    G -- le graphe contenant le nœud
    v -- le nœud à traiter
    """
    G.nodes[v]["color"] = "green"



def centralite_acteur(G, u):
    """
    Implémentation de l'algorithme de parcours en largeur (BFS) en utilisant une liste comme file d'attente.
    
    Paramètres:
    G -- le graphe à parcourir
    u -- le sommet de départ du parcours
    
    Valeur de retour:
    actor_target -- le nœud le plus éloigné du nœud de départ
    dist_max -- la distance maximale à partir du nœud de départ
    """
    
    # Initialisation
    Q = []
    Q.append(u)
    graph_init(G)
    visiter(G, None, u)
    dist_max = 0
    actor_target = u
    father = {u: (None, 0)}
    
    # Boucle principale
    while len(Q) > 0:
        v = Q.pop(0)  # Défile le premier élément de la liste
        for w in G.adj[v]:
            if G.nodes[w]["color"] == "white":
                visiter(G, v, w)
                arete_arbre(G, v, w)
                father[w] = (v, father[v][1] + 1)
                if father[w][1] > dist_max:
                    dist_max = father[w][1]
                    actor_target = w
                Q.append(w)
        traiter(G, v)
    return actor_target, dist_max



G = json_vers_nx("jeux de données réduits-20240506/data_100.txt")    



def centre_hollywood(G):
    acteur_central = ""
    dist_max = None
    for actor in G.nodes():
        centralite = centralite_acteur(G, actor)
        if dist_max is None or centralite[1] < dist_max:
            dist_max = centralite[1]
            acteur_central = actor
    return acteur_central, dist_max


print(centre_hollywood(G))





