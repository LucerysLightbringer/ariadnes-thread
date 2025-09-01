import random


# Algoritmo di generazione dei labirinti Recursive Backtracker,
# funziona analogamente a Depth-First Search ma in modo randomizzato.
# Costruisce il labirinto "scavando" percorsi da una cella all'altra.
# Sceglie una cella casuale iniziale, cerca tra le celle adiacenti e collega quelle
# non visitate. Quando non ci sono celle adiacenti non visitate, l'algoritmo torna indietro
# lungo il percorso fino a trovare una cella con vicini non visitati.
# - Complessità computazionale: O=(N), dove N sono le celle della griglia. Le visita tutte esattamente una volta.
#   Ogni cella viene visitata una volta, perché quando gli adiacenti (neighbors) di una cella sono linkati, la cella
#   viene pushata o poppata nello stack. Per ogni cella l'algoritmo controlla tutti gli adiacenti per trovare quelli
#   non linkati che è una costante (massimo 4 per ogni cella).
#
# - Efficienza di memoria: O=(N), dove N sono le celle della griglia, a causa dello stack.
class RecursiveBacktracker:

    @staticmethod
    def apply(grid):

        # Scegli cella casuale
        cell = grid.random_cell()

        # Inizializzo stack
        stack = []
        stack.append(cell)

        while stack:

            # Ottieni l'ultima cella nello stack senza rimuoverla
            current_cell = stack[-1]

            # Cerca le celle adiacenti non ancora linkate
            unlinked_neighbors = [
                neighbor for neighbor in current_cell.all_neighbors()
                if not neighbor.all_linked()
            ]

            # Se non ci sono celle adiacenti non linkati,
            # rimuovi la cella in cima allo stack,
            # ovvero la cella corrente
            if not unlinked_neighbors:
                stack.pop()
            else:
                # Scelgo casualmente una cella adiacente
                cell_neighbor = random.choice(unlinked_neighbors)

                # Collego la cella corrente alla cella adiacente scelta
                current_cell.link(cell_neighbor)

                # Inserisco nello stack la cella adiacente
                stack.append(cell_neighbor)

        return grid