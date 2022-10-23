from typing_extensions import Self
from vector import Vector
from canvas import Canvas
from pygame import Rect, draw
# from constants import colors # TODO investigar como manejar constantes

BLACK = (0,0,0)
G = 0.4
def constrain(value:float, low:float, high:float):
    if value > high: return high
    elif value < low: return low
    else: return value

class Ser:
    
    def __init__(self, canvas:Canvas, position:Vector, mass:float, radius:float=None, height:float=None, width:float=None) -> None:
        self.surface = canvas.get_surface()
        self.position = position
        self.mass = mass
        self.width = width
        self.height = height
        self.radius = radius
        self.circle = self.is_circle()

    def is_circle(self):
        if self.radius != None and self.height == None and self.width == None:
            return True
        elif self.radius == None and self.height != None and self.width != None:
            return False
        else:
            raise Exception("radius or sides! choose wisely")
    
    def display(self):
        if self.circle:
            draw.circle(surface=self.surface, color=BLACK, center=(self.position.x, self.position.y), radius = self.radius)
        else: 
            draw.rect(surface=self.surface, color=BLACK, rect=self.get_pygame_rect())

    def get_pygame_rect(self) -> Rect:
        return Rect(self.position.x, self.position.y, self.width, self.height)

    def attract(self, other_ser:Self) -> Vector:

        distance, direction = self.get_distance_and_direction(other_ser)
        strength = (G * self.mass * other_ser.mass) / (distance * distance)
        force = direction * strength

        return force

    def get_distance_and_direction(self, other_ser:Self) -> tuple[float,Vector]:
        direction = self.position - other_ser.position
        distance = direction.mag()
        distance = constrain(distance, 5, 25)
        direction.normalize()

        return distance, direction