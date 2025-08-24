from grid import Grid  # eredita da Grid
from distances import Distances


class ColoredGrid(Grid):


    def __init__(self, rows, columns):

        super().__init__(rows, columns)
        self._distances = None      # distanze
        self._maxdistance = 0       # distanza massima
    # ----------------------------------------------- #


    # Setter per la proprietà 'distances'.
    @property
    def distances(self):
        return self._distances
    # ----------------------------------------------- #


    # Si aspetta un oggetto Distances
    @distances.setter
    def distances(self, distances_obj: Distances):

        self._distances = distances_obj

        # Trova la cella più lontana e la sua distanza massima tramite longest_path_to(),
        # ritorna la cella e la sua distanza.
        if distances_obj:
            farthest_cell, self._maxdistance = distances_obj.longest_path_to()
        else:
            self._maxdistance = 0
    # ----------------------------------------------- #


    # Override metodo background_color
    def grid_background_color(self, cell):

        if not self._distances or self._distances[cell] is None:
            return None

        # Ottieni la distanza della cella.
        # Se non esiste ritorna None.
        distance = self._distances[cell]  # uso operatore [] : invoca __getitem__
        if distance is None:              # se la cella non è tra le distanze calcolate
            return None                   # ritorna bianco (default)

        # Quando distance è 0 (alla root o all'inizio del percorso), intensità massima.
        # Quando distance è _maxdistance (alla fine del percorso o la cella più lontana dallo start), intensità minima = 0.
        if self._maxdistance == 0:
            intensity = 0.0
        else:
            # intensity: 0 per distanza massima, 1 per la root
            intensity = (self._maxdistance - distance) / self._maxdistance

        smooth_exp = 0.5 # esponente per una transizione di colore più morbida
        interpolation_factor = max(0.0, min(1.0, intensity ** smooth_exp))

        color_start = (25, 220, 25)  # Verde chiaro per le celle vicine
        color_end = (0, 50, 0)       # Verde scuro per le celle lontane

        red = int(color_end[0] + (color_start[0] - color_end[0]) * interpolation_factor)
        green = int(color_end[1] + (color_start[1] - color_end[1]) * interpolation_factor)
        blue = int(color_end[2] + (color_start[2] - color_end[2]) * interpolation_factor)

        # Assicuriamoci che i valori RGB siano nel range 0-255
        red = max(0, min(255, red))
        green = max(0, min(255, green))
        blue = max(0, min(255, blue))

        return (red, green, blue)