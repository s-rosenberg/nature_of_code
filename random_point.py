# Ex I.4 Consider a simulation of paint splatter drawn as a collection of colored dots.
# Most of the paint clusters around a central location, 
# but some dots do splatter out towards the edges. 
# Can you use a normal distribution of random numbers to generate the locations of the dots?
# Can you also use a normal distribution of random numbers to generate a color palette?

import random
import pygame
from random_walker import Pixel

class RandomPoint(Pixel):
    """
    TODO: que el color caiga acorde a la posicion
    """    
    def __init__(self, mu:float, sigma:float, 
        canvas:pygame.Surface, radio:float, 
        pixel:bool = False):
        
        self.x = random.gauss(mu, sigma)
        self.y = random.gauss(mu, sigma)
        
        self.canvas = canvas
        self.pixel = pixel
        self.radio = radio
        self.color = self.get_random_color()

    def get_random_color(self):
        red = self.get_color_num()
        green = self.get_color_num()
        blue = self.get_color_num()

        return (red, green, blue)
    
    def get_color_num(self):
        mu = 255 / 2
        sigma = (255 - 255 / 2) / 5
        
        color_num = int(random.gauss(mu, sigma))
        # esto es tipo un binary overflow?
        if color_num > 255:
            color_num -= 255
        elif color_num < 0:
            color_num += 255
        
        return color_num
if __name__ == '__main__':
    pygame.init()
    SIZE = 600, 600
    screen = pygame.display.set_mode(SIZE)
    WHITE = (255,255,255)
    BLACK = (0,0,0)

    mu = SIZE[0] / 2
    sigma = (SIZE[0] - mu) / 3
    random_points = []
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        
        screen.fill(BLACK)

        random_point = RandomPoint(mu, sigma, screen,radio=2)
        random_points.append(random_point)
        for point in random_points:
            point.draw(point.x, point.y)
        pygame.display.flip()
    pygame.quit()