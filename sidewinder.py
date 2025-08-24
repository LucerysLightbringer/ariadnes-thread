import random


# Algoritmo di generazione dei labirinti Sidewinder.
# Partendo da una cella casuale, ed iterando per ogni cella della griglia,
# ma una riga per volta, :
# - Decido casualmente se andare a est (aggiungendo la cella al gruppo)
#   oppure tagliare a nord (in una cella causale del gruppo corrente).
#   Dopo che ho tagliato a nord, sciogliamo il gruppo e continuo
#   con le restanti celle della riga corrente. Dopo aver finito
#   con la riga corrente, continuo per le altre righe.

# - Complessità computazionale: O=(N), dove N sono le celle della griglia.
# - Efficienza di memoria: O=(N + K), dove N sono le celle della griglia e K l'array group
#   Ha solamente bisogno di abbastanza memoria per rappresentare una singola cella ad ogni istante,
#   e per ogni cella ha bisogno di salvare il gruppo di cui fa parte, che risulta in un array che però
#   viene cancellato ogni volta che si cambia gruppo, quindi diventa una costante.
class Sidewinder:

    # Bias di Sidewinder:
    # - La riga più a nord è sempre un passaggio ininterrotto.
    # - La colonna più a est potrebbe essere un passaggio ininterrotto, ma meno spesso rispetto a Binary Tree.
    # - Se parto dalla cella sud-ovest e cerco di raggiungere la cella nord-est, il cammino sarà sempre simile.
    #   Infatti ogni gruppo orizzontale di celle avrà esattamente un'uscita nord, quindi ci si può sempre muovere in direzione nord-est.


    # Metodo statico, non ho bisogno di instanziare una classe Sidewinder.
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

                    # Taglio a nord di questa cella, ovvero linko la cella
                    # creando un passaggio.
                    if new_cell.north:
                        new_cell.link(new_cell.north)

                    # Il gruppo corrente viene eliminato perché sceglierò una nuova cella
                    # dalla riga corrente
                    group.clear()

                else:
                    cell.link(cell.east) # Altrimenti mi linko ad est, creando un passaggio

        return grid