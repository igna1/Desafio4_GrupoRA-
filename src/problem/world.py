import json
import pygame
from typing import List
from src.problem.segment import Segment

class World:

    vectors: List[List[List[float]]]
    segments: List[Segment]

    def __init__(self, world_file:str = None):
        # Leyendo mundo
        if world_file:
            with open(world_file, 'r') as fh:
                data = json.load(fh)
            # Cargando vectores
            self.vectors = data["world"]
            self.init_position = data["init_position"]

            # Creando la lista de segmentos
            self.segments = []
            for chain in self.vectors:
                for index, vector in enumerate(chain[:-1]):
                    next_vector = chain[(index+1) % len(chain)]
                    new_segment = Segment(vector, next_vector)
                    self.segments.append(new_segment)
        else:
            self.vectors = [[],[]]
            self.segments = []

    def draw(self, surface: pygame.surface.Surface):
        for segment in self.segments:
            segment.draw(surface)

    def add_vector(self,chain,vector):
        if chain == 1:
            self.vectors[0].append(vector)
        else:
            self.vectors[1].append(vector)

        self.segments = []
        for chain in self.vectors:
                for index, vector in enumerate(chain[:-1]):
                    next_vector = chain[(index+1) % len(chain)]
                    new_segment = Segment(vector, next_vector)
                    self.segments.append(new_segment)

    def pop_vector(self,chain):
        if chain==1:
            if len(self.vectors[0]) > 0:
                self.vectors[0].pop()
        else:
            if len(self.vectors[1]) > 0:
                self.vectors[1].pop()

        self.segments = []
        for chain in self.vectors:
                for index, vector in enumerate(chain[:-1]):
                    next_vector = chain[(index+1) % len(chain)]
                    new_segment = Segment(vector, next_vector)
                    self.segments.append(new_segment)
