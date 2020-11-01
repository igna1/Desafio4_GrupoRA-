from __future__ import annotations
from typing import Tuple
import pygame
import math

class Segment:

    p1: Tuple[float]
    p2: Tuple[float]
    lenght: float
    color = (111, 111, 111)

    def __init__(self, p1: Tuple[float], p2: Tuple[float]):
        self.p1 = p1
        self.p2 = p2
        self.lenght = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def get_min_p(self) -> Tuple[float]:
        # !FIXME: Esto podria generar errores si el segmento es vertical
        # *OPTIMIZE: Esto se podría dejar preprocesar al inicializar
        return self.p1 if self.p1[0] <= self.p2[0] else self.p2

    def get_max_p(self) -> Tuple[float]:
        return self.p1 if self.p1[0] > self.p2[0] else self.p2

    def intersect(self, segment: Segment) -> bool:
        """
        Intersecta este segmento con el ingresado como paremtro

        Args:
            segment (Segment): Segmento con que si quiere intersectar

        Returns:
            bool: Retorna True si los segmentos se intersectan y False en caso
                  contrario.
        """
        # !FIXME: arreglar esto cuando alguno de los segmentos son verticales
        pp1 = self.get_min_p()
        pp2 = self.get_max_p()
        intersection = self.get_intersection(segment)
        if intersection is None:
            return False
        
        px, _ = intersection

        return pp1[0] <= px <= pp2[0]

    def get_intersection(self, segment: Segment) -> Tuple[float]:
        """
        Obtiene el punto de interseccion del segmento con el ingresado como
        parametro

        Args:
            segment (Segment): Segmento que se quiere intersectar con este

        Returns:
            Tuple[float]: Retorna una tupla correspondiente al punto de
                          interseccion. En caso de que no se intersecte se
                          retorna None.
        """
        # Obteniendo puntos
        pp1 = self.get_min_p()
        pp2 = self.get_max_p()
        pp3 = segment.get_min_p()
        pp4 = segment.get_max_p()

        # Caso en que son verticales
        if pp1[0] - pp2[0] == 0 and pp3[0] - pp4[0] == 0:
            return None
        if pp1[1] - pp2[1] == 0 and pp3[1] - pp4[1] == 0:
            return None
        elif pp1[0] - pp2[0] == 0 and pp4[1] - pp3[1] == 0:
            px = pp1[0]
            py = pp4[1]
            if min(pp1[1], pp2[1]) <= py <= max(pp1[1], pp2[1]) and \
                pp3[0] <= px <= pp4[0]:
                return px, py
            return None
        elif pp1[1] - pp2[1] == 0 and pp4[0] - pp3[0] == 0:
            px = pp3[0]
            py = pp1[1]
            if min(pp3[1], pp4[1]) <= py <= max(pp3[1], pp4[1]) and \
                pp1[0] <= px <= pp2[0]:
                return px, py
            return None
        elif pp1[0] - pp2[0] == 0:
            m = (pp4[1] - pp3[1]) / (pp4[0] - pp3[0])
            b = pp3[1] - pp3[0] * m
            px = pp1[0]
            py = m * px + b
            if min(pp1[1], pp2[1]) <= py <= max(pp1[1], pp2[1]) and \
                pp3[0] <= px <= pp4[0]:
                return px, py
            return None
        elif pp3[0] - pp4[0] == 0:
            m = (pp2[1] - pp1[1]) / (pp2[0] - pp1[0])
            b = pp1[1] - pp1[0] * m
            px = pp3[0]
            py = m * px + b
            if min(pp3[1], pp4[1]) <= py <= max(pp3[1], pp4[1]) and \
                pp1[0] <= px <= pp2[0]:
                return px, py
            return None

        # Obteniendo valores de la ecuacion
        ax = pp2[0] - pp1[0]
        bx = pp4[0] - pp3[0]
        cx = pp3[0] - pp1[0]
        ay = pp2[1] - pp1[1]
        by = pp4[1] - pp3[1]
        cy = pp3[1] - pp1[1]

        det = -ax * by + bx * ay

        lambda1 = (cx * (-by) + bx * cy) / det

        # Calculando punto de interseccion
        px = pp1[0] + lambda1 * (pp2[0] - pp1[0])
        py = pp1[1] + lambda1 * (pp2[1] - pp1[1])

        if pp1[0] <= px <= pp2[0] and pp3[0] <= px <= pp4[0]:
            return px, py
        return None

    def draw(self, surface: pygame.surface.Surface):
        pygame.draw.line(surface, self.color, self.p1, self.p2)
