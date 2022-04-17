
import math
from random_walker import Pixel
from canvas import Canvas
import pygame
import random
from perlin_noise import PerlinNoise
from copy import copy

BLACK = (0,0,0)
WHITE = (255,255,255)

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.x},{self.y})'

    def __str__(self):
        return f'({self.x},{self.y})'

    def suma(self, other_v):
        self.x += other_v.x
        self.y += other_v.y

    def __add__(self, other_v):
        new_vector = copy(self)
        new_vector.suma(other_v)

        return new_vector

    def neg(self):
        self.multiplicacion(-1)

    def __neg__(self):
        new_vector = copy(self)
        new_vector.neg()

        return new_vector

    def resta(self, other_v):
        self.suma(-other_v)

    def __sub__(self, other_v):
        new_vector = copy(self)
        new_vector.resta(other_v)

        return new_vector

    def multiplicacion(self, obj):
        # obj: int or float
        self.x *= obj
        self.y *= obj

    def __mul__(self, obj):
        if type(obj) == Vector:
            return self.vector_mul(self, obj) 
        elif type(obj) in (int, float):
            return self.scalar_mul(self, obj)
    
    def division(self, obj):
        if obj != 0:
            self.multiplicacion(obj ** -1)
        
    def __truediv__(self, obj):
        if type(obj) in (int, float):
            new_vector = copy(self)
            new_vector.division(obj)

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
        self.division(mag)

    def limit(self, max):
        if self.mag() > max:
            self.normalize()
            self.multiplicacion(max)

    def flip_horizontal(self):
        self.x *= -1
    
    def flip_vertical(self):
        self.y *= -1

    @staticmethod
    def vector_mul(vector_1, vector2):
        raise NotImplementedError
    
    @staticmethod
    def scalar_mul(vector, scalar):
        new_vector = copy(vector)
        new_vector.multiplicacion(scalar)

        return new_vector

    @staticmethod
    def get_distance(vector_1, vector_2):
        return math.sqrt(
            (vector_1.x - vector_2.x)**2 +
            (vector_1.y - vector_2.y)**2
        )
        
    @classmethod
    def random_vector(cls, min_x=None, max_x=None, min_y=None, max_y=None):
        
        normalize = False

        if not min_x and not min_y and not max_x and not max_y:
            min_x = min_y = -1
            max_x = max_y = 1
            normalize = True
        
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)

        return cls(x,y).normalized() if normalize else cls(x,y)

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

class PerlinVector(Vector):
    def __init__(self, x, y, delta_noise = 0.05):
        super().__init__(x, y)
        self.noise = PerlinNoise()
        self.idx_x = 0
        self.idx_y = 10000
        self.delta_noise = delta_noise
    
    def get_new_direction(self):
        self.idx_x += self.delta_noise
        self.idx_y += self.delta_noise
        noise_x = self.noise(self.idx_x)
        noise_y = self.noise(self.idx_y)
        
        self.x = noise_x
        self.y = noise_y
        self.normalize()
        self.multiplicacion(0.0005)

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

