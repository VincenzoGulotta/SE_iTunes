from networkx.algorithms.connectivity import node_disjoint_paths

from model.model import Model

model = Model()

model.create_graph(200)

n = len(model.albums.keys())
print(n)

nodi = model.G.number_of_nodes()
archi = model.G.number_of_edges()
print(nodi, archi)

a,b=model.analisi_comp(230)
print(a,b)

c, d= model.ricerca_percorso(3000, 230)

print(c)
print(d)
