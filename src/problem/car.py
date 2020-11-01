from typing import List, Tuple
import math
import pygame

from src.problem.segment import Segment
from src.problem.lidar import Lidar
from src.problem.world import World
import neural_network as nn


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

    BRAIN_OUTPUT = 2
    MAX_TURNS = 600

    def __init__(self, world, x: float, y: float, rotation: float = 0, hidden_layers=None):
        self.x = world.init_position[0]
        self.y = world.init_position[1]
        self.rotation = world.init_position[2]
        self.velocity = 1
        self.lidar = Lidar(world, [self.x, self.y], self.rotation)
        self.distance = 0
        self.brain = nn.Neural_Network(self.lidar.NUMBER_OF_LASERS)
        if hidden_layers is None:
            hidden_layers = [5]
        for nb_neurons in hidden_layers:
            self.brain.add_layer(nb_neurons)
        self.brain.add_layer(Car.BRAIN_OUTPUT)

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

        self.__update_segments(dx=self.x, dy=self.y, dr=self.rotation)
        self.crashed = False
        self.world = world

        self.first_turn = 0
        self.counter_turn = 0

    def update(self):
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

        predict = self.brain.forward(self.lidar.get_values())
        if predict[0, 0] > 0.5:
            self.turn_left()
        elif predict[0, 1] > 0.5:
            self.turn_right()
        if self.counter_turn == Car.MAX_TURNS:
            # print('exceeded turns')
            self.crashed = True
        # print(self.distance, self.x, self.y)

    def turn_left(self):
        if self.first_turn != -1:
            self.first_turn = -1
            self.counter_turn = 0
        else:
            self.counter_turn += 1
        if not self.crashed:
            self.rotation -= 0.03
            self.__update_segments(dr=-0.03)
    
    def turn_right(self):
        if self.first_turn != 1:
            self.first_turn = 1
            self.counter_turn = 0
        else:
            self.counter_turn += 1

        if not self.crashed:
            self.rotation += 0.03
            self.__update_segments(dr=0.03)

    def run_in_loop(self):
        # print(self.world.name, end='\t')
        while not self.crashed:
            self.update()
            if self.distance > 3000:
                # print(self.distance, end=' ')
                return
        # print(self.distance, end=' ')

    def reset_world(self, world):
        self.world = world
        self.x = world.init_position[0]
        self.y = world.init_position[1]
        self.distance = 0
        self.rotation = world.init_position[2]
        self.lidar = Lidar(world, [self.x, self.y], self.rotation)
        self.__update_segments(dx=self.x, dy=self.y, dr=self.rotation)
        self.crashed = False


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
        self.update()
        for segment in self.segments:
            segment.draw(surface)
        x, y = self.x, int(self.y)

        pygame.draw.circle(surface, (200,0,0), (int(x), y), 5)

        self.lidar.draw(surface)

    def load_brain(self):
        self.brain.load()

    def save_brain(self):
        self.brain.save()
