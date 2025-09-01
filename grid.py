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

        self._distances = None      # distanze di ogni cella da una root arbitraria
        self._maxdistance = 0       # distanza massima dalla root
    # ----------------------------------------------- #


    # Creo una nuova cella in ogni singola posizione di (row,column).
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


    # Getter per la proprietà 'distances'.
    @property
    def distances(self):
        return self._distances
    # ----------------------------------------------- #


    # Setter per 'distances'
    @distances.setter
    def distances(self, distances_obj: Distances):

        self._distances = distances_obj

        # Trova la cella più lontana e la sua distanza massima tramite longest_path_to(),
        # ritorna la cella e la sua distanza.
        if distances_obj:
            farthest_cell, self._maxdistance = distances_obj.longest_path_from()
        else:
            self._maxdistance = 0
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

        for cell in self.each_cell():

            # Controlla se la cella ha esattamente una sola cella collegata
            # ovvero è un vicolo cieco
            if len(cell.links_as_dict()) == 1:
                deadends.append(cell)

        return deadends
    # ----------------------------------------------- #


    # Stampa il labirinto
    def to_png(self,
               cell_size=10,
               background_type="plain_white",
               show_distances=False, distances_obj=None,
               show_solution=False, solution_path=None,
               start_cell=None, end_cell=None):

        # Creo PNG default
        img_width = cell_size * self.columns
        img_height = cell_size * self.rows
        img = Image.new("RGB", (img_width + 1, img_height + 1), "white")
        draw = ImageDraw.Draw(img)

        # Carica i font per le distanze solamente se richiesto
        if show_distances and distances_obj:

            try:
                font_normal = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=9)
                font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=8)
                current_font = font_normal
            except IOError:
                font_default = ImageFont.load_default()
                current_font = font_default


        # Itero ogni cella e ne calcolo il colore
        for cell in self.each_cell():

            # Vertice della cella "pixel"
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            # Colore cella default
            cell_color = None

            # Calcola colore della cella in base alla distanza
            # come un gradiente tra due colori
            if self.distances:

                dist = self.distances[cell]

                if dist is not None and self._maxdistance > 0:

                    intensity = (self._maxdistance - dist) / self._maxdistance
                    smooth_exp = 0.5
                    interpolation = max(0.0, min(1.0, intensity ** smooth_exp))

                    color_start = (25, 220, 25) # verde chiaro
                    color_end = (0, 50, 0)      # verde scuro

                    red = int(color_end[0] + (color_start[0] - color_end[0]) * interpolation)
                    green = int(color_end[1] + (color_start[1] - color_end[1]) * interpolation)
                    blue = int(color_end[2] + (color_start[2] - color_end[2]) * interpolation)

                    cell_color = (red, green, blue)
            # ------------------------------------- #

            # Se non calcolo il colore in base alle distanza,
            # mi riduco a due opzioni standard
            if not cell_color:

                if background_type == "checkerboard":
                    if (cell.row + cell.column) % 2 == 0:
                        cell_color = (255, 255, 255)
                    else:
                        cell_color = (220, 220, 220)
                elif background_type == "plain_white":
                    cell_color = (255, 255, 255)


            # Coloro effettivamente la cella
            if cell_color:
                draw.rectangle([x1, y1, x2, y2], fill=cell_color)


            # Disegna le mura sottili attorno ad ogni cella
            thin_wall_color = (50, 50, 50) # grigio
            thin_wall_width = 1
            draw.line([(x1, y1), (x2, y1)], fill=thin_wall_color, width=thin_wall_width)
            draw.line([(x1, y1), (x1, y2)], fill=thin_wall_color, width=thin_wall_width)
            draw.line([(x2, y1), (x2, y2)], fill=thin_wall_color, width=thin_wall_width)
            draw.line([(x1, y2), (x2, y2)], fill=thin_wall_color, width=thin_wall_width)


            # Disegna i numeri delle distanze (se richiesto)
            if distances_obj and distances_obj[cell] is not None:

                text_color = (240, 50, 255) # viola
                x = cell.column * cell_size + cell_size // 4
                y = cell.row * cell_size + cell_size // 4

                if distances_obj[cell] >= 1000:
                    current_font = font_small

                draw.text((x, y), str(distances_obj[cell]), fill=text_color, font=current_font)


        # Disegna le mura effettive che compongono il labirinto
        thick_wall_width = 3
        thick_wall_color = (0, 0, 0) # nero

        for cell in self.each_cell():

            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            if not cell.north:
                draw.line([(x1, y1), (x2, y1)], width=thick_wall_width, fill=thick_wall_color)
            if not cell.west:
                draw.line([(x1, y1), (x1, y2)], width=thick_wall_width, fill=thick_wall_color)
            if not cell.is_linked(cell.east):
                draw.line([(x2, y1), (x2, y2)], width=thick_wall_width, fill=thick_wall_color)
            if not cell.is_linked(cell.south):
                draw.line([(x1, y2), (x2, y2)], width=thick_wall_width, fill=thick_wall_color)


        # Disegna il percorso della soluzione (se richiesto)
        if show_solution and solution_path:

            # Definisco start_cell e end_cell di default
            # se non vengono esplicitate
            if start_cell is None:
                start_cell = solution_path[0]

            if end_cell is None:
                end_cell = solution_path[-1]

            path_color = (240, 50, 255)  # viola
            start_color = (255, 200, 0)  # giallo
            end_color = (0, 255, 255)    # ciano

            # Disegna il percorso
            for i in range(len(solution_path) - 1):

                cell1 = solution_path[i]
                cell2 = solution_path[i + 1]

                cx1 = cell1.column * cell_size + cell_size // 2
                cy1 = cell1.row * cell_size + cell_size // 2
                cx2 = cell2.column * cell_size + cell_size // 2
                cy2 = cell2.row * cell_size + cell_size // 2

                draw.line((cx1, cy1, cx2, cy2), fill=path_color, width=max(1, cell_size // 10))


            try:
                font_big = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=15)
                current_font = font_big
            except IOError:
                font_default = ImageFont.load_default()
                current_font = font_default

            text_color = (240, 50, 255) # viola

            if start_cell:
                sx1 = start_cell.column * cell_size
                sy1 = start_cell.row * cell_size
                sx2 = (start_cell.column + 1) * cell_size
                sy2 = (start_cell.row + 1) * cell_size
                draw.rectangle((sx1 + 1, sy1 + 1, sx2 - 1, sy2 - 1), fill=start_color)
                text_x = start_cell.column * cell_size + cell_size // 5
                text_y = start_cell.row * cell_size + cell_size // 5
                draw.text((text_x, text_y), "S", fill=text_color, font=current_font)

            if end_cell:
                ex1 = end_cell.column * cell_size
                ey1 = end_cell.row * cell_size
                ex2 = (end_cell.column + 1) * cell_size
                ey2 = (end_cell.row + 1) * cell_size
                draw.rectangle((ex1 + 1, ey1 + 1, ex2 - 1, ey2 - 1), fill=end_color)
                text_x = end_cell.column * cell_size + cell_size // 5
                text_y = end_cell.row * cell_size + cell_size // 5
                draw.text((text_x, text_y), "E", fill=text_color, font=current_font)

        return img
        # ------------------------------------------------------------------------------------- #