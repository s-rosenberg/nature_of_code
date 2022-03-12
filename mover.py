from vector import Vector
from canvas import Canvas
import pygame

# colores
BLACK = (0,0,0)
WHITE = (255,255,255)

class Mover:

    def __init__(self, canvas:Canvas, position:Vector = None, velocity:Vector = None, max_velocity=10):
        
        self.surface = canvas.get_surface()
        self.max_x = canvas.size[0]
        self.max_y = canvas.size[1]
        self.position = position if position else Vector.random_vector(0,self.max_x, 0, self.max_y)
        self.velocity = velocity if velocity else Vector.random_vector(-2,2,-2,2)
        self.aceleration = Vector(0.001, 0.001)
        self.max_velocity = max_velocity

    def update(self):
        self.velocity += self.aceleration
        self.velocity.limit(self.max_velocity)
        self.position += self.velocity
    
    def display(self):
        pygame.draw.circle(self.surface, center= (self.position.x, self.position.y), color=BLACK, radius=10)

    def check_bordes(self, flip=True):
        if self.position.x >= self.max_x or self.position.x <= 0:
            self.velocity.flip_horizontal()
            self.aceleration.flip_horizontal()
        if self.position.y >= self.max_y or self.position.y <= 0:
            self.velocity.flip_vertical()
            self.aceleration.flip_vertical()

if __name__ == '__main__':
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    # init del Mover
    mover = Mover(canvas, velocity=Vector(0,0),max_velocity=1)
    
    def loop_function():
        screen.fill(WHITE)
        mover.display()
        mover.update()
        mover.check_bordes()
        pygame.display.flip()
    
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas
