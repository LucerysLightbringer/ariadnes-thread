# Classe usata per salvare le distanze di ogni cella da una cella root arbitraria.
class Distances:

    # La cella arbitraria iniziale è root.
    # Il costruttore semplicemente inizializza un dizionario (cell,distance)
    # con distanza dalla root == 0.
    def __init__(self, root):

        self.root = root
        self._cells = {root: 0} 
    # ----------------------------------------------- #


    # Definisco la sintassi [i] per poter ottenere la distanza di una singola cella dalla root.
    # [i] = ..., dove ... è la distanza ritornata.
    # Restituisce None se non esiste.
    def __getitem__(self, cell):
        return self._cells.get(cell)
    # ----------------------------------------------- #


    # Definisco la sintassi [i] per poter settare la distanza di una singola cella dalla root.
    # [i] = k, dove k è la distanza da settare.
    def __setitem__(self, cell, distance):
        self._cells[cell] = distance
    # ----------------------------------------------- #


    # Ritorna la lista di tutte le distanze.
    # Utilizzo @property per poter usare getter e setter su _cells.key()
    # senza dover fare refactoring di codice precedente.
    @property
    def all_cells(self):
        # restituisce la “vista” delle chiavi; se le vuoi mutabili, fai list(self._cells)
        return self._cells.keys()
    # ----------------------------------------------- #


    # Utilizzando la matrice delle distanze pre-calcolata,
    # ricostruisce un cammino minimo per quel percorso (root <-> cell_goal).
    def shortest_path_to(self, cell_goal):

        current_cell = cell_goal
        backtrack = Distances(self.root) # calcola distanze dalla root
        backtrack[current_cell] = self[current_cell]

        # Finché non arrivo alla cella root
        while current_cell != self.root:

            # Itero su tutte le celle collegate alla cella corrente
            for neighbor in current_cell.links_as_dict():

                # Se una cella collegata ha distanza minore della cella corrente
                # è quella da cui si è arrivati
                if self[neighbor] < self[current_cell]:

                    # Rendo la cella corrente quella con distanza minore (neighbor),
                    # esco dal ciclo e ricomincio con la nuova cella corrente
                    backtrack[neighbor] = self[neighbor]
                    current_cell = neighbor
                    break

        return backtrack # dizionario (cell,distance)
    # ----------------------------------------------- #


    # Calcola la cella con distanza massima dalla root.
    def longest_path_from(self):

        max_distance = 0
        max_cell = self.root  # inizializza con la root, in caso non ci siano altre celle

        # Itera sul dizionario _cells che contiene (cella: distanza)
        for cell, dist in self._cells.items():

            if dist > max_distance:
                max_cell = cell
                max_distance = dist

        return max_cell, max_distance # ritorna coppia (cell,distance)
    # ----------------------------------------------- #
    
    
    