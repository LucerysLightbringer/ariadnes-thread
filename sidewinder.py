import random


# Algoritmo di generazione dei labirinti Sidewinder.
# Decido casualmente se andare a est (aggiungendo la cella al gruppo)
# oppure tagliare a nord (in una cella causale del gruppo corrente).
# Dopo che ho tagliato a nord, sciogliamo il gruppo e continuo
# con le restanti celle della riga corrente. Dopo aver finito
# con la riga corrente, continuo per le altre righe.

class Sidewinder:

    @staticmethod
    def apply(grid):

        # Itera una riga per volta
        for row in grid.each_row():

            # Definisco un array group vuoto per ogni cella (solamente all'inizio)
            group = []

            # Itera su ogni cella della riga corrente
            for cell in row:

                # Aggiungo la cella corrente al gruppo
                group.append(cell)

                # Se ci troviamo sul bordo est, non possiamo andare
                # ancora più a est, quindi chiudiamo il gruppo
                east_edge = cell.east is None # bool

                # Se ci troviamo sul bordo nord, non possiamo andare
                # ancora più a nord, quindi chiudiamo il gruppo
                north_edge = cell.north is None # bool

                # Se non siamo sul bordo nord e a caso decidiamo di chiudere il gruppo
                # (piuttosto che continuare ad aggiungere celle ad est),
                # scegliamo una cella casuale del gruppo corrente,
                # collegandola verso nord (questo per mantere l'algoritmo casuale)
                is_group_closed = (east_edge or (not north_edge and random.randint(0,1) == 0)) # bool

                # Se non posso più aggiungere celle al gruppo
                if is_group_closed:

                    # Seleziono causalmente una cella dal gruppo corrente
                    new_cell = random.choice(group)

                    # Taglio a nord di questa cella,
                    # ovvero collego la cella creando un passaggio.
                    if new_cell.north:
                        new_cell.link(new_cell.north)

                    # Il gruppo corrente viene eliminato perché sceglierò una nuova cella
                    # dalla riga corrente
                    group.clear()

                else:
                    cell.link(cell.east) # Altrimenti mi collego ad est, creando un passaggio

        return grid