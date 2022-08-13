from mover import NewtonMover
from liquid import Liquid
import pygame
from canvas import Canvas
from vector import Vector

BLACK = (0,0,0)
WHITE = (255,255,255)

def exc_2_5():
    """
    Ex 2.5
    Take a look at our formula for drag again: drag force = coefficient * speed * speed. The faster an object moves, 
    the greater the drag force against it. In fact, an object not moving in water experiences no drag at all. 
    Expand the example to drop the balls from different heights. How does this affect the drag as they hit the water?
    """
    mass = 1
    movers = [
        NewtonMover(
            canvas, 
            velocity=vel_inicial, 
            aceleration=ac_inicial, 
            position=Vector((SIZE[0] / 20)*pos , pos*5),
            forces=[gravity*mass/10],
            mass=mass)
            for pos in range(1, 20, 1)]
    return movers

class RectMover(NewtonMover):
    def __init__(self, canvas: Canvas, position: Vector, mass: float, radius: float = None, height: float = None, width: float = None, velocity: Vector = None, aceleration: Vector = None, max_velocity: int = 10, forces: list[Vector] = ...) -> None:
        super().__init__(canvas, position, mass, radius, height, width, velocity, aceleration, max_velocity, forces)
    # def __init__(self, canvas: Canvas, mass: float = 1, position: Vector = None, velocity: Vector = None, aceleration: Vector = None, max_velocity: int = 10, forces: list[Vector] = [], width:int = 1, height:int = 1):
    #     super().__init__(canvas, mass, position, velocity, aceleration, max_velocity, forces)
    #     self.width = width
    #     self.height = height
    
    # def display(self):
    #     pygame.draw.rect(self.surface, BLACK, self.get_pygame_rect())
    
    # def get_pygame_rect(self) -> pygame.Rect:
    #     return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def drag(self, liquid: Liquid):
        speed = self.velocity.mag()
        drag_magnitude = liquid.coefficient_of_drag * self.width / 5 * speed ** 2 
        drag = -self.velocity
        drag.normalize()
        drag.multiplicacion(drag_magnitude)
        self.apply_force(drag)

def exc_2_6():
    """
    The formula for drag also included surface area. Can you create a simulation of boxes 
    falling into water with a drag force dependent on the length of the side hitting the water?

    Crear una clase que herede de newton mover que sea un cuadrado (o rectangulo)
    y agregar la surface area en el metodo correspondiente
    """
    mass = 1
    movers = [
        NewtonMover(
            canvas, 
            velocity=vel_inicial, 
            aceleration=ac_inicial, 
            position=Vector((SIZE[0] / 5)*pos , 0),
            forces=[gravity*mass/10],
            mass=mass,
            width=pos * 10,
            height = pos * 10)
            for pos in range(1, 5, 1)]
    return movers

if __name__ == '__main__':
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    vel_inicial = Vector(0,0)
    ac_inicial = Vector(0,0)
    gravity = Vector(0,0.001)
    liquid = Liquid(location=Vector(0,canvas.get_y_size()/2), height=canvas.get_y_size()/2, width=canvas.get_x_size(), coefficient_of_drag=0.01)
    movers = exc_2_6()
    
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