
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
    near = near_to_wall(mover, distance=100)
    nearest_wall = get_nearest_wall(mover)
    distance_to_wall = Vector.get_distance(mover.position, nearest_wall)
    new_force = near / distance_to_wall
    mover.forces = [new_force]

def get_nearest_wall(mover: NewtonMover):

    #################################################
    #                       #                       #
    #   primer cuadrante    #   segundo cuadrante   #
    #                       #                       #
    #################################################
    #                       #                       #
    #   tercer cuadrante    #   cuarto cuadrante    #
    #                       #                       #
    #################################################

    pos_x = mover.position.x
    pos_y = mover.position.y
    max_x = mover.max_x
    max_y = mover.max_y
    izquierda = pos_x <= max_x / 2
    arriba = pos_y <= max_y / 2

    if izquierda:
        if arriba: 
            # primer cuadrante
            if pos_x >= pos_y:
                wall = Vector(pos_x, 0)
            else:
                wall = Vector(0, pos_y)
        else:
            # tercer cuadrante
            if pos_x >= mover.max_y - pos_y:
                wall = Vector(pos_x, max_y)
            else:
                wall = Vector(0, pos_y)
    else:
        if arriba:
            # segundo cuadrante
            if max_x - pos_x >= pos_y:
                wall = Vector(pos_x, 0)
            else:
                wall = Vector(0, pos_y) 
        else:
            # cuarto cuadrante
            if max_x - pos_x >= max_y - pos_y:
                wall =  Vector(pos_x, max_y)
            else:
                wall = Vector(max_x, pos_y)
    return wall

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