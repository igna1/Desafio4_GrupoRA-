import pygame
import json
from src.problem.world import World
from src.problem.car import Car

class Editor:

    __screen: pygame.surface.Surface
    __done: bool

    # Mundo del simulador
    __chain_selected: int
    __world: World
    __car: Car
    __car_selected: bool

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    def __init__(self,filename,edit):
        pygame.init()
        self.__filename = filename
        self.__screen = pygame.display.set_mode((self.SCREEN_HEIGHT,
                                                 self.SCREEN_WIDTH))
        self.__done = False
        pygame.display.set_caption("IA Driver World Editor ({})".format(filename))

        self.__font = pygame.font.SysFont(None, 32)
        self.__r_info= self.__font.render(
                "r: reset", True, (255, 255, 255))
        self.__s_info= self.__font.render(
                "s: save", True, (255, 255, 255))
        self.__z_info= self.__font.render(
                "z: undo lane", True, (255, 255, 255))
        self.__c_info= self.__font.render(
                "c: complete", True, (255, 255, 255))

        if edit:
            self.__world = World(filename)
        else:
            self.__world = World()
        
        self.__car = Car(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2, 0)
        self.__chain_selected = 1
        self.__car_selected = False
        self.__init_position = [self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2]


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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if not self.__car_selected:
                        self.__world.add_vector(self.__chain_selected,[mx,my])
                    else:
                        self.__car = Car(mx, my, self.__car.rotation)
                        self.__init_position = [mx,my]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.__chain_selected = 1
                        self.__car_selected = False
                    elif event.key == pygame.K_2:
                        self.__chain_selected = 2
                        self.__car_selected = False
                    elif event.key == pygame.K_3:
                        self.__car_selected = not self.__car_selected
                    elif event.key == pygame.K_LEFT:
                        new_rotation = self.__car.rotation - 0.25
                        self.__car = Car(self.__car.x, self.__car.y,new_rotation)
                    elif event.key == pygame.K_RIGHT:
                        new_rotation = self.__car.rotation + 0.25
                        self.__car = Car(self.__car.x, self.__car.y,new_rotation)
                    elif event.key == pygame.K_DOWN:
                        new_rotation = self.__car.rotation - 0.05
                        self.__car = Car(self.__car.x, self.__car.y,new_rotation)
                    elif event.key == pygame.K_UP:
                        new_rotation = self.__car.rotation + 0.05
                        self.__car = Car(self.__car.x, self.__car.y,new_rotation)
                    elif event.key == pygame.K_r:
                        self.__world = World()
                    elif event.key == pygame.K_s:
                        data = {}
                        data["world"] = self.__world.vectors
                        data["init_position"] = [self.__car.x,self.__car.y,self.__car.rotation]
                        with open(self.__filename,"w") as output:
                            json.dump(data,output, indent=1)
                            print("file saved as {}".format(self.__filename))
                    elif event.key == pygame.K_z:
                        self.__world.pop_vector(self.__chain_selected)
                    elif event.key == pygame.K_c:
                        if len(self.__world.vectors[0]) > 0 and len(self.__world.vectors[1]) > 0 :
                            self.__world.add_vector(1,self.__world.vectors[0][0])
                            self.__world.add_vector(2,self.__world.vectors[1][0])


            # Actualizando pantalla
            self.__info= self.__font.render(
                "lane:{} , moving_car:{} ".format(self.__chain_selected,self.__car_selected), True, (255, 255, 255))
            self.__draw_and_update()

    def __draw_and_update(self):
        self.__screen.fill((33, 33, 33))
        self.__world.draw(self.__screen)
        self.__car.draw(self.__screen)
        self.__screen.blit(self.__info,(0,0))
        self.__screen.blit(self.__z_info,(450,0))
        self.__screen.blit(self.__c_info,(450,30))
        self.__screen.blit(self.__s_info,(500,60))
        self.__screen.blit(self.__r_info,(500,90))
        


        pygame.display.update()
