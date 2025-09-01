import random


# Algoritmo di generazione Binary Tree.
# Partendo da una cella casuale, ed iterando per ogni cella della griglia:
# se la cella ha una adiacente a nord, posso tagliare il muro a nord
# se la cella ha una adiacente a est, posso tagliare il muro a est
# scelgo casualmente tra le due opzioni per il taglio
# ovviamente non taglio sulle celle dei bordi
class BinaryTree:

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