import random

class AldousBroder:

    @staticmethod
    def apply(grid):

        # Inizializza un set con tutte le celle della griglia.
        # Questo ci permette di controllare in O(1) se una cella è già stata visitata.
        unvisited = set(grid.each_cell())

        # Scegli una cella casuale come punto di partenza.
        cell = grid.random_cell()

        # La cella di partenza è considerata "visitata" e fa parte del labirinto.
        unvisited.remove(cell)

        # Finché ci sono celle non visitate
        while unvisited:  # La condizione diventa semplicemente se il set non è vuoto

            # Scelgo una cella adiacente casuale alla cella corrente
            neighbor_cell = random.choice(cell.all_neighbors())

            # Se la cella adiacente è ancora nel set delle "non visitate"
            # significa che la stiamo visitando per la prima volta con questa passeggiata.
            if neighbor_cell in unvisited:

                # La colleghiamo alla cella corrente.
                cell.link(neighbor_cell)

                # La rimuoviamo dal set delle non visitate.
                unvisited.remove(neighbor_cell)

            # Spostiamo la cella corrente all'adiacente per il prossimo passo della passeggiata casuale.
            cell = neighbor_cell

        return grid