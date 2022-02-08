"""
usar perlin en 2d para hacer cosas copadas
"""
from random import Random
from perlin_noise import PerlinNoise
import perlin_noise
import pygame
from random_walker import PequeñoSer, RandomWalker

WHITE = (255,255,255)
BLACK = (0,0,0)

class PerlinSurface():
    
    def __init__(self, canvas:pygame.Surface, delta_noise:float=0.01):
        self.canvas = canvas
        self.width = canvas.get_width()
        self.height = canvas.get_height()
        self.delta_noise = delta_noise
        self.noise = PerlinNoise()

    def populate_surface(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                noise = self.noise([x*self.delta_noise, y*self.delta_noise])
                
                bright = int(RandomWalker.map_range(noise,-1,1,0,255))
                # print(noise, bright)
                color = (bright, bright, bright)
                pequeño_ser = PequeñoSer(x,y,self.canvas,color,True)
                # TODO crear matriz o algo y displayear todo
    
if __name__ == '__main__':
    # TODO una clase de canvas
    pygame.init()
    SIZE = 800, 600
    screen = pygame.display.set_mode(SIZE)
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        perlin_surface = PerlinSurface(screen)
        perlin_surface.populate_surface()
        pygame.display.flip()
    pygame.quit()