from random import gauss
import time
import pygame
from random_walker import RandomWalker, DownRightRandomWalker, RandomFollower

pygame.init()
SIZE = 800,600
screen = pygame.display.set_mode(SIZE)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255, 0)

walker = RandomWalker(SIZE[0]/2,SIZE[1]/2,screen,pixel=True)
gauss_walker = RandomWalker(SIZE[0]/2,SIZE[1]/2,screen, color=RED,pixel=True)
# dr_walker = DownRightRandomWalker(SIZE[0]/2,SIZE[1]/2,screen,color=RED,pixel=True)
# follower = RandomFollower(SIZE[0]/2,SIZE[1]/2,screen,color=GREEN,pixel=True)

run = True
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
    # dibujo al gauss_walker
    gauss_walker.display()
    gauss_walker.gaussian_step()
    # # dibujo al dr_walker
    # dr_walker.display()
    # dr_walker.book_step()
    # # time.sleep(0.1)
    # follower.display()
    # follower.step()
    pygame.display.flip()
pygame.quit()