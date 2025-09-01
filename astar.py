import heapq  # coda di priorità (min-heap)


class AStar:


    @staticmethod
    def _manhattan_distance(cell1, cell2):
        return abs(cell1.row - cell2.row) + abs(cell1.column - cell2.column)

    @staticmethod
    def apply(grid, root, goal_cell):

        # Contatore tie breaker per evitare conflitti con coda di priorità
        tie_breaker_counter = 0

        # Coda di priorità che contiene le celle da esplorare.
        # Le celle con f_score più basso hanno priorità più alta.
        open_set = []

        # La tupla inserita nell'heap è (f_score, tie_breaker_counter, cell).
        # tie_breaker_counter agisce come tie-breaker per due valori f_score uguali.
        # Inseriamo la cella di partenza (root).
        heapq.heappush(open_set, (AStar._manhattan_distance(root, goal_cell), tie_breaker_counter, root))
        tie_breaker_counter += 1  # Incrementa il contatore per il prossimo inserimento.

        # Dizionario per ricostruire il percorso
        path = {}

        # g_score è il costo del percorso dalla cella di partenza alla cella corrente.
        # Inizializziamo tutti i costi a infinito.
        g_score = {cell: float('inf') for cell in grid.each_cell()}
        g_score[root] = 0 # costo per raggiungere la partenza da sé stessa è 0.

        # f_score è il costo totale stimato f(n) = g(n) + h(n)
        # Inizializziamo tutti i costi a infinito.
        f_score = {cell: float('inf') for cell in grid.each_cell()}
        f_score[root] = AStar._manhattan_distance(root, goal_cell)


        # Finché ci sono celle da esplorare
        while open_set:

            # Estrae dalla coda la cella con l'f_score più basso.
            # Con tie-breaker, se due cell hanno lo stesso f_score, viene estratta quella inserita prima.
            # (Il contatore viene ignorato usando '_' perché serve solo per l'ordinamento nell'heap)
            current_f_score, _, current_cell = heapq.heappop(open_set)

            # Se la cella attuale è la cella obiettivo, abbiamo trovato il percorso
            if current_cell == goal_cell:

                # Ricostruiamo il percorso ripercorrendolo al contrario
                solution_path = []
                temp = goal_cell

                while temp in path:
                    solution_path.append(temp)
                    temp = path[temp]

                solution_path.append(root)
                return solution_path[::-1] # inverto il percorso

            # Se la cella attuale non è la cella obiettivo,
            # visito le celle collegate a quella attuale
            for neighbor in current_cell.all_linked():

                # Il costo per raggiungere la cella adiacente attraverso la cella corrente.
                # Nel nostro caso (labirinto ortogonale), costo unitario.
                tentative_g_score = g_score[current_cell] + 1


                # Se questo percorso per la cella adiacente è più corto
                # di quello precedente
                if tentative_g_score < g_score[neighbor]:

                    # Aggiorno scores della cella adiacente
                    path[neighbor] = current_cell
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + AStar._manhattan_distance(neighbor, goal_cell)

                    # Aggiungiamo la cella adiacente alla coda di priorità per esaminarla,
                    # usando il nuovo f_score e il contatore come tie-breaker.
                    heapq.heappush(open_set, (f_score[neighbor], tie_breaker_counter, neighbor))
                    tie_breaker_counter += 1  # Incrementa il contatore dopo ogni push

        # Se il ciclo finisce e non abbiamo raggiunto la goal cell, non esiste il percorso
        return []
