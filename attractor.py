from vector import Vector
from ser import Ser
from canvas import Canvas

class Attractor(Ser):
    
    def __init__(self, canvas: Canvas, position: Vector, mass: float, radius: float = None, height: float = None, width: float = None) -> None:
        super().__init__(canvas, position, mass, radius, height, width)