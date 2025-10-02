import random


# Algoritmo di generazione RecursiveDivision.
# Crea una griglia vuota (senza muri) collegando ogni cella con le sue adiacenti.
# Sceglie casualmente se dividere la regione attuale orizzontalmente o verticalmente.
# Costruisce un muro lungo la linea di divisione scelta, scollegando ogni cella
# da quella sud oppure est.
# Lascia una cella casuale come passaggio, lasciando la cella collegata.
# Effettua ricorsivamente gli step per le due nuove aree create.
class RecursiveDivision:


    @staticmethod
    def apply(grid):

        # Collega ogni cella con le adiacenti,
        # creando una griglia completamente aperta.
        for cell in grid.each_cell():
            for neighbor in cell.all_neighbors():
                cell.link(neighbor, bidirectional=False)

        # Inizia divisione ricorsiva
        RecursiveDivision._divide(grid, 0, 0, grid.rows, grid.columns)

        return grid


    # Metodo interno per la divisione
    @staticmethod
    def _divide(grid, row, col, rows, columns):

        # Non puoi dividere un area troppo piccola
        if rows <= 1 or columns <= 1:
            return

        # Dividi orizzontalmente o verticalmente
        if rows >= columns:
            RecursiveDivision._divide_horizontal(grid, row, col, rows, columns)
        else:
            RecursiveDivision._divide_vertical(grid, row, col, rows, columns)


    # Metodo interno per dividere orizzontalmente
    @staticmethod
    def _divide_horizontal(grid, row, col, rows, columns):

        # Scegli riga casuale dove costruire il muro.
        # Indica l'indice a NORD del muro
        wall_south = random.randrange(rows - 1)

        # Scegli colonna casuale dove scavare il passaggio nel muro
        passage = random.randrange(columns)

        # Itera lungo la linea scelta e crea il muro
        for position in range(columns):

            # Se ti trovi sul passaggio, ignora
            if passage == position:
                continue

            # Crea il muro rimuovendo i link tra celle
            cell = grid[row + wall_south, col + position]
            if cell and cell.south:
                cell.unlink(cell.south)


        # Ricorsione sulle nuove aree create
        RecursiveDivision._divide(grid, row, col, wall_south + 1, columns)
        RecursiveDivision._divide(grid, row + wall_south + 1, col, rows - wall_south - 1, columns)



    # Metodo interno per dividere verticalmente
    @staticmethod
    def _divide_vertical(grid, row, col, rows, columns):

        # Scegli colonna casuale dove costruire il muro.
        # Indica l'indice a OVEST del muro
        wall_east = random.randrange(columns - 1)

        # Scegli riga casuale dove scavare il passaggio nel muro
        passage = random.randrange(rows)

        # Itera lungo la linea scelta e crea il muro
        for position in range(rows):

            # Se ti trovi sul passaggio, ignora
            if passage == position:
                continue

            # Crea il muro rimuovendo i link tra celle
            cell = grid[row + position, col + wall_east]
            if cell and cell.east:
                cell.unlink(cell.east)


        # Ricorsione sulle nuove aree create
        RecursiveDivision._divide(grid, row, col, rows, wall_east + 1)
        RecursiveDivision._divide(grid, row, col + wall_east + 1, rows, columns - wall_east - 1)