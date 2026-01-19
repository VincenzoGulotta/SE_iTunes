import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        self._view.lista_visualizzazione_1.controls.clear()
        soglia = self._view.txt_durata.value
        try:
            if soglia.isdigit():
                nodi, archi = self._model.create_graph(int(soglia))
                self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato: {nodi} album e {archi} archi"))
                self._view.update()
        except Exception:
            self._view.show_alert("Inserisci un numero")
            return
        self._view.dd_album.options.clear()
        lista_album = self._model.riempi_dd_album()
        for coppia in lista_album:
            album_id = coppia[0]
            album = coppia[1]
            self._view.dd_album.options.append(ft.DropdownOption(key = album_id, text = album))
        self._view.pulsante_analisi_comp.disabled = False
        self._view.update()


    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""


    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        self._view.lista_visualizzazione_2.controls.clear()
        album_id = int(self._view.dd_album.value)
        num_connessi, totale = self._model.analisi_comp(album_id)
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione componente: {num_connessi}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione totale: {totale:.2f}"))
        self._view.pulsante_set_album.disabled = False
        self._view.update()



    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        self._view.lista_visualizzazione_3.controls.clear()
        soglia = self._view.txt_durata_totale.value
        try:
            soglia = int(self._view.txt_durata_totale.value)
            album_id = int(self._view.dd_album.value)
            percorso, peso = self._model.ricerca_percorso(soglia, album_id)
            self._view.lista_visualizzazione_3.controls.append(ft.Text
                                                               (f"Set trovato: {len(percorso)} album, durata {peso:.2f} minuti"))
            for i in range(len(percorso)):
                self._view.lista_visualizzazione_3.controls.append(ft.Text
                                                                   (f"- {percorso[i]} ({percorso[i].minuti:.2f})"))
            self._view.update()

        except Exception:
            self._view.show_alert("Inserisci un numero valido")