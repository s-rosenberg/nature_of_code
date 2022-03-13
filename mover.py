from vector import Vector
from canvas import Canvas
import pygame

# colores
BLACK = (0,0,0)
WHITE = (255,255,255)

class Mover:

    def __init__(self, canvas:Canvas, position:Vector = None, velocity:Vector = None, aceleration: Vector = None, max_velocity=10):
        
        self.surface = canvas.get_surface()
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
    
    def display(self):
        pygame.draw.circle(self.surface, center= (self.position.x, self.position.y), color=BLACK, radius=10)

    def check_bordes(self, flip=True):
        if self.position.x >= self.max_x or self.position.x <= 0:
            self.velocity.flip_horizontal()
            self.aceleration.flip_horizontal()
        if self.position.y >= self.max_y or self.position.y <= 0:
            self.velocity.flip_vertical()
            self.aceleration.flip_vertical()

    def random_aceleration(self, ratio=0.01):
        aceleration = Vector.random_vector(-1,1,-1,1)
        aceleration.normalize()
        aceleration *= ratio
        
        return aceleration

    def control_aceleration(self, events=None):
        self.velocity += self.aceleration

class MoverAcelerable(Mover):
    def __init__(self, canvas: Canvas, position: Vector = None, velocity: Vector = None, aceleration: Vector = None, max_velocity=10):
        super().__init__(canvas, position, velocity, aceleration, max_velocity)
        
    def acelerar(self):
        self.velocity += self.aceleration
    def desacelerar(self):
        self.velocity -= self.aceleration
    
    def control_aceleration(self, events):
        key_event = self.get_key_press_event(events)
        if key_event:
            if key_event.key == pygame.K_UP:
                print('arriba')
                self.acelerar()
            elif key_event.key == pygame.K_DOWN:
                print('abajo')
                self.desacelerar()
        
    def get_key_press_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                return event
            

if __name__ == '__main__':
    SIZE = 800, 600
    canvas = Canvas(SIZE)
    screen = canvas.get_surface()
    # init del Mover
    mover = MoverAcelerable(canvas, velocity=Vector(0,0),max_velocity=10)
    
    
    def loop_function(events):
        
        screen.fill(WHITE)
        mover.display()
        mover.update(events)
        mover.check_bordes()
        pygame.display.flip()
    
    canvas.loop_function = loop_function
    
    canvas.kill_event = pygame.QUIT
    canvas.main()
    del canvas
