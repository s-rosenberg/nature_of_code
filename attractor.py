from vector import Vector
from ser import Ser
from canvas import Canvas
from mover import NewtonMover
import pygame



G = 0.4
WHITE = (255,255,255)
BLACK = (0,0,0)

class Attractor(Ser):
    
    def __init__(self, canvas: Canvas, position: Vector, mass: float, radius: float = None, height: float = None, width: float = None) -> None:
        super().__init__(canvas, position, mass, radius, height, width)

if __name__ == '__main__':
    
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    vel_inicial = Vector(1,0)
    ac_inicial = Vector(0,0)
    
    attractor_mass = 10
    attractor = Attractor(canvas, position=Vector(SIZE[0]/2,SIZE[1]/2),mass=attractor_mass, radius=attractor_mass)
    mover_position = attractor.position + Vector(0,20)
    mover = NewtonMover(canvas=canvas, position = mover_position, mass=5, radius=5,velocity=vel_inicial,aceleration=ac_inicial, max_velocity=0.5)

    def loop_function(events):
        
        screen.fill(WHITE)
        
        attraction = attractor.attract(mover)
        mover.apply_force(attraction)
        mover.update(events)
        mover.display()
        attractor.display()
        # mover.check_bordes(damping=0.75)  
        pygame.display.flip()
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas
