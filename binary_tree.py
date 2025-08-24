import random


# Algoritmo di generazione Binary Tree.
# Partendo da una cella casuale, ed iterando per ogni cella della griglia:
# se la cella ha una adiacente a nord, posso tagliare il muro a nord
# se la cella ha una adiacente a est, posso tagliare il muro a est
# scelgo casualmente tra le due opzioni per il taglio
# ovviamente non taglio sulle celle dei bordi

# Complessità computazionale: O=(N), dove N sono le celle della griglia.
# Efficienza di memoria: O=(N), dove N sono le celle della griglia.
class BinaryTree:

    # Bias di BinaryTree:
    # - La riga più a nord è sempre un passaggio ininterrotto.
    # - La colonna più a est è sempre un passaggio ininterrotto.
    # - Se parto dalla cella sud-ovest e cerco di raggiungere la cella nord-est, il cammino sarà sempre simile.
    #   (Tenderà ad essere lungo una diagonale, oppure lungo la colonna est).
    #   Infatti ogni cella avrà un'uscita nord o est, quindi ci si può sempre muovere in direzione nord-est.


    # Metodo statico, non ho bisogno di instanziare una classe BinaryTree.
    @staticmethod
    def apply(grid):

        # Itera su ogni cella
        for cell in grid.each_cell():

            # Definisco array neighbors vuoto
            # per ogni cella (solamente all'inizio), ovvero
            # la lista delle celle adiacenti.
            neighbors = []

            # Se la cella ha una cella adiacente nord
            # puoi aggiungerla alla lista delle celle adiacenti
            if cell.north:
                neighbors.append(cell.north)

            # Se la cella ha una cella adiacente est
            # puoi aggiungerla alla lista delle celle adiacenti
            if cell.east:
                neighbors.append(cell.east)

            # Sono sicuro che posso andare a nord o est.
            # Scelgo una cella a caso tra le due e mi linko ad essa,
            # creando un passaggio.
            if neighbors:
                neighbor = random.choice(neighbors)
                cell.link(neighbor)

        return grid