
import pygame
from mover import NewtonMover
from canvas import Canvas
from vector import Vector

"""
Create pockets of friction in a Processing sketch so that objects only experience friction
when crossing over those pockets. What if you vary the strength (friction coefficient)
of each area? What if you make some pockets feature the opposite of friction—i.e., 
when you enter a given pocket you actually speed up instead of slowing down?
"""

# armar un grid dividiendo el canvas en rectangulos de igual tamaño (parametrizable)
class Division:

    def __init__(self, x, y, width, height) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
    
    def is_in_division(self, mover:NewtonMover):
        position = mover.position
        x = position.x
        y = position.y
        
        return self.is_between(x, True) and self.is_between(y, False)

    def is_between(self, coordinate, x=True):
    
        compare1, compare2 = (self.x1, self.x2) if x else (self.y1, self.y2)
        
        return coordinate <= compare2 and coordinate >= compare1

class Grid:             

    def __init__(self, canvas:Canvas, rows:int, columns:int) -> None:
        self.width = canvas.get_x_size()
        self.height = canvas.get_y_size()
        self.rows = rows
        self.columns = columns
        
    def create_grid(self):
        grid = []
        x_division = self.width / self.columns
        y_division = self.height / self.rows

        x_divisions = [x * x_division for x in range(self.columns)]
        y_divisions = [y * y_division for y in range(self.rows)]
        
        for x in x_divisions:
            for y in y_divisions:
                division = Division(x,y,x_division,y_division)
                grid.append(division)

        return grid

if __name__ == '__main__':
    SIZE = 800, 600
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    grid = Grid(canvas, 2, 2)
    divisions = grid.create_grid()
    forces_grid = [Vector.random_vector() for _ in range(len(divisions))]
    mover = NewtonMover(canvas)
    
    def loop_function(events):
        screen.fill(WHITE)
        for n, division in enumerate(divisions):
            if division.is_in_division(mover):
                force = forces_grid[n]
                force.normalize()
                force *= 0.001
                mover.forces.append(force)
        mover.display()
        mover.update(events)
        mover.check_bordes(damping=1)
        if mover.forces:  mover.forces.pop()
        pygame.display.flip()

    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas
