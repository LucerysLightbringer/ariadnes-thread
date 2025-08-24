# Overrides il metodo contents_of() per ritornare
# la distanza di ogni cella dalla root all'interno della
# rappresentazione ASCII della griglia.
import string

from distances import Distances
from grid import Grid


class DistanceGrid(Grid):

    def __init__(self, rows, columns):
        super().__init__(rows, columns) # creo griglia rows x columns
        self.distances = None           # dizionario {cell: distance}


    # Override del metodo contents_of() di Grid
    def contents_of(self, cell):

        # Traduci numeri 10...35 in lettere
        if self.distances and cell in self.distances:
            return self._int_to_base62(self.distances[cell])

        # Altrimenti riutilizza contents_of() di Grid
        return super().contents_of(cell)
    # ----------------------------------------------- #


    # Converte numeri interi in stringa base-62 (0...9 , a...z, A...Z).
    # Se il labirinto è più grande di 36 x 36, servono più caratteri.
    # Metodo static perché viene utilizzato direttamente
    # in contents_of()
    @staticmethod
    def _int_to_base62(num):

        if num < 0:
            raise ValueError("Number must be non-negative")

        if num == 0:
            return "0"

        # Salvo le cifre di num al contrario
        # digits = []
        digits = ""

        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        while num > 0:

            # Divido num/62 e salvo il modulo in rem
            num, rem = divmod(num, 62)

            # rem è tra 0...61, quindi prendiamo la cifra corrispondente
            # digits.append(alphabet[rem])
            digits = alphabet[rem] + digits

        # Invertiamo il risultato
        #return "".join(reversed(digits))
        return digits
    # ----------------------------------------------- #