import pygame

class Canvas:

    def __init__(self, size:tuple, pre_function=None, loop_function=None, kill_event=None):
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
            # TODO: fix este problema
            # la lista de eventos se esta recorriendo dos veces 
            # por lo que esta generando mucho lag
            # lo solucione pasandole la lista de eventos como arg a la loop function
            # el problema no esta en que se recorra dos veces
            # sino que se llame dos veces a la lista de eventos
            
            events = pygame.event.get()
            for event in events:
                if event.type == self.kill_event:
                    run = False
            if self.loop_function : self.loop_function.__call__(events)
        # DATAZA para llamar funciones pasadas como variables usar el __call__()
        
    def get_surface(self) -> pygame.Surface:
        return self.screen    
    
    def get_x_size(self):
        return self.size[0]

    def get_y_size(self):
        return self.size[1]
        
    def __del__(self):
        pygame.quit()

        