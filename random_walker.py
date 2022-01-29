from cmath import pi
import random
import pygame

# colores
BLACK = (0,0,0)
WHITE = (255,255,255)

class PequeñoSer:

    def __init__(self, x:int, y:int, canvas: pygame.Surface, color=BLACK, pixel=False):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.color = color
        self.pixel = pixel
    
    def display(self):
        if self.pixel:
            pygame.draw.line(self.canvas, self.color, (self.x, self.y), (self.x, self.y))
        else:
            pygame.draw.circle(self.canvas, self.color, (self.x, self.y), 1)
    
    # TODO que deje un recorrido
    # se puede appendear a una lista ? y que displayee eso tambien

class RandomWalker(PequeñoSer):
    
    def __init__(self, x:int, y:int, canvas: pygame.Surface, color=BLACK, pixel=False):
        super().__init__(x, y, canvas, color, pixel)        
    
    def step(self):
        choice = random.randint(0,3)
        if choice == 0:
            self.x += 1
        elif choice == 1:
            self.x -= 1
        elif choice == 2:
            self.y += 1
        else: 
            self.y -= 1