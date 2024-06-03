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

G = json_vers_nx("jeux de données réduits-20240506/data_1000.txt")
#start = time.time()
#print(distance_naive(G, "Steven Bauer", "Robert Downey Jr."))
#end = time.time()
#print(end - start)
#start2 = time.time()
#print(distance(G, "Steven Bauer", "Robert Downey Jr."))
#end2 = time.time()
#print(end2 - start2)
#start2 = time.time()
#print(distance2(G, "Steven Bauer", "Robert Downey Jr."))
#end2 = time.time()
#print(end2 - start2)

# Q4


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

def eloignement_max(G: dict):
    max_distance = -1
    
    # Fonction pour le BFS à partir d'un nœud source
    def bfs(source):
        visited = {source}
        queue = [(source, 0)]
        local_max_distance = 0
        
        while queue:
            node, distance = queue.pop(0)
            local_max_distance = max(local_max_distance, distance)
            
            for neighbor in G[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        
        return local_max_distance
    
    # Parcours des nœuds pour trouver la distance maximale
    visited_nodes = set()
    
    for node in G:
        if node not in visited_nodes:
            # BFS à partir du nœud non visité
            component_max_distance = bfs(node)
            max_distance = max(max_distance, component_max_distance)
            visited_nodes.add(node)
    
    return max_distance


start = time.time()
print(eloignement_max(G))
end = time.time()
print(end - start)


# Bonus

#plt.figure(figsize=(12, 8))
#pos = nx.spring_layout(test, k=0.15, scale = 2)  # Utilisation de spring_layout avec un paramètre de ressort k ajusté

#nx.draw(test, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=200, font_size=10)  # Taille de nœud et police réduites
#plt.show()

#transfo = transformation("jeux de données réduits-20240506/data_100.txt")
#graphe = transformation_graphe(transfo)
#print(collaborateurs_communs(graphe, "Lew Horn", "Al Pacino"))