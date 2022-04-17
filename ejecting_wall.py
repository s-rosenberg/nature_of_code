from shutil import move
from vector import Vector
from mover import NewtonMover
from canvas import Canvas
import pygame

WHITE = (255,255,255)
"""
Ex 2.3
Instead of objects bouncing off the edge of the wall, 
create an example in which an invisible force pushes back 
on the objects to keep them in the window. 
Can you weight the force according to 
how far the object is from an edge—
i.e., the closer it is, the stronger the force?
"""
def eject(mover:NewtonMover):
    near = near_to_wall(mover)
    # TODO: como esta implementado ahora 
    # funciona muy similar al check bordes
    # modificar para que la fuerza sea inversamente 
    # proporcional a la distancia
    new_force = near * 1.5
    mover.forces = [new_force]
    
def near_to_wall(mover:NewtonMover, distance=10):
    max_x = mover.max_x
    max_y = mover.max_y
    x = 0
    y = 0
    if mover.position.x > max_x - distance:
        x = -1
    elif mover.position.x < distance:
        x = 1
    if mover.position.y > max_y - distance:
        y = -1    
    elif mover.position.y < distance:
        y = 1
    return Vector(x, y) 

def main():
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()

    forces = []
    mover = NewtonMover(canvas, forces=forces, max_velocity=2)
    
    def loop_function(events):
        
        screen.fill(WHITE)
        mover.display()
        eject(mover)
        mover.update(events)
        # mover.check_bordes(damping=1) 
        
        pygame.display.flip()
    
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas

if __name__ == '__main__':
    main()