"""
what happens if you design a force that is weaker the closer it gets and stronger the farther it gets?
Or what if you design your attractor to attract faraway objects, but repel close ones?
TODO: mejorar esto / entender balance de fuerzas

"""


from attractor import Attractor
from canvas import Canvas
from vector import Vector
from mover import NewtonMover
import pygame
import constants

class AttractorInverse(Attractor):
    def __init__(
        self, canvas: Canvas, 
        position: Vector, 
        mass: float, 
        radius: float = None, 
        height: float = None, 
        width: float = None) -> None:

        super().__init__(canvas, position, mass, radius, height, width)

    def attract(self, mover: NewtonMover) -> Vector:
        distance, direction = self.get_distance_and_direction(mover)
        strength = distance / self.mass / mover.mass / constants.G / 100
        force = direction * strength

        return force

    def attract_far_repel_close(self, mover:NewtonMover) -> Vector:
        distance, direction = self.get_distance_and_direction(mover)
        strength = distance / self.mass / mover.mass / constants.G / 100
        if distance < 25: direction *= -100

        force = direction * strength

        return force


if __name__ == '__main__':
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    attractor = AttractorInverse(canvas, Vector(SIZE[0],SIZE[1])/2,100,100)
    mover = NewtonMover(canvas,Vector(SIZE[0],SIZE[1]),10,10,velocity=Vector(0,0),aceleration=Vector(0,0))
    mover_2 = NewtonMover(canvas, Vector(SIZE[0],SIZE[1])/3,10,10, velocity=Vector(0,0),aceleration=Vector(0,0))
    def loop_function(events):
        
        screen.fill(constants.WHITE)
        
        attractor.display()
        attraction = attractor.attract_far_repel_close(mover)
        attraction_2 = attractor.attract(mover_2)
        
        mover.apply_force(attraction)
        mover.display()
        mover.update(events)

        mover_2.apply_force(attraction_2)
        mover_2.display()
        mover_2.update(events)
        
        # for mover in movers:
        #     for attractor in attractors:
        #         # attractor.display()
        #         attraction = attractor.attract(mover)
        #         mover.apply_force(attraction)    
        #     mover.display()
            
        #     mover.update(events)
        #     mover.check_bordes(damping=0.75)  
        pygame.display.flip()
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas