from re import L
from vector import Vector
from canvas import Canvas
# from mover import NewtonMover

class Liquid:
    def __init__(self, location:Vector, height:float, width:float, coefficient_of_drag:float) -> None:
        self.location = location
        self.height = height
        self.width = width
        self.coefficient_of_drag = coefficient_of_drag

