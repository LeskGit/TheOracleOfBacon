#Pour la transformation en Graphe la première version ne contenait pas de méthode "suppression". La deuxième ne contenait pas, lors de l'ouverture du 
#fichier, de choix de l'encoding

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
    """
    visites = []
    a_visiter = [(u, 0)]
    
    while len(a_visiter) > 0:
        acteur_courant, distance_courante = a_visiter.pop(0)
        
        if acteur_courant == v:
            return distance_courante
        
        visites.append(acteur_courant)
        
        for voisin in G.adj[acteur_courant]:
            if voisin not in visites:
                a_visiter.append((voisin, distance_courante + 1))
    
    return -1

# Exemple d'utilisation :
# distance_v1(G, 'Al Pacino', 'Robert De Niro')


def distanceV2(G, u, v):
    """
    Fonction renvoyant la distance entre les acteurs u et v dans le graphe G en utilisant une approche par pile (DFS).
    
    Paramètres :
        G : le graphe
        u : acteur de départ
        v : acteur d'arrivée
        
    Retourne :
        La distance entre u et v, None si l'un des acteurs est absent du graphe et -1 si l'acteur v n'est pas atteignable depuis u.
    """
    if u not in G.nodes or v not in G.nodes:
        return None

    pile = [(u, 0)]
    visites = set()

    while pile:
        acteur_courant, distance_courante = pile.pop()
        if acteur_courant == v:
            return distance_courante

        if acteur_courant not in visites:
            visites.add(acteur_courant)
            for voisin in G.adj[acteur_courant]:
                if voisin not in visites:
                    pile.append((voisin, distance_courante + 1))

    return -1

def distanceV3(G, u, v):
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


#est proche

def est_procheV1(G, u, v, k = 1):
    if u not in G.nodes:
        print(u," est un illustre inconnu")
        return None
    if v not in G.nodes:
        print(v," est un illustre inconnu")
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
    """
    collaborateurs = collaborateurs_proches(G, u, k)
    return v in collaborateurs


#Collaborateurs communs

def collaborateurs_communsV1(G, actor1, actor2):
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

def collaborateurs_communs_Bonus(G, u, k):
    """Fonction renvoyant le sous-graphe induit par l'acteur u et tous les acteurs à distance au plus k de u dans le graphe G.
    
    Paramètres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
        
    Retourne:
        Le sous-graphe induit par u et tous les sommets à distance k de u, ou None si u est absent du graphe.
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
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    
    # Créer le sous-graphe 
    sous_graphe = G.subgraph(collaborateurs).copy()
    return sous_graphe


# Eloignement Max

def eloignement_maxV1(G: nx.Graph):
    max_distance = None
    parcours = set(G.nodes)
    for act1 in parcours.copy():
        for act2 in parcours:
            if act1 != act2:
                temp = distance(G, act1, act2)
                if max_distance is None or temp > max_distance:
                    max_distance = temp
        parcours.remove(act1)
    return max_distance 

def eloignement_maxV2(G: nx.Graph):
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

def eloignement_maxV3(graph):
    # Choisissez un nœud arbitraire (ici, nous choisissons le premier nœud)
    start_node = next(iter(graph.nodes()))
    
    # Trouvez le nœud le plus éloigné de ce nœud arbitraire
    farthest_node = max(nx.single_source_shortest_path_length(graph, start_node).items(), key=lambda x: x[1])[0]
    
    # Trouvez le nœud le plus éloigné de ce nœud le plus éloigné précédemment trouvé
    approximate_diameter = max(nx.single_source_shortest_path_length(graph, farthest_node).values())
    
    return approximate_diameter


def eloignement_maxV4(G: dict):
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