import pygame

class Canvas:

    def __init__(self, size, pre_function=None, loop_function=None, kill_event=None):
        self.size = size
        self.pre_function = pre_function
        self.loop_function = loop_function
        self.kill_event = kill_event
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        
    def main(self):
        if self.pre_function: self.pre_function.__call__()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == self.kill_event: 
                    print('DEBERIA CERRAR!!')
                    run = False
            if self.loop_function : self.loop_function.__call__()
        # DATAZA para llamar funciones pasadas como variables usar el __call__()
        
    def get_surface(self) -> pygame.Surface:
        return self.screen    
    
    def __del__(self):
        pygame.quit()