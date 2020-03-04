#Vektor-Klasse

import math

class Vector(object):
    def __init__(self, *args):
        #default (0, 0), sonst beliebig
        if len(args) == 0:
            self.values = (0, 0)
        elif len(args) == 1:
            self.values = [val for val in args[0]]
        else:
            self.values = args

    def norm(self):
        #betrag
        return math.sqrt(sum(x ** 2 for x in self))

    def argument(self):
        #winkel von x achse zum vektor, gegen den uhrzeigersinn auf der xy ebene
        arg_in_rad = math.acos(Vector(1,0)*self/self.norm())
        arg_in_deg = math.degrees(arg_in_rad)
        if self.values[0] > 0:
            return 360 - arg_in_deg
        else:
            return arg_in_deg

    def normalize(self):
        #vektor normalisieren
        norm = self.norm()
        if norm != 0:
            normed = tuple(comp / norm for comp in self)
            return Vector(*normed)
        return self

    def rotate(self, *args):
        #wenn zahl übergeben, 2D vektor rotieren
        if len(args) == 1 and type(args[0]) in (int, float):
            if len(self) != 2:
                raise ValueError("Rotation axis not defined for greater than 2D vector")
            return self._rotate2D(*args)
        #sonst wird rotationsmatrix erwartet
        elif len(args) == 1:
            matrix = args[0]
            if not all(len(row) == len(matrix) for row in matrix) or not len(matrix) == len(self):
                raise ValueError("Rotation matrix must be square and same dimensions as vector")
            return self.matrix_mult(matrix)

    def _rotate2D(self, theta):
        #2D vektor um theta grad rotieren
        theta = math.radians(theta)
        dc, ds = math.cos(theta), math.sin(theta)
        x, y = self.values
        x, y = dc * x - ds * y, ds * x + dc * y
        return Vector(x, y)

    def matrix_mult(self, matrix):
        #vektor * matrix
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError("Matrix must match vector dimensions")

        product = tuple(Vector(*row) * self for row in matrix)
        return Vector(*product)

    def inner(self, other):
        #vektor * vektor
        return sum(a * b for a, b in zip(self, other))

    def __mul__(self, other):
        #vektor * vektor oder vektor * zahl
        if type(other) == type(self):
            return self.inner(other)
        elif type(other) in (int, float):
            product = tuple(a * other for a in self)
            return Vector(*product)

    def __rmul__(self, other):
        #wenn zahl * vektor
        return self.__mul__(other)

    def __truediv__(self, other):
        #vektor / zahl
        if type(other) in (int, float):
            divided = tuple(a / other for a in self)
            return Vector(*divided)
            
    def __floordiv__(self, other):
        #vektor / zahl
        if type(other) in (int, float):
            divided = tuple(a // other for a in self)
            return Vector(*divided)

    def __add__(self, other):
        #vektor + vektor
        added = tuple(a + b for a, b in zip(self, other))
        return Vector(*added)

    def __sub__(self, other):
        #vektor - vektor
        subbed = tuple(a - b for a, b in zip(self, other))
        return Vector(*subbed)

    def __iter__(self):
        #for i in vektor
        return self.values.__iter__()

    def __len__(self):
        #len(vektor)
        return len(self.values)

    def __getitem__(self, key):
        #vektor[i]
        return self.values[key]

    def __repr__(self):
        #print(vektor)
        return str(self.values)
    
    def serialize(self):
        return self.values