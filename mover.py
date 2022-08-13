
from vector import Vector, PerlinVector
from canvas import Canvas
import pygame
import random
from perlin_noise import PerlinNoise
from copy import copy
from liquid import Liquid
from ser import Ser
# colores
BLACK = (0,0,0)
WHITE = (255,255,255)

class Mover(Ser):

    def __init__(self, canvas: Canvas, position: Vector, mass: float, 
                radius: float = None, height: float = None, width: float = None,
                velocity:Vector=None, aceleration:Vector = None, max_velocity:int=10) -> None:
        
        super().__init__(canvas, position, mass, radius, height, width)
        
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
    def __init__(self, canvas: Canvas, position: Vector, mass: float, radius: float = None, height: float = None, width: float = None, velocity: Vector = None, aceleration: Vector = None, max_velocity: int = 10) -> None:
        super().__init__(canvas, position, mass, radius, height, width, velocity, aceleration, max_velocity)
        
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
    def __init__(self, canvas: Canvas, position: Vector, mass: float, radius: float = None, height: float = None, width: float = None, velocity: Vector = None, aceleration: Vector = None, max_velocity: int = 10, aceleration_max = 2) -> None:
        super().__init__(canvas, position, mass, radius, height, width, velocity, aceleration, max_velocity)
        self.aceleration = aceleration if aceleration else Vector.random_vector() 
        self.aceleration_max = aceleration_max
    
    def change_aceleration(self):
        self.aceleration = Vector.random_vector()
        self.aceleration *= random.uniform(0, self.aceleration_max)
        
    def control_aceleration(self, events=None):
        self.change_aceleration()
        self.velocity += self.aceleration

class MoverRandomPerlin(MoverRandom):
    def __init__(self, canvas: Canvas, position: Vector, mass: float, radius: float = None, height: float = None, width: float = None, velocity: Vector = None, aceleration: Vector = None, max_velocity: int = 10, aceleration_max:int=2, delta_noise:float=0.01) -> None:
        super().__init__(canvas, position, mass, radius, height, width, velocity, aceleration, max_velocity, aceleration_max)
        self.noise = PerlinNoise()
        self.index = 0
        self.delta_noise = delta_noise

    def change_aceleration(self):
        self.index += self.delta_noise
        noise = self.noise(self.index)
        self.aceleration = Vector.random_vector()
        self.aceleration *= noise
        
class MoverHaciaMouse(Mover):
    
    def __init__(self, canvas: Canvas, position: Vector = None, mass:float=1, radius: float = None, width: float = None, height:float=None, velocity: Vector = None, 
        aceleration: Vector = Vector(0,0), max_velocity=10, aceleration_ratio = 0.5, 
        gravitational=False, min_distance=5, max_distance=100):

        super().__init__(canvas, position, mass, radius, height, width, velocity, aceleration, max_velocity)  
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
    # def __init__(self, canvas: Canvas, mass: float = 1, position: Vector = None, 
    # velocity: Vector = None, aceleration: Vector = None, max_velocity: int=10, forces: list[Vector] = []):
    def __init__(self, canvas: Canvas, position: Vector, mass: float, radius: float = None, height: float = None, 
        width: float = None, velocity: Vector = None, aceleration: Vector = None, max_velocity: int = 10, forces: list[Vector] = []) -> None:
        super().__init__(canvas, position, mass, radius, height, width, velocity, aceleration, max_velocity)
    
        self.forces = forces
        # self.mass = mass
        # self.radius = mass if not radius else mass*radius

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

    def display(self):
        super().display()  

    def is_inside(self, liquid: Liquid):
        liquid_x1 = liquid.location.x 
        liquid_x2 = liquid.location.x + liquid.width
        liquid_y1 = liquid.location.y 
        liquid_y2 = liquid.location.y + liquid.height

        return self.position.x > liquid_x1 and self.position.y < liquid_x2 \
                and self.position.y > liquid_y1 and self.position.y < liquid_y2
    
    def drag(self, liquid: Liquid):
        speed = self.velocity.mag()
        drag_magnitude = liquid.coefficient_of_drag * speed ** 2
        if self.width:
            drag_magnitude *= self.width / 5
        drag = -self.velocity
        drag.normalize()
        drag.multiplicacion(drag_magnitude)
        self.apply_force(drag)

    
if __name__ == '__main__':
    # SIZE = 800, 600
    # canvas = Canvas(SIZE)
    # screen = canvas.get_surface()
    # # init del Mover
    # # mover = MoverHaciaMouse(canvas, velocity=Vector(0,0), 
    # #     max_velocity=1, aceleration_ratio=0.01, gravitational=True)
    # # mover_2 = MoverRandomPerlin(canvas, velocity=Vector(0,0), max_velocity=1)
    
    # # array de movers
    
    # # movers = [MoverHaciaMouse(canvas, 
    # #                 velocity=Vector(0,0), 
    # #                 max_velocity=1, 
    # #                 aceleration_ratio=0.005
    # #                 ) for idx in range(10)]

    # vel_inicial = Vector(0,0)
    # ac_inicial = Vector(0,0)
    # pos_inicial = Vector(SIZE[0] / 2, 50)
    # # pos_inicial_2 = Vector(100,SIZE[1]-50)
    # gravity = Vector(0,0.001)
    # wind_force = Vector(0.00001,0)
    # # mover_1 = NewtonMover(canvas, velocity=vel_inicial, aceleration=ac_inicial, position=pos_inicial,forces=[gravity, wind_force])
    # # mover_2 = NewtonMover(canvas, mass= 0.5, velocity=vel_inicial, aceleration=ac_inicial, position=pos_inicial,forces=[gravity, wind_force])
    # # movers = [mover_1, mover_2]
    # movers = [
    #     NewtonMover(
    #         canvas, 
    #         velocity=vel_inicial, 
    #         aceleration=ac_inicial, 
    #         position=pos_inicial,
    #         forces=[gravity*mass/10, wind_force],
    #         mass=mass/10)
    #         for mass in range(1, 20, 1)]

    # def loop_function(events):
        
    #     screen.fill(WHITE)
    #     for mover in movers:
    #         friction = copy(mover.velocity)
    #         friction *= -1       
    #         friction.normalize()
    #         friction *= 0.0001
    #         mover.forces.append(friction)
    #         mover.display()
    #         mover.update(events)
    #         mover.check_bordes(damping=1)
    #         mover.forces.pop() # sino se me descontrola mas, se seguian agregando fuerzas de friccion :(
    #         # wind_force.get_new_direction()   
    #     pygame.display.flip()
    
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    vel_inicial = Vector(0,0)
    ac_inicial = Vector(0,0)
    pos_inicial = Vector(SIZE[0] / 2, 50)
    gravity = Vector(0,0.001)
    # wind_force = Vector(0.00001,0)
    
    liquid = Liquid(location=Vector(0,canvas.get_y_size()/2), height=canvas.get_y_size()/2, width=canvas.get_x_size(), coefficient_of_drag=0.01)
    movers = [
        NewtonMover(
            canvas, 
            velocity=vel_inicial, 
            aceleration=ac_inicial, 
            position=Vector((SIZE[0] / 20)*mass ,50),
            forces=[gravity*mass/10],
            radius=mass,
            mass=mass/10)
            for mass in range(1, 20, 1)]
    
    def loop_function(events):
        
        screen.fill(WHITE)
        for mover in movers:
            
            mover.display()
            if mover.is_inside(liquid): 
                mover.drag(liquid)
            mover.update(events)
            mover.check_bordes(damping=0.75)  
        pygame.display.flip()
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas
