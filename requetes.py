#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code diffusé aux étudiants de BUT1 dans le cadre de la SAE 2.02: Exploration algorithmique d'un problème.

IUT d'Orleans BUT1 Informatique 2021-2022 
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
import time

# Q1

def transformation_dic(chemin):
    res = []
    f = open(chemin, "r", encoding="utf-8")
    for ligne in f:
        fic = json.loads(ligne.strip()) # transforme en dictionnaire
        res.append(fic) #création d'une liste de dictionnaires
    return res

def suppression(liste):
    for dico in liste:
        dico["cast"] = [nom.strip("[]").strip() for nom in dico["cast"]]
    return liste

def json_vers_nx(chemin):
    transfo = suppression(transformation_dic(chemin))
    G = nx.Graph()
    for dico in transfo:
        acteurs = dico["cast"]
        G.add_nodes_from(acteurs)
        for i in range(len(acteurs)):
            for j in range(i + 1, len(acteurs)):
                G.add_edge(acteurs[i], acteurs[j])
    return G

# Q2

def collaborateurs_communs2(G, u, v):
    """
    Trouve l'ensemble des acteurs/actrices ayant collaboré avec deux acteurs/actrices donnés.

    Paramètres :
        G (nx.Graph): le graphe
        acteur1 (str): le premier acteur/actrice
        acteur2 (str): le deuxième acteur/actrice

    Retourne :
        set: l'ensemble des acteurs/actrices ayant collaboré avec les deux acteurs/actrices donnés.
    """
    # Obtention des voisins de chaque acteur
    voisins_acteur1 = set(G.adj[u])
    voisins_acteur2 = set(G.adj[v])
    
    # Calcul de l'ensemble des collaborateurs communs grâce à la fonction "union"
    collaborateurs_communs = voisins_acteur1.union(voisins_acteur2)
    
    return collaborateurs_communs


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
    #print(collaborateurs)
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
    Fonction renvoyant la distance entre les acteurs u et v dans le graphe G.
    
    Paramètres :
        G : le graphe
        u : acteur de départ
        v : acteur d'arrivée
        
    Retourne :
        La distance entre u et v, None si l'un des acteurs est absent du graphe et -1 si l'acteurs v n'est pas atteignable depuis u.
    """
    if u not in G.nodes or v not in G.nodes:
        return None

    distance = 0
    visites = set()
    file = [u]

    while file:
        distance += 1
        file2 = []
        for actor in file:
            visites.add(actor)
            for acteur in G.adj[actor]:
                if acteur == v:
                    return distance
                elif acteur not in visites:
                    file2.append(acteur)
        file = file2
    return -1

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

def eloignement_max(G: nx.Graph):
    pass

# Bonus

#plt.figure(figsize=(12, 8))
#pos = nx.spring_layout(test, k=0.15, scale = 2)  # Utilisation de spring_layout avec un paramètre de ressort k ajusté

#nx.draw(test, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=200, font_size=10)  # Taille de nœud et police réduites
#plt.show()

#transfo = transformation("jeux de données réduits-20240506/data_100.txt")
#graphe = transformation_graphe(transfo)
#print(collaborateurs_communs(graphe, "Lew Horn", "Al Pacino"))



# Fonctions optimisées avec des fonctions NetworkX :

def distanceOpti(G, u, v):
    return nx.shortest_path_length(G, u, v)

def centralite_acteurOpti(graphe, acteur):
    """
    Calcule la centralité de l'acteur dans le graphe.

    Paramètres:
        graphe (nx.Graph): le graphe
        acteur (Any): un acteur

    Résultat:
        int: la centralité de l'acteur
    """
    try:
        # Fonction de comparaison pour trouver le chemin le plus long
        def longueur_chemin(chemin):
            return len(chemin)

        # Trouve le chemin le plus long depuis l'acteur vers les autres acteurs
        chemin_le_plus_long = max(nx.single_source_dijkstra_path(graphe, acteur).items(), key=longueur_chemin)
        
        # Retourne le premier et dernier acteur du chemin le plus long, ainsi que sa longueur - 1
        return chemin_le_plus_long[1][0], chemin_le_plus_long[1][-1], len(chemin_le_plus_long[1]) - 1
    except:
        return None

def centre_hollywoodOpti(graphe):
    """
    Trouve le centre du graphe.

    Paramètres:
        graphe (nx.Graph): le graphe

    Résultat:
        str : le sommet au centre du graphe
    """
    # Fonction de comparaison pour trouver le chemin le plus long
    def longueur_chemin(chemin):
        return len(chemin)

    # Sélectionne un nœud arbitraire pour commencer les calculs
    noeud_depart = list(graphe.nodes)[0]
    
    # Trouve le chemin le plus long depuis le nœud de départ vers tous les autres nœuds
    chemin_le_plus_long = max(nx.single_source_dijkstra_path(graphe, centralite_acteurOpti(graphe, noeud_depart)[0]).items(), key=longueur_chemin)
    
    # Retourne l'élément central du chemin le plus long
    return chemin_le_plus_long[1][len(chemin_le_plus_long[1]) // 2]


