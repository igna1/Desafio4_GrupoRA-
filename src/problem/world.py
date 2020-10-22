import json
import pygame
from typing import List
from src.problem.segment import Segment

class World:

    vectors: List[List[List[float]]]
    segments: List[Segment]

    def __init__(self, world_file: str):
        # Leyendo mundo
        with open(world_file, 'r') as fh:
            data = json.load(fh)
        
        # Cargando vectores
        self.vectors = data["world"]

        # Creando la lista de segmentos
        self.segments = []
        for chain in self.vectors:
            for index, vector in enumerate(chain[:-1]):
                next_vector = chain[(index+1) % len(chain)]
                new_segment = Segment(vector, next_vector)
                self.segments.append(new_segment)

    def draw(self, surface: pygame.surface.Surface):
        for segment in self.segments:
            segment.draw(surface)