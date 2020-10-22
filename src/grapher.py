import pygame
import json
from src.problem.world import World
from src.problem.car import Car

class Grapher:

    __screen: pygame.surface.Surface
    __done: bool

    # Mundo del simulador
    __world: World
    __car: Car

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((self.SCREEN_HEIGHT,
                                                 self.SCREEN_WIDTH))
        self.__done = False
        pygame.display.set_caption("IA Driver")

        #deberíamos pasarle la wea desde aqui 
        self.__world = World("world2.json")
        with open("world2.json", 'r') as fh:
                x,y,r = json.load(fh)["init_position"]
        
        self.__car = Car(x, y, r)

    def run(self):
        """
        Bucle del graficador. Es necesario correr esta funcion para que el
        graficador funcione.
        """
        while not self.__done:
            # Actualizando eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__done = True
                    break

            # Actualizando pantalla
            self.__draw_and_update()

    def __draw_and_update(self):
        self.__screen.fill((33, 33, 33))
        self.__world.draw(self.__screen)
        self.__car.draw(self.__screen)
        pygame.display.update()
