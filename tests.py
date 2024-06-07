import requetes as rq
import networkx as nx
import matplotlib.pyplot as plt



#Initialisation des graphes pour les tests

G1 = nx.Graph()
G1.add_nodes_from([1, 2, 3, 4, 5])
G1.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)])


G2 = nx.Graph()
nodes = range(1, 31)
G2.add_nodes_from(nodes)
edges = [
    (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), 
    (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13), 
    (7, 14), (7, 15), (8, 16), (8, 17), (9, 18), (9, 19), 
    (10, 20), (10, 21), (11, 22), (11, 23), (12, 24), (12, 25), 
    (13, 26), (13, 27), (14, 28), (14, 29), (15, 30)
]
G2.add_edges_from(edges)

G3 = nx.Graph()

# Ajouter 20 nœuds représentant des mots sur le thème des fruits
fruits = ["pomme", "banane", "orange", "fraise", "kiwi",
           "ananas", "citron", "mangue", "cerise",
          "abricot", "poire", "pêche", "pastèque", "prune",
          "grenade", "framboise", "figue", "avocat", "cassis"]

G3.add_nodes_from(fruits)

# Ajouter des arêtes pour connecter certains nœuds
relations = [("pomme", "banane"), ("pomme", "orange"), ("pomme", "fraise"),
             ("banane", "kiwi"), ("banane", "ananas"), ("orange", "citron"),
             ("orange", "mangue"), ("fraise", "cerise"), ("fraise", "abricot"),
             ("kiwi", "poire"), ("poire", "pêche"), ("poire", "avocat"),
             ("abricot", "pastèque"), ("pastèque", "prune"), ("prune", "grenade"),
             ("grenade", "framboise"), ("framboise", "figue"), ("figue", "avocat"),
             ("avocat", "cassis")]

G3.add_edges_from(relations)


#Utilitaire

def afficheG(G):
    nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold')
    plt.show()

#Tests

def test_collaborateurs_communs():
    assert rq.collaborateurs_communs(G1,1,2) == {3}
    assert rq.collaborateurs_communs(G1,2,5) == {4, 3}
    assert rq.collaborateurs_communs(G2,1,17) == set()
    
def test_est_proche():
    assert not rq.est_proche(G1, 1, 5)
    assert rq.est_proche(G2, 1, 2)
    assert rq.est_proche(G2, 1, 30, 5) #distance passe de 24 a 5 pour des questions de simplicité et lisibilité
    
def test_distance():
    assert rq.distance(G1,1,2) == 1
    assert rq.distance(G1,2,5) == 2
    assert rq.distance(G1,17,28) is None
    
def test_distance_naive():
    assert rq.distance(G1,1,2) == 1
    assert rq.distance(G1,2,5) == 2
    assert rq.distance(G1,17,28) is None
    
def test_centralite():
    assert rq.centralite(G1,1)[1] == 2
    assert rq.centralite(G2,2)[1] == 5
    assert rq.centralite(G2,17)[1] == 8

def test_centralite_holywood():
    assert rq.centre_hollywood(G1)[0] == 1
    assert rq.centre_hollywood(G2)[0] == 1
    assert rq.centre_hollywood(G3)[0] == "pomme"
    
def test_eloignement_max():
    assert rq.eloignement_max(G1) == 2
    assert rq.eloignement_max(G2) == 8
    assert rq.eloignement_max(G3) == 8


