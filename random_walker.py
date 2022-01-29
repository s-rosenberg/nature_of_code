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
        
    def draw(self, x, y):
        if self.pixel:
            pygame.draw.line(self.canvas, self.color, (x, y), (x, y))
        else:
            pygame.draw.circle(self.canvas, self.color, (x, y), 1)

class RandomWalker(PequeñoSer):
    
    def __init__(self, x:int, y:int, canvas: pygame.Surface, color=BLACK, pixel=False):
        super().__init__(x, y, canvas, color, pixel)        
        self.recorrido = [(self.x,self.y)]
        
    def step(self):
        step_x = random.randint(-1, 1)
        step_y = random.randint(-1, 1)
        self.x += step_x
        self.y += step_y
        self.recorrido.append((self.x,self.y))

    def display(self, leave_trail=True):
        if leave_trail:
            for punto in self.recorrido:
                super().draw(punto[0],punto[1])
        else:
            super().draw(self.x, self.y)

class DownRightRandomWalker(RandomWalker):
    # Ex I.1 Create a random walker that has a tendency to move down and to the right
    def __init__(self, x:int, y:int, canvas: pygame.Surface, color=BLACK, pixel=False):
        super().__init__(x, y, canvas, color, pixel)
    
    def step(self, weight=0.1):
        step_x = random.randint(-1, 1) + random.uniform(0, weight)
        step_y = random.randint(-1, 1) + random.uniform(0, weight)
        self.x += step_x
        self.y += step_y
        self.recorrido.append((self.x,self.y))

    # metodo planteado por el libro
    def book_step(self):
        rand_num = random.uniform(0,1)
        if rand_num <0.3:
            self.x += 1
        elif rand_num < 0.6:
            self.y += 1
        elif rand_num < 0.8:
            self.x -= 1
        else:
            self.y -= 1
        self.recorrido.append((self.x, self.y))

class RandomFollower(RandomWalker):
    # Ex I.3 50% probability of following mouse direction
    def __init__(self, x:int, y:int, canvas: pygame.Surface, color=BLACK, pixel=False):
        super().__init__(x, y, canvas, color, pixel)
    
    def step(self):
        rand_num = random.uniform(0,1)
        if rand_num < 0.5:
            self.follow_mouse()
        else:
            super().step()

    def follow_mouse(self):
        mouse_x, mouse_y = self.get_mouse_position()

        if mouse_x > self.x:
            self.x += 1
        else:
            self.x -= 1

        if mouse_y > self.y:
            self.y += 1
        else:
            self.y -= 1
        self.recorrido.append((self.x, self.y))
                
    def get_mouse_position(self):
        return pygame.mouse.get_pos()