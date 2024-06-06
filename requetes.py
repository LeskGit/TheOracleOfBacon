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
    """
    Fonction pour transformer un fichier JSON en une liste de dictionnaires.
    
    Paramètre :
        chemin : chemin du fichier JSON
        
    Retourne :
        Une liste de dictionnaires représentant les données du fichier JSON.
        
    Complexité asymptotique : O(n), où n est le nombre de lignes dans le fichier.
    """
    res = []
    with open(chemin, "r", encoding="utf-8") as f:
        for ligne in f:
            fic = json.loads(ligne.strip())  # transforme chaque ligne en dictionnaire
            res.append(fic)  # ajoute le dictionnaire à la liste
    return res

def suppression(liste):
    """
    Fonction pour nettoyer les noms des acteurs en supprimant les crochets et les espaces superflus.
    
    Paramètre :
        liste : liste de dictionnaires contenant les informations des films
        
    Retourne :
        La liste de dictionnaires mise à jour avec les noms nettoyés.
        
    Complexité asymptotique : O(n * m), où n est le nombre de dictionnaires et m est le nombre d'acteurs par dictionnaire.
    """
    for dico in liste:
        # Nettoyage des noms des acteurs
        dico["cast"] = [nom.strip("[]").strip() for nom in dico["cast"]]
    return liste

def json_vers_nx(chemin):
    """
    Fonction pour transformer les données JSON en un graphe NetworkX.
    
    Paramètre :
        chemin : chemin du fichier JSON
        
    Retourne :
        Un graphe NetworkX représentant les relations entre les acteurs.
        
    Complexité asymptotique : O(n * m^2), où n est le nombre de films et m est le nombre d'acteurs par film.
    """
    transfo = suppression(transformation_dic(chemin))
    G = nx.Graph()
    for dico in transfo:
        acteurs = dico["cast"]
        G.add_nodes_from(acteurs)  # ajout des acteurs comme noeuds
        for i in range(len(acteurs)):
            for j in range(i + 1, len(acteurs)):
                G.add_edge(acteurs[i], acteurs[j])  # ajout des arêtes entre les acteurs ayant joué ensemble
    return G

# Q2

def collaborateurs_communs(G, u, v):
    """
    Trouve l'ensemble des acteurs/actrices ayant collaboré avec deux acteurs/actrices donnés.
    
    Paramètres :
        G (nx.Graph): le graphe
        u (str): le premier acteur/actrice
        v (str): le deuxième acteur/actrice
        
    Retourne :
        set: l'ensemble des acteurs/actrices ayant collaboré avec les deux acteurs/actrices donnés.
        
    Complexité asymptotique : O(d1 + d2), où d1 est le degré de u et d2 est le degré de v.
    """
    # Obtention des voisins de chaque acteur
    voisins_acteur1 = set(G.adj[u])
    voisins_acteur2 = set(G.adj[v])
    
    # Calcul de l'ensemble des collaborateurs communs grâce à la fonction "intersection"
    collaborateurs_communs = voisins_acteur1.intersection(voisins_acteur2)
    
    return collaborateurs_communs

def collaborateurs_communs_Bonus(G, u, k):
    """
    Fonction renvoyant le sous-graphe induit par l'acteur u et tous les acteurs à distance au plus k de u dans le graphe G.
    
    Paramètres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
        
    Retourne:
        Le sous-graphe induit par u et tous les sommets à distance k de u, ou None si u est absent du graphe.
        
    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes explorées jusqu'à la distance k.
    """
    if u not in G.nodes:
        print(u, "est un illustre inconnu")
        return None

    collaborateurs = set()
    collaborateurs.add(u)
    
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        # Union des nouveaux collaborateurs directs avec l'ensemble existant
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    
    # Créer le sous-graphe induit
    sous_graphe = G.subgraph(collaborateurs).copy()
    return sous_graphe

# Q3

def collaborateurs_proches(G, u, k):
    """
    Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. 
    La fonction renvoie None si u est absent du graphe.
    
    Paramètres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
        
    Retourne:
        Un ensemble contenant les acteurs à distance au plus k de u.
        
    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes explorées jusqu'à la distance k.
    """
    if u not in G.nodes:
        print(u, "est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        # Union des nouveaux collaborateurs directs avec l'ensemble existant
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs

def est_proche(G, u, v, k=1):
    """
    Fonction qui détermine si l'acteur v se trouve à distance k de l'acteur u dans le graphe G.
    
    Paramètres:
        G: le graphe
        u: le sommet de départ
        v: l'acteur à vérifier
        k: la distance (par défaut à 1)
        
    Retourne:
        True si v se trouve à distance k de u, False sinon.
        
    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes explorées jusqu'à la distance k.
    """
    collaborateurs = collaborateurs_proches(G, u, k)
    return v in collaborateurs

def distance_naive(G, u, v):
    """
    Fonction renvoyant la distance entre les acteurs u et v dans le graphe G.
    Cette version est volontairement non optimisée.
    
    Paramètres :
        G : le graphe
        u : acteur de départ
        v : acteur d'arrivée
        
    Retourne :
        La distance entre u et v, None si l'un des acteurs est absent du graphe, et -1 si v n'est pas atteignable depuis u.
        
    Complexité asymptotique : O(n^2 + nm), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    if u not in G.nodes or v not in G.nodes:
        return None
    distance = 0
    i = 0
    collab = collaborateurs_proches(G, u, distance)
    while v not in collab and i < len(G):
        distance += 1
        i += 1
        collab = collaborateurs_proches(G, u, distance)
    if i != len(G):
        return distance
    return -1
    
def distance(G, u, v):
    """
    Fonction renvoyant la distance entre les acteurs u et v dans le graphe G en utilisant une approche par file (BFS).
    
    Paramètres :
        G : le graphe
        u : acteur de départ
        v : acteur d'arrivée
        
    Retourne :
        La distance entre u et v, None si l'un des acteurs est absent du graphe, et -1 si v n'est pas atteignable depuis u.
        
    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes.
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
        # Remplacement de la file actuelle par la nouvelle file
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

    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    
    # Initialisation de la file d'attente et des variables de suivi
    Q = []
    Q.append(u)
    dist_max = 0
    actor_target = u
    father = {u: (None, 0)}
    visite = set()
    
    # Boucle principale de BFS
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
    """
    Trouve l'acteur central d'Hollywood en utilisant la centralité des acteurs.

    Paramètres:
        G -- le graphe représentant les relations entre les acteurs

    Retourne:
        acteur_central -- l'acteur ayant la plus petite distance maximale à partir de n'importe quel autre acteur
        dist_max -- la distance maximale à partir de cet acteur

    Complexité asymptotique : O(n * (n + m)), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    acteur_central = ""
    dist_max = None
    for actor in G.nodes():
        centralite = centralite_acteur(G, actor)
        if dist_max is None or centralite[1] < dist_max:
            dist_max = centralite[1]
            acteur_central = actor
    return acteur_central, dist_max

# Q5

def bfs_distance_maximale(G, noeud_depart):
    """
    Effectue un parcours en largeur (BFS) pour trouver le nœud le plus éloigné
    à partir d'un nœud de départ et la distance maximale.

    Paramètres :
        G : le graphe sous forme de dictionnaire où les clés sont les nœuds
            et les valeurs sont les listes de voisins de chaque nœud.
        noeud_depart : le nœud de départ pour le BFS

    Retourne :
        Un tuple (dernier_noeud, distance_max) où dernier_noeud est le nœud le plus éloigné
        du noeud_depart et distance_max est la distance jusqu'à ce nœud.

    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    visites = set()
    file = [(noeud_depart, 0)]
    dernier_noeud, distance_max = noeud_depart, 0

    while file:
        noeud_courant, distance_courante = file.pop(0)
        if noeud_courant not in visites:
            visites.add(noeud_courant)
            dernier_noeud, distance_max = noeud_courant, distance_courante
            for voisin in G[noeud_courant]:
                if voisin not in visites:
                    file.append((voisin, distance_courante + 1))
    
    return dernier_noeud, distance_max

def eloignement_max(G):
    """
    Trouve la distance maximale entre toutes les paires de nœuds dans le graphe G.

    Paramètres :
        G : le graphe sous forme de dictionnaire où les clés sont les nœuds
            et les valeurs sont les listes de voisins de chaque nœud.

    Retourne :
        La distance maximale entre toutes les paires de nœuds dans le graphe.

    Complexité asymptotique : O(n * (n + m)), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    distance_maximale = 0
    
    for noeud in G:
        u, _ = bfs_distance_maximale(G, noeud)
        _, distance = bfs_distance_maximale(G, u)
        distance_maximale = max(distance_maximale, distance)
    
    return distance_maximale


# Bonus

#def centralite_groupe(G,S):

# Fonctions optimisées avec des fonctions NetworkX :

def distanceOpti(G, u, v):
    """
    Calcule la distance la plus courte entre les nœuds u et v dans le graphe G en utilisant l'algorithme de Dijkstra.

    Paramètres:
        G : le graphe
        u : acteur de départ
        v : acteur d'arrivée

    Retourne:
        int : la distance la plus courte entre u et v

    Complexité asymptotique : O(n log n + m), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    return nx.shortest_path_length(G, u, v)

def centralite_acteurOpti(graphe, acteur):
    """
    Calcule la centralité de l'acteur dans le graphe.

    Paramètres:
        graphe (nx.Graph): le graphe
        acteur (Any): un acteur

    Résultat:
        tuple : le premier et dernier acteur du chemin le plus long, ainsi que la longueur de ce chemin

    Complexité asymptotique : O(n log n + m), où n est le nombre de sommets et m est le nombre d'arêtes.
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

    Complexité asymptotique : O(n (n log n + m)), où n est le nombre de sommets et m est le nombre d'arêtes.
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

def bfs_distance_maximaleOpti(G, noeud_depart):
    """
    Effectue un parcours en largeur (BFS) pour trouver le nœud le plus éloigné
    à partir d'un nœud de départ et la distance maximale.

    Paramètres :
        G : le graphe
        noeud_depart : le nœud de départ pour le BFS

    Retourne :
        Un tuple (noeud_final, distance_max) où noeud_final est le nœud le plus éloigné
        du noeud_depart et distance_max est la distance jusqu'à ce nœud.

    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    distances = nx.single_source_shortest_path_length(G, noeud_depart)
    noeud_final = max(distances, key=distances.get)
    distance_max = distances[noeud_final]
    return noeud_final, distance_max

def eloignement_maxOpti(G: nx.Graph) -> int:
    """
    Trouve la distance maximale entre toutes les paires de nœuds dans le graphe G.

    Paramètres :
        G : le graphe non pondéré, non dirigé

    Retourne :
        La distance maximale entre toutes les paires de nœuds dans le graphe.

    Complexité asymptotique : O(n * (n + m)), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    distance_maximale = 0
    vus = set()
    
    for noeud in G.nodes:
        if noeud not in vus:
            # Trouver la composante connexe contenant le noeud
            composante_connexe = nx.node_connected_component(G, noeud)
            vus.update(composante_connexe)
            # Étape 1 : Trouver le nœud le plus éloigné de n'importe quel nœud de la composante
            u, _ = bfs_distance_maximaleOpti(G, noeud)
            # Étape 2 : Trouver le nœud le plus éloigné de u
            _, distance = bfs_distance_maximaleOpti(G, u)
            # Mettre à jour la distance maximale trouvée
            distance_maximale = max(distance_maximale, distance)
    
    return distance_maximale

G = json_vers_nx("jeux de données réduits-20240506/data_100.txt")
start = time.time()
print(eloignement_maxOpti(G))
end = time.time()
print(end - start)