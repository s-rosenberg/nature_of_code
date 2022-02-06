import random
from perlin_noise import PerlinNoise
import pygame

# colores
BLACK = (0,0,0)
WHITE = (255,255,255)

class PequeñoSer:

    def __init__(self, x:int, y:int, canvas: pygame.Surface, color=BLACK, pixel=False, radio:float = 1):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.color = color
        self.pixel = pixel
        self.radio = radio

    def draw(self, x, y):
        if self.pixel:
            pygame.draw.line(self.canvas, self.color, (x, y), (x, y))
        else:
            pygame.draw.circle(self.canvas, self.color, (x, y), self.radio)

class RandomWalker(PequeñoSer):
    
    def __init__(self, x:int, y:int, canvas: pygame.Surface, color=BLACK, pixel=False):
        super().__init__(x, y, canvas, color, pixel)        
        self.recorrido = [(self.x,self.y)]
        
        # perlin 
        self.tx = 0
        self.ty = 10000 

    def step(self, step_x=None, step_y=None):
        step_x = step_x if step_x else random.randint(-1, 1)
        step_y = step_y if step_y else random.randint(-1, 1)
        self.x += step_x
        self.y += step_y
        self.recorrido.append((self.x,self.y))

    def display(self, leave_trail=True):
        if leave_trail:
            for punto in self.recorrido:
                super().draw(punto[0],punto[1])
        else:
            super().draw(self.x, self.y)
    
    def gaussian_step(self):
        mu = 0
        sigma = 1
        step_x = random.gauss(mu,sigma)
        step_y = random.gauss(mu,sigma)

        self.step(step_x, step_y)
    
    def custom_step(self):
        # Exercise I.6
        # Use a custom probability distribution to vary the size of a step 
        # taken by the random walker. The step size can be determined by influencing
        # the range of values picked. Can you map the probability exponentially
        # —i.e. making the likelihood that a value is picked equal to the value squared?
        
        step_size = self.custom_probability()
        step_x = random.uniform(-step_size, step_size)
        step_y = random.uniform(-step_size, step_size)
        self.step(step_x, step_y)

    def custom_probability(self):
        return self.exponential_probability()

    def perlin_step(self):
        noise = PerlinNoise()
        step_x = self.map_range(noise(self.tx), 0, 1, 0,self.canvas.get_width()//20)
        step_y = self.map_range(noise(self.ty), 0, 1, 0,self.canvas.get_height()//20)
        self.tx += 0.01
        self.ty += 0.01
        self.step(step_x,step_y)
        
    def exponential_probability(self):
        while True:
            random_number = random.uniform(0,10)
            probability = random_number ** 2
            random_number2 = random.uniform(0,1)
            if random_number2 < probability / 100:
                return random_number

    @staticmethod
    def map_range(value, start1, stop1, start2, stop2):
        # fuente https://stackoverflow.com/questions/57739846/is-there-a-processing-map-equivalent-for-pytho
        return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

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