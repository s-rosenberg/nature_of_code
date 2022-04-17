from vector import Vector, PerlinVector
from mover import NewtonMover
from canvas import Canvas
import pygame

# Ex 2.1
# Using forces, simulate a helium-filled balloon floating upward 
# and bouncing off the top of a window. 
# Can you add a wind force that changes over time, 
# perhaps according to Perlin noise?

if __name__ == '__main__':
    # colores
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    
    helium_force = Vector(0, -0.0002)
    gravity = Vector(0, 0.000098)
    wind = PerlinVector(0,0)
    # TODO: modelar viento bien xd
    pos_inicial = Vector(50,SIZE[1]-50)
    vel_inicial = Vector(0,0)
    ac_inicial = Vector(0,0)
    max_velocity = float('inf')
    pelota = NewtonMover(canvas, pos_inicial, vel_inicial, ac_inicial,max_velocity, forces=[gravity, helium_force, wind])    
    def loop_function(events):
        
        screen.fill(WHITE)
        pelota.display()
        pelota.update(events)            
        pelota.check_bordes()
        wind.get_new_direction()
        pygame.display.flip()
    
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas
