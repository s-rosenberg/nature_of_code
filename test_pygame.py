import time
import pygame
from random_walker import RandomWalker

pygame.init()
SIZE = 800,600
screen = pygame.display.set_mode(SIZE)
WHITE = (255,255,255)
BLACK = (0,0,0)
run = True

walker = RandomWalker(SIZE[0]/2,SIZE[1]/2,screen,pixel=True)

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
    
    screen.fill(WHITE)
    
    # # dibujar un punto (pixel)
    # pygame.draw.line(screen, BLACK, (400,300),(400,300))
    # # dibujar un punto usando circle
    # pygame.draw.circle(screen, BLACK, (350,250),1)
    
    # dibujo al walker
    walker.display()
    walker.step()
    # time.sleep(0.1)
    pygame.display.flip()
pygame.quit()