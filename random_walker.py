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
        self.recorrido = [(self.x,self.y)]

    def display(self, leave_trail=True):
        if leave_trail:
            for punto in self.recorrido:
                self.draw(punto[0],punto[1])
        else:
            self.draw(self.x, self.y)
    def draw(self, x, y):
        if self.pixel:
            pygame.draw.line(self.canvas, self.color, (x, y), (x, y))
        else:
            pygame.draw.circle(self.canvas, self.color, (x, y), 1)
    
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
        self.recorrido.append((self.x,self.y))