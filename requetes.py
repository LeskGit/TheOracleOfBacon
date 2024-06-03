#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code diffusé aux étudiants de BUT1 dans le cadre de la SAE 2.02: Exploration algorithmique d'un problème.

IUT d'Orleans BUT1 Informatique 2021-2022 
"""

import networkx as nx
import matplotlib.pyplot as plt
import time

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

def est_proche(G, u, v, k=24):
    """
    Fonction qui détermine si l'acteur v se trouve à distance k de l'acteur u dans le graphe G.
    
    Paramètres:
        G: le graphe
        u: le sommet de départ
        v: l'acteur à vérifier
        k: la distance (par défaut à 1)
        
    Retourne:
        True si v se trouve à distance k de u, False sinon.
    """
    collaborateurs = collaborateurs_proches(G, u, k)
    return v in collaborateurs

def distance_naive(G, u, v):
    if u not in G.nodes or v not in G.nodes:
        return None
    distance = 0
    i = 0
    collab = collaborateurs_proches(G, u, distance)
    while v not in collab and i<len(G):
        distance += 1
        i += 1
        collab = collaborateurs_proches(G, u, distance)
    if i != len(G):
        return distance
    return -1
    
def distance(G, u, v):
    """
    Recherche en largeur pour déterminer la distance entre deux acteurs.
    
    Paramètres:
        G: le graphe
        u: le sommet de départ
        v: le sommet d'arrivée
        
    Retourne:
        La distance entre u et v, -1 si v n'est pas atteignable depuis u ou None si u ou v n'existe pas.
    """
    if u not in G.nodes or v not in G.nodes:
        return None
    
    queue = [(u, 0)]  # stocke les sommets à explorer et leur distance par rapport au sommet de départ
    visited = {u}     # Ensemble des sommets visités
    
    while queue: #tant que queue n'est pas vide
        sommet_actuel, distance = queue.pop(0)  # Retire le premier élément de la file
        if sommet_actuel == v:
            return distance
        for voisin in G.adj[sommet_actuel]:
            if voisin not in visited:
                visited.add(voisin)
                queue.append((voisin, distance + 1))  # Ajoute le voisin à la file avec la distance + 1
    
    return -1  # Si v n'est pas atteignable depuis u

test = json_vers_nx("jeux de données réduits-20240506/data_100.txt")
print(distance_naive(test, "Anne Bancroft", "Robert Downey Jr."))
print(distance(test, "Anne Bancroft", "Robert Downey Jr."))

# Q4


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
    dist_max = 0
    actor_target = u
    father = {u: (None, 0)}
    visite = set()
    
    # Boucle principale
    while len(Q) > 0:
        v = Q.pop(0)  # Défile le premier élément de la liste
        for w in G.adj[v]:
            if w not in visite:
                visite.add(w)
                father[w] = (v, father[v][1] + 1)
                if father[w][1] > dist_max:
                    dist_max = father[w][1]
                    actor_target = w
                Q.append(w)
    return actor_target, dist_max


def centre_hollywood(G):
    acteur_central = ""
    dist_max = None
    for actor in G.nodes():
        centralite = centralite_acteur(G, actor)
        if dist_max is None or centralite[1] < dist_max:
            dist_max = centralite[1]
            acteur_central = actor
    return acteur_central, dist_max


# Q5

#def eloignement_max(G:nx.Graph):

# Bonus

#plt.figure(figsize=(12, 8))
#pos = nx.spring_layout(test, k=0.15, scale = 2)  # Utilisation de spring_layout avec un paramètre de ressort k ajusté

#nx.draw(test, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=200, font_size=10)  # Taille de nœud et police réduites
#plt.show()

#transfo = transformation("jeux de données réduits-20240506/data_100.txt")
#graphe = transformation_graphe(transfo)
#print(collaborateurs_communs(graphe, "Lew Horn", "Al Pacino"))