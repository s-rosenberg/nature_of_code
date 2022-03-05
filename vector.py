
import math
from random_walker import Pixel
from canvas import Canvas
import pygame
import random
from copy import copy

BLACK = (0,0,0)
WHITE = (255,255,255)

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __suma(self, other_v):
        self.x += other_v.x
        self.y += other_v.y

    def __add__(self, other_v):
        new_vector = copy(self)
        new_vector.__suma(other_v)

        return new_vector

    def __resta(self, other_v):
        self.x -= other_v.x
        self.y += other_v.y

    def __sub__(self, other_v):
        new_vector = copy(self)
        new_vector.__resta(other_v)

        return new_vector

    def __multiplicacion(self, obj):
        # obj: int or float
        self.x *= obj
        self.y *= obj

    def __mul__(self, obj):
        if type(obj) == Vector:
            return self.vector_mul(self, obj) 
        elif type(obj) in (int, float):
            return self.scalar_mul(self, obj)
    
    def __division(self, obj):
        if obj != 0:
            self.__multiplicacion(obj ** -1)
        
    def __truediv__(self, obj):
        if type(obj) in (int, float):
            new_vector = copy(self)
            new_vector.__division(obj)

            return new_vector

    def mag(self):
        # magnitud del vector
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalized(self):
        new_vector = copy(self)
        new_vector.normalize()

        return new_vector

    def normalize(self):
        # convierte a vector unitario
        mag = self.mag()
        self.__division(mag)

    @staticmethod
    def vector_mul(vector_1, vector2):
        raise NotImplementedError
    
    @staticmethod
    def scalar_mul(vector, scalar):
        new_vector = copy(vector)
        new_vector.__multiplicacion(scalar)

        return new_vector

class RandomVectorWalker(Pixel):
    
    def __init__(self, posicion:Vector, canvas:pygame.Surface, color=BLACK, pixel=False):
        x = posicion.x
        y = posicion.y
        super().__init__(x,y,canvas,color,pixel)
        self.recorrido = [posicion]
        self.posicion = posicion

    def get_step(self, step_x=None, step_y=None):
        step_x = step_x if step_x else random.randint(-1, 1)
        step_y = step_y if step_y else random.randint(-1, 1)
        return Vector(step_x, step_y)
    
    def step(self, step_x=None, step_y=None):
        step = self.get_step(step_x, step_y)
        self.posicion += step
        
        self.recorrido.append(self.posicion)

    def display(self, leave_trail=True):
        if leave_trail:
            for posicion in self.recorrido:
                super().draw(posicion.x, posicion.y)
        else:
            super().draw(posicion.x, posicion.y)

if __name__ == '__main__':
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    # init del random w
    pos = Vector(SIZE[0]/2, SIZE[1]/2)
    walker = RandomVectorWalker(pos, screen,pixel=True)
    
    def loop_function():
        screen.fill(WHITE)
        walker.display()
        walker.step()

        pygame.display.flip()
    
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas

