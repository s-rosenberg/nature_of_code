from vector import Vector, PerlinVector
from canvas import Canvas
import pygame
import random
from perlin_noise import PerlinNoise
from copy import copy
# colores
BLACK = (0,0,0)
WHITE = (255,255,255)

class Mover:

    def __init__(self, canvas:Canvas, position:Vector = None, velocity:Vector = None, aceleration: Vector = None, max_velocity=10):
        
        self.surface = canvas.get_surface()
        self.max_x = canvas.size[0]
        self.max_y = canvas.size[1]
        self.position = position if position else Vector.random_vector(0,self.max_x, 0, self.max_y)
        self.velocity = velocity if velocity else Vector.random_vector(-2,2,-2,2)
        self.aceleration = aceleration if aceleration else self.random_aceleration()
        self.max_velocity = max_velocity

    def update(self, events):
        self.control_aceleration(events)
        self.velocity.limit(self.max_velocity)
        self.position += self.velocity
    
    def display(self, radius=1):
        pygame.draw.circle(self.surface, center= (self.position.x, self.position.y), color=BLACK, radius=10*radius)

    def check_bordes(self, flip=True):
        if self.position.x >= self.max_x or self.position.x <= 0:
            self.velocity.flip_horizontal()
            self.aceleration.flip_horizontal()
            
            return True
        if self.position.y >= self.max_y or self.position.y <= 0:
            self.velocity.flip_vertical()
            self.aceleration.flip_vertical()
            return True
            
    def random_aceleration(self, ratio=0.01):
        aceleration = Vector.random_vector()
        aceleration *= ratio
        
        return aceleration

    def control_aceleration(self, events=None):
        self.velocity += self.aceleration

class MoverAcelerable(Mover):
    def __init__(self, canvas: Canvas, position: Vector = None, velocity: Vector = None, aceleration: Vector = None, max_velocity=10):
        super().__init__(canvas, position, velocity, aceleration, max_velocity)
        
    def acelerar(self):
        self.velocity += self.aceleration
    def desacelerar(self):
        self.velocity -= self.aceleration
    
    def control_aceleration(self, events):
        key_event = self.get_key_press_event(events)
        if key_event:
            if key_event.key == pygame.K_UP:
                self.acelerar()
            elif key_event.key == pygame.K_DOWN:
                self.desacelerar()
        
    def get_key_press_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                return event

class MoverRandom(Mover):
    def __init__(self, canvas: Canvas, position: Vector = None, velocity: Vector = None, aceleration: Vector = None, max_velocity=10, aceleration_max=2):
        super().__init__(canvas, position, velocity, aceleration, max_velocity)
        self.aceleration = aceleration if aceleration else Vector.random_vector() 
        self.aceleration_max = aceleration_max
    
    def change_aceleration(self):
        self.aceleration = Vector.random_vector()
        self.aceleration *= random.uniform(0, self.aceleration_max)
        
    def control_aceleration(self, events=None):
        self.change_aceleration()
        self.velocity += self.aceleration

class MoverRandomPerlin(MoverRandom):
    def __init__(self, canvas: Canvas, position: Vector = None, velocity: Vector = None, aceleration: Vector = None, max_velocity=10, aceleration_max=2, delta_noise=0.01):
        super().__init__(canvas, position, velocity, aceleration, max_velocity, aceleration_max)
        self.noise = PerlinNoise()
        self.index = 0
        self.delta_noise = delta_noise

    def change_aceleration(self):
        self.index += self.delta_noise
        noise = self.noise(self.index)
        self.aceleration = Vector.random_vector()
        self.aceleration *= noise
        
class MoverHaciaMouse(Mover):
    def __init__(self, canvas: Canvas, position: Vector = None, velocity: Vector = None, 
        aceleration: Vector = Vector(0,0), max_velocity=10, aceleration_ratio = 0.5, 
        gravitational=False, min_distance=5, max_distance=100):
        super().__init__(canvas, position, velocity, aceleration, max_velocity)
        self.aceleration_ratio = aceleration_ratio
        self.gravitational = gravitational
        self.min_distance = min_distance
        self.max_distance = max_distance

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def control_aceleration(self, events=None):
        mouse_x, mouse_y = self.get_mouse_pos()
        mouse_vector = Vector(mouse_x, mouse_y)
        
        aceleration_ratio = self.aceleration_ratio
        self.aceleration = mouse_vector - self.position
        if self.gravitational:
            # Ej 1.8 Try implementing the above example with a variable 
            # magnitude of acceleration, stronger 
            # when it is either closer or farther away.
            distance = self.aceleration.mag() 
            
            if distance < self.min_distance or distance > self.max_distance:
                aceleration_ratio *= 1.05
        self.aceleration.normalize()
        self.aceleration *= aceleration_ratio
        self.velocity += self.aceleration

class NewtonMover(Mover):
    # un mover al que se le pueden aplicar fuerzas
    def __init__(self, canvas: Canvas, mass: float = 1, position: Vector = None, 
    velocity: Vector = None, aceleration: Vector = None, max_velocity=10, forces=[]):
        super().__init__(canvas, position, velocity, aceleration, max_velocity)
        self.forces = forces
        self.mass = mass

    def apply_force(self, force:Vector):
        force /= self.mass
        self.aceleration += force
    
    def control_aceleration(self, events=None):
        for force in self.forces:
            self.apply_force(force)
        super().control_aceleration(events)
        self.aceleration *= 0

    def check_bordes(self, flip=True, damping=0.75):
        bounce = super().check_bordes(flip)
        if bounce: self.velocity *= damping # reducir velocidad por impacto

    def display(self, radius=1):
        radius *= self.mass
        super().display(radius)  

if __name__ == '__main__':
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    # init del Mover
    # mover = MoverHaciaMouse(canvas, velocity=Vector(0,0), 
    #     max_velocity=1, aceleration_ratio=0.01, gravitational=True)
    # mover_2 = MoverRandomPerlin(canvas, velocity=Vector(0,0), max_velocity=1)
    
    # array de movers
    
    # movers = [MoverHaciaMouse(canvas, 
    #                 velocity=Vector(0,0), 
    #                 max_velocity=1, 
    #                 aceleration_ratio=0.005
    #                 ) for idx in range(10)]

    vel_inicial = Vector(0,0)
    ac_inicial = Vector(0,0)
    pos_inicial = Vector(SIZE[0] / 2, 50)
    # pos_inicial_2 = Vector(100,SIZE[1]-50)
    gravity = Vector(0,0.001)
    wind_force = Vector(0.00001,0)
    # mover_1 = NewtonMover(canvas, velocity=vel_inicial, aceleration=ac_inicial, position=pos_inicial,forces=[gravity, wind_force])
    # mover_2 = NewtonMover(canvas, mass= 0.5, velocity=vel_inicial, aceleration=ac_inicial, position=pos_inicial,forces=[gravity, wind_force])
    # movers = [mover_1, mover_2]
    movers = [
        NewtonMover(
            canvas, 
            velocity=vel_inicial, 
            aceleration=ac_inicial, 
            position=pos_inicial,
            forces=[gravity*mass/10, wind_force],
            mass=mass/10)
            for mass in range(1, 20, 1)]

    def loop_function(events):
        
        screen.fill(WHITE)
        for mover in movers:
            friction = copy(mover.velocity)
            friction *= -1       
            friction.normalize()
            friction *= 0.0001
            mover.forces.append(friction)
            mover.display()
            mover.update(events)
            mover.check_bordes(damping=1)
            mover.forces.pop() # sino se me descontrola mas, se seguian agregando fuerzas de friccion :(
            # wind_force.get_new_direction()   
        pygame.display.flip()
    
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas
