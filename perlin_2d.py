"""
usar perlin en 2d para hacer cosas copadas
"""

from perlin_noise import PerlinNoise
import pygame
from random_walker import PequeñoSer, RandomWalker
# import numpy as np
WHITE = (255,255,255)
BLACK = (0,0,0)

class PerlinSurface():
    
    def __init__(self, canvas:pygame.Surface, delta_noise:float=0.01):
        self.canvas = canvas
        self.width = canvas.get_width()
        self.height = canvas.get_height()
        self.delta_noise = delta_noise
        self.noise = PerlinNoise()
        # self.surface = np.zeros((self.width,self.height))
        # print(self.surface)
        self.all_pixels = []

    def populate_surface(self, fast=False):
        for x in range(0, self.width):
            for y in range(0, self.height):
                noise = self.noise([x*self.delta_noise, y*self.delta_noise])
                
                bright = int(RandomWalker.map_range(noise,-1,1,0,255))
                color = (bright, bright, bright)
                pequeño_ser = PequeñoSer(x,y,self.canvas,color,True)
                if fast:
                    # updatear de a cachitos la patanalla (ir barriendo tipo pantalla tele)
                    # definir rect al rededor de pequeño ser
                    # pygame.display.update(rect)
                    pequeño_ser.draw(pequeño_ser.x, pequeño_ser.y)
                    pygame.display.update(x,y,1,1)
                else:
                    # implementacion para show surface / no muy eficiente
                    
                    self.all_pixels.append(pequeño_ser)
                
                
    def show_surface(self):
        # esta implementacion es super lenta, necesita tener todos los pixels para updatear
        for pequeño_ser in self.all_pixels:
            pequeño_ser.draw(pequeño_ser.x, pequeño_ser.y)


if __name__ == '__main__':
    # TODO una clase de canvas
    pygame.init()
    SIZE = 800, 600
    screen = pygame.display.set_mode(SIZE)
    run = True
    perlin_surface = PerlinSurface(screen,0.1)
    perlin_surface.populate_surface(fast=True)
    # perlin_surface.show_surface()
    # pygame.display.flip()
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        
        
        
    pygame.quit()