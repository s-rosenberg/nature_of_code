import pygame

class Canvas:

    def __init__(self, width, height, pre_function=None, loop_function=None, kill_event=None):
        self.width = width
        self.height = height
        self.pre_function = pre_function
        self.loop_function = loop_function
        self.kill_event = kill_event
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        
    def main(self):
        self.pre_function
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == self.kill_event: 
                    print('DEBERIA CERRAR!!')
                    run = False
            self.loop_function
        
    def get_surface(self) -> pygame.Surface:
        return self.screen    
    
    def __del__(self):
        pygame.quit()