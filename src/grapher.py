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
    __turn_left = False
    __turn_right = False

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((self.SCREEN_HEIGHT,
                                                 self.SCREEN_WIDTH))
        self.__done = False
        pygame.display.set_caption("IA Driver")

        self.__world = World("ezworld.json")
        self.__car = Car(self.__world, 162, 301, 1.6)

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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.__turn_left = True
                    elif event.key == pygame.K_d:
                        self.__turn_right = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.__turn_left = False
                    elif event.key == pygame.K_d:
                        self.__turn_right = False

            # Actualizando pantalla
            self.__draw_and_update()

    def __draw_and_update(self):
        self.__screen.fill((33, 33, 33))
        self.__world.draw(self.__screen)
        self.__car.draw(self.__screen)
        pygame.display.update()

        # ! Temporal
        if self.__turn_left:
            self.__car.turn_left()
        if self.__turn_right:
            self.__car.turn_right()
