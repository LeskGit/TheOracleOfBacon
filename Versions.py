import json
import networkx as nx
import matplotlib.pyplot as plt
import time

#Pour tester les temps

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

# Distance

def distance_v1(G, u, v):
    """
    Fonction renvoyant la distance entre les acteurs u et v dans le graphe G.

    Paramètres :
        G : le graphe
        u : acteur de départ
        v : acteur d'arrivée

    Retourne :
        La distance entre u et v, -1 si l'acteur v n'est pas atteignable depuis u.

    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    visites = []  # Liste des acteurs visités
    a_visiter = [(u, 0)]  # Liste des acteurs à visiter avec leur distance par rapport à u

    while len(a_visiter) > 0:
        acteur_courant, distance_courante = a_visiter.pop(0)  # Utilisation d'une file pour le parcours en largeur
        
        if acteur_courant == v:
            return distance_courante  # Si l'acteur cible est atteint, retourne la distance

        visites.append(acteur_courant)  # Ajoute l'acteur courant à la liste des visites
        
        for voisin in G.adj[acteur_courant]:
            if voisin not in visites:
                a_visiter.append((voisin, distance_courante + 1))  # Ajoute les voisins non visités à la liste à visiter avec la distance + 1
    
    return -1  # Si l'acteur v n'est pas atteignable depuis u

def distanceV2(G, u, v):
    """
    Fonction renvoyant la distance entre les acteurs u et v dans le graphe G en utilisant une approche par pile (DFS).

    Paramètres :
        G : le graphe
        u : acteur de départ
        v : acteur d'arrivée

    Retourne :
        La distance entre u et v, None si l'un des acteurs est absent du graphe et -1 si l'acteur v n'est pas atteignable depuis u.

    Complexité asymptotique : O(n + m), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    if u not in G.nodes or v not in G.nodes:
        return None

    pile = [(u, 0)]  # Utilisation d'une pile pour le parcours en profondeur
    visites = set()

    while pile:
        acteur_courant, distance_courante = pile.pop()  # Utilisation d'une pile pour le parcours en profondeur
        if acteur_courant == v:
            return distance_courante  # Si l'acteur cible est atteint, retourne la distance

        if acteur_courant not in visites:
            visites.add(acteur_courant)
            for voisin in G.adj[acteur_courant]:
                if voisin not in visites:
                    pile.append((voisin, distance_courante + 1))  # Ajoute les voisins non visités à la pile avec la distance + 1

    return -1  # Si l'acteur v n'est pas atteignable depuis u


def distanceV3(G, u, v):
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


#est proche

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

def est_procheV1(G, u, v, k=1):
    """
    Détermine si l'acteur v se trouve à distance k de l'acteur u dans le graphe G.

    Paramètres:
        G (nx.Graph): le graphe
        u (str): le sommet de départ
        v (str): l'acteur à vérifier
        k (int): la distance (par défaut à 1)

    Retourne:
        set: l'ensemble des acteurs/actrices à distance k de u, None si u ou v est absent du graphe.

    Complexité asymptotique: O(k * (n + m)), où n est le nombre de sommets et m est le nombre d'arêtes.
    """
    if u not in G.nodes:
        print(u, " est un illustre inconnu")
        return None
    if v not in G.nodes:
        print(v, " est un illustre inconnu")
        return None

    collaborateurs = set()
    collaborateurs.add(u)

    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)

    return v in collaborateurs


def est_procheV2(G, u, v, k=1):
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


#Collaborateurs communs

def collaborateurs_communsV1(G, actor1, actor2):
    """
    Trouve l'ensemble des acteurs/actrices ayant collaboré avec deux acteurs/actrices donnés.

    Paramètres :
        G (nx.Graph): le graphe
        actor1 (str): le premier acteur/actrice
        actor2 (str): le deuxième acteur/actrice

    Retourne :
        set: l'ensemble des acteurs/actrices ayant collaboré avec les deux acteurs/actrices donnés.

    Complexité asymptotique: O(n + m), où n est le nombre d'acteurs proches de actor1 ou actor2.
    """
    ensemble_acteurs = set()
    collab_actor1 = collaborateurs_proches(G, actor1, 1)
    collab_actor2 = collaborateurs_proches(G, actor2, 1)
    for actor in collab_actor1:
        if actor in collab_actor2:
            ensemble_acteurs.add(actor)
    return ensemble_acteurs


def collaborateurs_communsV2(G, u, v):
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


# Eloignement Max

def eloignement_maxV1(G: nx.Graph):
    """
    Trouve la distance maximale entre toutes les paires de nœuds dans le graphe G.

    Paramètres :
        G : le graphe non pondéré, non dirigé

    Retourne :
        La distance maximale entre toutes les paires de nœuds dans le graphe.
        
    Complexité asymptomatique: O(n^3), où n est le nombre de nœuds dans le graphe
    """
    max_distance = None
    parcours = set(G.nodes)
    
    # Parcours de tous les nœuds
    for act1 in parcours.copy():
        for act2 in parcours:
            if act1 != act2:
                # Calcul de la distance entre les paires de nœuds
                temp = distanceV3(G, act1, act2)
                # Mise à jour de la distance maximale
                if max_distance is None or temp > max_distance:
                    max_distance = temp
        parcours.remove(act1)
    return max_distance  

def eloignement_maxV2(G: nx.Graph):
    """
    Trouve la distance maximale entre toutes les paires de nœuds dans le graphe G.

    Paramètres :
        G : le graphe non pondéré, non dirigé

    Retourne :
        La distance maximale entre toutes les paires de nœuds dans le graphe.
        
    Complexité asymptotique: O(n + m), où n est le nombre d'acteurs proches de actor1 ou actor2
    """
    max_distance = -1
    
    # Parcours de tous les nœuds dans le graphe
    for source in G.nodes:
        # Pile pour le parcours en profondeur
        stack = [(source, 0)]
        # Ensemble pour suivre les nœuds visités
        visited = set([source])
        
        while stack:
            node, distance = stack.pop()
            # Mise à jour de la distance maximale si nécessaire
            max_distance = max(max_distance, distance)
            
            # Parcours des voisins du nœud actuel (en ordre inversé pour traiter le dernier voisin en premier)
            for neighbor in reversed(list(G.neighbors(node))):
                # Si le voisin n'a pas été visité, l'ajouter à la pile et à l'ensemble des visites
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, distance + 1))
                    
    return max_distance  

def bfs_distance_maximaleV1(G, noeud_depart):
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

def eloignement_maxV3(G: nx.Graph) -> int:
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
            u, _ = bfs_distance_maximaleV1(G, noeud)
            # Étape 2 : Trouver le nœud le plus éloigné de u
            _, distance = bfs_distance_maximaleV1(G, u)
            # Mettre à jour la distance maximale trouvée
            distance_maximale = max(distance_maximale, distance)
    
    return distance_maximale

def bfs_distance_maximaleV2(G, noeud_depart):
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

def eloignement_maxV4(G):
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
        u, _ = bfs_distance_maximaleV2(G, noeud)
        _, distance = bfs_distance_maximaleV2(G, u)
        distance_maximale = max(distance_maximale, distance)
    
    return distance_maximale

