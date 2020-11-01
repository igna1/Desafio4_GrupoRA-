from typing import List, Tuple
import math
import pygame

from src.problem.segment import Segment
from src.problem.lidar import Lidar
from src.problem.world import World


class Car:

    # Posiciones del centro del carro
    x: float
    y: float

    # Rotación de carro
    rotation: float     # En radianes

    # Velocidad del carro
    velocity: float

    # Estado del carro
    crashed: bool

    # Cuerpo del carro
    segments: List[Segment]
    color = (200, 100, 100)

    # Lidar del carro
    lidar: Lidar

    # Mundo en donde se encuentra el carro
    world: World

    # Dimensiones del carro
    WIDTH = 20
    HEIGHT = 10

    def __init__(self, world, x: float, y: float, rotation: float = 0):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.velocity = 1
        self.lidar = Lidar(world, [self.x, self.y], self.rotation)
        self.distance = 0

        # Creando cuarpo del carro
        p1 = (-self.WIDTH/2, -self.HEIGHT/2)
        p2 = (self.WIDTH/2, -self.HEIGHT/2)
        p3 = (self.WIDTH/2, self.HEIGHT/2)
        p4 = (-self.WIDTH/2, self.HEIGHT/2)
        self.segments = [
            Segment(p1, p2),
            Segment(p2, p3),
            Segment(p3, p4),
            Segment(p4, p1)
        ]

        self.__update_segments(dx=x, dy=y, dr=rotation)
        self.crashed = False
        self.world = world

    def __update(self):
        # Si el auto está colisionado no se actualiza
        if self.crashed:
            return

        # Actualizando posición en base a la velocidad y a la rotación
        dx = self.velocity * math.cos(self.rotation)
        dy = self.velocity * math.sin(self.rotation)
        
        self.x += dx
        self.y += dy

        self.__update_segments(dx=dx, dy=dy)
        self.lidar.set_position([self.x, self.y], self.rotation)

        self.distance += self.velocity
        # Comprobando colision del carro
        for segment in self.segments:
            if self.crashed:
                break
            for world_segment in self.world.segments:
                if world_segment.intersect(segment):
                    self.crashed = True
                    break

            if self.crashed:
                break

    def turn_left(self):
        if not self.crashed:
            self.rotation -= 0.1
            self.__update_segments(dr=-0.1)
    
    def turn_right(self):
        if not self.crashed:
            self.rotation += 0.1
            self.__update_segments(dr=0.1)

    def __update_segments(self, dx: float = 0, dy: float = 0, dr: float = 0):
        for segment in self.segments:
            p1 = list(segment.p1)
            
            # Desplazando al punto
            p1[0] = p1[0] + dx
            p1[1] = p1[1] + dy
            
            # Rotando al punto
            p1[0] = p1[0] - self.x
            p1[1] = p1[1] - self.y
            rotation = math.atan2(p1[1], p1[0])
            rotation += dr
            dist = (p1[0]**2 + p1[1]**2)**(1/2)
            p1[0] = dist * math.cos(rotation) + self.x
            p1[1] = dist * math.sin(rotation) + self.y

            p2 = list(segment.p2)
            
            # Desplazando al punto
            p2[0] = p2[0] + dx
            p2[1] = p2[1] + dy
            
            # Rotando al punto
            p2[0] = p2[0] - self.x
            p2[1] = p2[1] - self.y
            rotation = math.atan2(p2[1], p2[0])
            rotation += dr
            dist = (p2[0]**2 + p2[1]**2)**(1/2)
            p2[0] = dist * math.cos(rotation) + self.x
            p2[1] = dist * math.sin(rotation) + self.y

            segment.p1 = p1
            segment.p2 = p2

    def draw(self, surface: pygame.surface.Surface):
        self.__update()
        for segment in self.segments:
            segment.draw(surface)
        x, y = self.x, int(self.y)

        pygame.draw.circle(surface, (200,0,0), (int(x), y), 5)

        self.lidar.draw(surface)
