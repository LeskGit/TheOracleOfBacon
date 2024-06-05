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
    """
    distance_maximale = 0
    vus = set()
    
    for noeud in G.nodes:
        if noeud not in vus:
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