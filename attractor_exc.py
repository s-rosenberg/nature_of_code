import pygame
from canvas import Canvas
from mover import NewtonMover
from attractor import Attractor
from vector import Vector
WHITE = (255,255,255)
def exc_2_8():
    """
    build an example with both attractors and movers
    """
    ac_inicial = Vector(0,0)
    vel_inicial = Vector(0,0)
    movers = [NewtonMover(canvas,position=Vector.random_vector(0,SIZE[0],0,SIZE[1]),mass=mass, radius=mass, velocity=vel_inicial, aceleration=ac_inicial) for mass in range(5)]
    attractors = [Attractor(canvas, position=Vector(x,SIZE[1]/2), mass=20, height=20, width=20) for x in range(0, SIZE[0], SIZE[0]//3)]
    return movers, attractors    
    # pass
def exc_2_8_bis():
    """
    build an example with both attractors and movers
    what if los attractors son invisibles 
    """
    # comentar o descomentar attractor display
    pass

if __name__ == '__main__':
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    movers, attractors = exc_2_8()
    
    def loop_function(events):
        
        screen.fill(WHITE)
        
        for mover in movers:
            for attractor in attractors:
                # attractor.display()
                attraction = attractor.attract(mover)
                mover.apply_force(attraction)    
            mover.display()
            
            mover.update(events)
            mover.check_bordes(damping=0.75)  
        pygame.display.flip()
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas