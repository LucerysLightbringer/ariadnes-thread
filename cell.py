from distances import Distances # per Dijkstra


# Classe base, rappresenta una singola cella della griglia.
# Definisce una cella come un insieme di coordinate 2D (row,column).
# Inoltre, per ogni cella vengono salvate una serie di informazioni:
# celle adiacenti (nord,sud,est,ovest)
# celle con cui è collegata (cioè con cui crea un passaggio)
class Cell:



    # Costruttore:
    # - creo una cella di posizione (row,column)
    # - con nessuna cella adiacente
    # - con nessuna cella collegata
    def __init__(self, r, c):

        self.row = r
        self.column = c

        self.north = None
        self.south = None
        self.east = None
        self.west = None

        # Utilizzo un dizionario booleano (valore di default = true)
        # per tenere traccia di quali celle sono collegate
        # alla cella corrente, ovvero se sono collegate da un passaggio
        self._links = {}
    # ----------------------------------------------- #



    # Collega la cella corrente self -> another_cell
    # Se bidirectional = true, allora collega anche another_cell -> self
    def link(self, another_cell, bidirectional=True):

        self._links[another_cell] = True

        if bidirectional:
            another_cell.link(self, False)

        return self
    # ----------------------------------------------- #



    # Scollega self da another_cell
    # Se bidirectional = true, allora scollega anche another_cell da self
    def unlink(self, another_cell, bidirectional=True):

        if another_cell in self._links:
            del self._links[another_cell]

        if bidirectional:
            another_cell.unlink(self, False)

        return self
    # ----------------------------------------------- #



    # Ritorna tutte le celle collegate alla cella corrente
    # Una funzione ritorna una lista, una un dizionario
    def links_as_list(self):
        return list(self._links.keys())

    def links_as_dict(self):
        return self._links.keys()
    # ----------------------------------------------- #



    # Ritorna true se la cella corrente è collegata ad un'altra cella
    def is_linked(self, another_cell):
        return another_cell in self._links
    # ----------------------------------------------- #



    # Restituisce tutte le celle adiacenti (quindi non per forza collegate)
    def all_neighbors(self):

        neighbors = []

        if self.north:
            neighbors.append(self.north)

        if self.south:
            neighbors.append(self.south)

        if self.east:
            neighbors.append(self.east)

        if self.west:
            neighbors.append(self.west)

        return neighbors
    # ----------------------------------------------- #



    # Algoritmo BFS per il calcolo delle distanze
    # di ogni cella dalla cella root
    # Complessità computazionale: O=(V + E) dove (V = RxC) ed (E = 4V) (circa)
    def distances(self):

        # Creo istanza di oggetto distances.
        # La root è la cella attuale (self) da cui tutte le distanze saranno calcolate.
        # distances[i] = (cell,distance_from_root)
        distances = Distances(self)

        # Array delle celle di frontiera, inizializzato con cella attuale (self)
        frontier = [self]

        # Finché ci sono celle nella frontiera.
        # Alla fine del loop, avremo calcolato la distanza di ogni cella dalla root.
        while frontier:

            # Salva tutte le celle non ancora visitate, che sono collegate
            # (esiste un passaggio) con le celle della frontiera attuale
            new_frontier = []

            # Per ogni cella nella frontiera
            for cell in frontier:

                # Per ogni cella collegata alla cella attuale
                # (ovvero per la quale esiste un passaggio)
                for linked in cell.links_as_list():

                    # Se la cella è già stata visitata,
                    # finisci l'attuale iterazione e passa alla prossima
                    # cella collegata
                    if distances[linked] is not None:
                        continue

                    # Se non è stata già visitata:
                    # Aumento la distanza della cella corrente + 1
                    distances[linked] = distances[cell] + 1

                    # Aggiungo alla frontiera la cella collegata attuale
                    new_frontier.append(linked)

            # Aggiorno la frontiera con le celle appena calcolate
            frontier = new_frontier

        return distances # hash table (cella, distanza da root)
    # ----------------------------------------------- #



    # Devo rendere le celle hashabili, altrimenti
    # non possono essere usate come chiavi nel dizionario
    # in DistanceGrid: self.distances = None
    def __hash__(self):
        return hash((self.row, self.column))
    # ----------------------------------------------- #



    # Devo rendere le celle comparabili, altrimenti
    # non possono essere usate come chiavi nel dizionario
    # in DistanceGrid: self.distances = None
    def __eq__(self, other):
        return (isinstance(other, Cell) and
                (self.row == other.row) and
                (self.column == other.column))
    # ----------------------------------------------- #



    # Rappresento la cella in formato leggibile
    def __str__(self):
        return f"({self.row}, {self.column})"
    # ----------------------------------------------- #



    # Rappresento la cella per debugging
    def __repr__(self):
        return f"({self.row}, {self.column})"
    # ----------------------------------------------- #
    
    
    