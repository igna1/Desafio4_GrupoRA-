import pygame
import math
from typing import List
from src.problem.world import World
from src.problem.segment import Segment

class Lidar:

    # Posicionamiento y el mundo
    __world: World                  # Mundo donde se encuentra el lidar
    __position: List[float]         # Posicion del lidar
    __rotation: float               # Rotación del lidar en radianes
    
    # Constantes
    LASER_LENGHT = 200              # Largo de cada laser
    LIDAR_AMPLITUDE = math.pi/2       # Angulo de cobertura del lidar en radianes
    NUMBER_OF_LASERS = 5

    def __init__(self, world: World, position: List[float], rotation: float):
        self.__world = world
        self.__position = position
        self.__rotation = rotation

        self.color = (200, 100, 100)

    def set_position(self, position: List[float], rotation: float):
        self.__position = position
        self.__rotation = rotation

    def get_values(self) -> List[float]:
        angle = self.__rotation - self.LIDAR_AMPLITUDE/2
        values = []

        for _ in range(self.NUMBER_OF_LASERS):
            start_pos = self.__position
            end_pos = (self.LASER_LENGHT * math.cos(angle) + self.__position[0],
                       self.LASER_LENGHT * math.sin(angle) + self.__position[1])
            segment = Segment(start_pos, end_pos)
            value = 1
            for world_segment in self.__world.segments:
                intersection = segment.get_intersection(world_segment)
                if not intersection is None: # Si hubo un interseccion
                    new_value = math.sqrt((intersection[0] - start_pos[0])**2 + (intersection[1] - start_pos[1])**2) \
                            / segment.lenght
                    value = min(value, new_value)
                    
            values.append(value)

            angle += self.LIDAR_AMPLITUDE/(self.NUMBER_OF_LASERS - 1)
        return values

    def draw(self, surface: pygame.surface.Surface):
        angle = self.__rotation - self.LIDAR_AMPLITUDE/2

        for value in self.get_values():
            lenght = self.LASER_LENGHT * value
            end_pos = (lenght * math.cos(angle) + self.__position[0],
                       lenght * math.sin(angle) + self.__position[1])
            color = (255 - 255 * value, 200 * value, 50 * value)
            pygame.draw.line(surface, color, self.__position, end_pos)
            angle += self.LIDAR_AMPLITUDE/(self.NUMBER_OF_LASERS - 1)