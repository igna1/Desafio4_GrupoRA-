from typing import List, Tuple
import math
import pygame

from src.problem.segment import Segment

class Car:

    # Posiciones del centro del carro
    x: float
    y: float

    # Rotación de carro
    rotation: float     # En radianes

    # Velocidad del carro
    velocity: float

    # Cuerpo del carro
    segments: List[Segment]
    color = (200, 100, 100)

    # Dimensiones del carro
    WIDTH = 10
    HEIGHT = 20

    def __init__(self, x: float, y: float, rotation: float = 0):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.velocity = 1
        
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

    def __update(self):
        # Actualizando posición en base a la velocidad y a la rotación
        dx = self.velocity * math.cos(self.rotation)
        dy = self.velocity * math.sin(self.rotation)
        
        self.x += dx
        self.y += dy

        self.__update_segments(dx=dx, dy=dy)

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
        for segment in self.segments:
            segment.draw(surface)
        pygame.draw.circle(surface, (200,0,0), (self.x, self.y), 5)