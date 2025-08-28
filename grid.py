import math
from random import randrange
from PIL import Image, ImageDraw, ImageFont  # Libreria Pillow per salvare come immagine PNG il labirinto
from cell import Cell
from distances import Distances


# Nessun _	| Pubblico, per uso generale
# _nome	    | Privato per convenzione (ma posso comunque accederlo)
# __nome	| Privato con "protezione" da override
# __nome__	| Metodo speciale (usare solo come override)


# Rappresenta una griglia.
# Definisce una griglia di grandezza (rows x columns).
class Grid:
    
    

    # Costruttore:
    # creo una griglia di dimensione (rows, columns)
    # creo una serie di celle per ogni posizione della griglia
    # inizializzo le celle e ogni adiacente di ogni cella
    def __init__(self, rows, columns):

        # Setto la dimensione della griglia
        self.rows = rows
        self.columns = columns

        # Creo griglia vuota
        self._grid = self._create_grid()

        # Setto gli adiacenti di ogni cella
        self._configure_cells()
    # ----------------------------------------------- #



    # Creo una nuova cella in ogni singola posizione
    # di (row,column) come un array 2D di celle (quindi una matrice).
    # Ritorno quindi la matrice.
    def _create_grid(self):

        grid = []

        for row in range(self.rows):

            row_list = []

            for col in range(self.columns):
                cell = Cell(row, col)
                row_list.append(cell)

            grid.append(row_list)

        return grid
    # ----------------------------------------------- #



    # Definisce ogni cella adiacente (neighbor) per ogni cella della griglia.
    def _configure_cells(self):

        for cell in self.each_cell():

            row, col = cell.row, cell.column

            cell.north = self[row - 1, col]
            cell.south = self[row + 1, col]
            cell.west  = self[row, col - 1]
            cell.east  = self[row, col + 1]
    # ----------------------------------------------- #



    # Definisco la sintassi [i][j] per poter ottenere una singola cella.
    # Se la coppia di indici [i][j] è fuori dal range della griglia, ritorno None.
    def __getitem__(self, position):

        row, column = position

        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self._grid[row][column]

        return None
    # ----------------------------------------------- #



    # Ritorna una cella casuale della griglia.
    def random_cell(self):

        row = randrange(self.rows)
        column = randrange(self.columns)

        return self[row, column]
    # ----------------------------------------------- #



    # Ritorna la grandezza della griglia.
    def size(self):
        return self.rows * self.columns
    # ----------------------------------------------- #



    # Ritorna le righe della griglia una alla volta.
    def each_row(self):
        for row in self._grid:
            yield row
    # ----------------------------------------------- #



    # Itero su tutte le celle della griglia e ritorno una cella alla volta.
    def each_cell(self):
        for row in self.each_row():
            for cell in row:

                # Se la cella esiste effettivamente, la ritorno
                if cell:
                    yield cell
    # ----------------------------------------------- #



    # Raggruppa i vicoli ciechi, ovvero le singole celle
    # che hanno solamente un'altra cella collegata.
    def deadends(self):

        deadends = []

        # Itera su tutte le celle della griglia
        for cell in self.each_cell():

            # Controlla se la cella ha esattamente una sola cella collegata
            # ovvero è un vicolo cieco
            if len(cell.links_as_dict()) == 1:
                deadends.append(cell)

        return deadends
    # ----------------------------------------------- #



    # Colore di sfondo di una cella, sovrascritto in ColoredGrid
    def grid_background_color(self, cell):
        return None  # di default non vengono colorate
    # ----------------------------------------------- #



    # Disegna il labirinto base
    def _draw_base_maze_image(self, cell_size=10, background_type="plain_white"):

        img_width = cell_size * self.columns
        img_height = cell_size * self.rows
        img = Image.new("RGB", (img_width + 1, img_height + 1), "white")
        draw = ImageDraw.Draw(img)


        for cell in self.each_cell():

            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            # Se scelgo come tipo di colore di background scacchiera, alterno
            # celle bianche e nere
            if background_type == "checkerboard":
                if (cell.row + cell.column) % 2 == 0:
                    background_color = (255, 255, 255)  # bianco
                else:
                    background_color = (220, 220, 220)  # grigio

                draw.rectangle([x1, y1, x2, y2], fill=background_color)

            # Se scelgo come tipo di colore di background bianco,
            # non faccio nulla perché l'immagine viene generata bianca di default

        return img
    # ----------------------------------------------- #



    #
    def to_png(self,
               cell_size=10, inset=0,
               background_type="plain_white", full_space_color=True,
               thin_wall_color=(0, 0, 0, 50), thin_wall_width=1):

        img = self._draw_base_maze_image(cell_size, background_type)
        draw = ImageDraw.Draw(img)

        # Disegna i colori di sfondo specifici delle celle (es. da ColoredGrid)
        for cell in self.each_cell():

            back_color = self.grid_background_color(cell)

            if back_color:

                x1 = cell.column * cell_size
                y1 = cell.row * cell_size
                x2 = (cell.column + 1) * cell_size
                y2 = (cell.row + 1) * cell_size

                # Riempi l'intera cella con il colore specificato
                if full_space_color:

                    draw.rectangle([x1, y1, x2, y2], fill=back_color)

                    # Disegna bordi sottili sopra la cella colorata
                    draw.line([(x1, y1), (x2, y1)], fill=thin_wall_color, width=thin_wall_width)  # Nord
                    draw.line([(x1, y1), (x1, y2)], fill=thin_wall_color, width=thin_wall_width)  # Ovest
                    draw.line([(x2, y1), (x2, y2)], fill=thin_wall_color, width=thin_wall_width)  # Est
                    draw.line([(x1, y2), (x2, y2)], fill=thin_wall_color, width=thin_wall_width)  # Sud

                # Applica l'inset per colorare solo una porzione della cella
                else:

                    effective_inset = min(inset, cell_size // 2 - 1)
                    colored_x1 = x1 + effective_inset
                    colored_y1 = y1 + effective_inset
                    colored_x2 = x2 - effective_inset
                    colored_y2 = y2 - effective_inset

                    if colored_x2 > colored_x1 and colored_y2 > colored_y1:
                        draw.rectangle([colored_x1, colored_y1, colored_x2, colored_y2], fill=back_color)

        # Disegna le pareti spesse del labirinto
        wall_width = 3
        wall_color = (0, 0, 0) # Nero per i muri principali

        for cell in self.each_cell():

            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            if not cell.north:
                draw.line([(x1, y1), (x2, y1)], width=wall_width, fill=wall_color)
            if not cell.west:
                draw.line([(x1, y1), (x1, y2)], width=wall_width, fill=wall_color)
            if not cell.is_linked(cell.east):
                draw.line([(x2, y1), (x2, y2)], width=wall_width, fill=wall_color)
            if not cell.is_linked(cell.south):
                draw.line([(x1, y2), (x2, y2)], width=wall_width, fill=wall_color)

        return img
    # ----------------------------------------------- #



    # Crea una immagine PNG della griglia con i numeri delle distanze.
    def to_png_distances(self, distances_obj: Distances,
                         cell_size=10, inset=0,
                         background_type="plain_white"):

        img = self.to_png(cell_size=cell_size, inset=inset, background_type=background_type)
        draw = ImageDraw.Draw(img)

        # Carica il font desiderato, oppure seleziona quello di default
        try:
            font_normal = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=9)
            font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=8)
            current_font = font_normal
        except IOError:
            font_default = ImageFont.load_default()
            current_font = font_default

        text_color = (240, 50, 255) # viola

        for cell in distances_obj.all_cells: # Usa all_cells dal Distances object

            dist = distances_obj[cell]

            if dist is not None:

                # Centra il testo nella cella
                x = cell.column * cell_size + cell_size // 4
                y = cell.row * cell_size + cell_size // 4

                if dist >= 1000:
                    current_font = font_small

                draw.text((x, y), str(dist), fill=text_color, font=current_font)

        return img
    # ----------------------------------------------- #



    # Crea una immagine PNG della griglia con il percorso risolutivo.
    def to_png_solution_path(self,
                             cell_size=10, inset=0,
                             solution_path=None, start_cell=None, end_cell=None,
                             background_type="plain_white"):

        img = self.to_png(cell_size=cell_size, inset=inset, background_type=background_type)
        draw = ImageDraw.Draw(img)


        if start_cell is None:
            start_cell = self._grid[0][0]

        if end_cell is None:
            end_cell = self._grid[self.rows-1][self.columns-1]

        path_color = (255, 255, 255) # bianco per il percorso
        start_color = (255, 200, 0)  # giallo per la radice
        end_color = (0, 255, 255)    # ciano per la cella obiettivo

        # Disegna il percorso della soluzione se fornito
        if solution_path:

            for i in range(len(solution_path) - 1):

                cell1 = solution_path[i]
                cell2 = solution_path[i + 1]

                cx1 = cell1.column * cell_size + cell_size // 2
                cy1 = cell1.row * cell_size + cell_size // 2
                cx2 = cell2.column * cell_size + cell_size // 2
                cy2 = cell2.row * cell_size + cell_size // 2

                draw.line((cx1, cy1, cx2, cy2), fill=path_color, width=max(1, cell_size // 10))


        # Colora le celle di inizio e fine
        if start_cell:
            sx1 = start_cell.column * cell_size
            sy1 = start_cell.row * cell_size
            sx2 = (start_cell.column + 1) * cell_size
            sy2 = (start_cell.row + 1) * cell_size
            draw.rectangle((sx1 + 1, sy1 + 1, sx2 - 1, sy2 - 1), fill=start_color)

        if end_cell:
            ex1 = end_cell.column * cell_size
            ey1 = end_cell.row * cell_size
            ex2 = (end_cell.column + 1) * cell_size
            ey2 = (end_cell.row + 1) * cell_size
            draw.rectangle((ex1 + 1, ey1 + 1, ex2 - 1, ey2 - 1), fill=end_color)


        return img
    # ----------------------------------------------- #