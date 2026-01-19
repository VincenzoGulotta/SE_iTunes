from collections import deque

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.albums = None
        self.connessi = None
        self.percorso = []
        self.peso = 0

    def create_graph(self, soglia):
        self.G.clear()
        self.albums = DAO.get_album(soglia)
        for album_id in self.albums.keys():
            album = self.albums[album_id]
            self.G.add_node(album)

        connessioni = DAO.get_connessioni(soglia)
        playlist_ids = connessioni.keys()
        for playlist_id in playlist_ids:
            lista_album = connessioni[playlist_id]
            for album_id_1 in lista_album:
                for album_id_2 in lista_album:
                    if album_id_1 != album_id_2:
                        album1 = self.albums[album_id_1]
                        album2 = self.albums[album_id_2]
                        self.G.add_edge(album1, album2)

        nodi = self.G.number_of_nodes()
        archi = self.G.number_of_edges()

        return nodi, archi

    def riempi_dd_album(self):
        lista = []
        for album_id in self.albums.keys():
            album = self.albums[album_id]
            coppia = [album_id, album]
            lista.append(coppia)

        return lista

    def analisi_comp(self, album_id):
        self.connessi = []  # Lista visitati
        album = self.albums[album_id]
        not_visited = deque([album])  # Lista non visitati
        while not_visited:  # Fino a quando la lista non visitati non si svuota
            nodo = not_visited.popleft()  # Prendi il primo nodo tra i non visitati, salvalo e rimuovilo
            for nuovo_nodo in self.G.neighbors(nodo):  # Per tutti i nodi adiacenti al nodo salvato
                if nuovo_nodo not in self.connessi and nuovo_nodo != album:  # Se il nodo non è tra i visitati ed è diverso dal
                                                        # nodo di partenza
                    self.connessi.append(nuovo_nodo)  # Aggiungi il nodo ai visitati
                    not_visited.append(nuovo_nodo)  # Aggiungi il nodo per ultimo ai non visitati

        totale = album.minuti
        for nuovo_album in self.connessi:
            totale += nuovo_album.minuti
        return len(self.connessi)+1, totale

    def ricerca_percorso(self, soglia, album_id):
        album = self.albums[album_id]
        peso = album.minuti
        self.ricorsione([album],peso ,soglia, album)

        print(self.percorso)
        print(self.peso)
        return self.percorso, self.peso

    def ricorsione(self, percorso_parziale, peso_parziale, soglia, vecchio_album):
        if len(percorso_parziale) > len(self.percorso) and peso_parziale < soglia:
            self.percorso = percorso_parziale
            self.peso = peso_parziale

        elif peso_parziale > soglia:
            return

        for nuovo_album in self.G.neighbors(vecchio_album):
            if nuovo_album not in percorso_parziale:
                nuovo_percorso = list(percorso_parziale)
                nuovo_percorso.append(nuovo_album)
                peso = nuovo_album.minuti
                self.ricorsione(nuovo_percorso, peso_parziale + peso, soglia, nuovo_album)







