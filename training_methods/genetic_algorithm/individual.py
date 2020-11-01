import numpy as np
import neural_network as nn
from src.problem.car import Car

DEFAULT_FITNESS = -1 * np.inf


class Individual:

    """
    Para efectos del desafío debe recibir una red completa
    """
    size_flattened = 0

    def __init__(self, world, x, y, rotation, hidden_layers=None):
        self.car = Car(world, x, y, rotation, hidden_layers)

        Individual.size_flattened = self.car.brain.size()

        self.fitness = DEFAULT_FITNESS

    def print_status(self):
        print(f"size: {Individual.size_flattened}\n"
              f"fitness: {self.fitness}")

    def calculate_fitness(self):
        self.car.update()
        self.fitness = self.car.distance
        return self.fitness

    def get_genes(self):
        """
        Obtiene los pesos de la red neuronal aplanados
        :return:
        """
        layers = []
        for layer in self.car.brain.layers:
            layers.append(layer.weights.flatten())
        return np.concatenate(layers)

    def overwrite(self, weights):
        """
        Sobreescribe los pesos de una red neuronal y setea su fitness a -inf
        :param weights:
        :return:
        """
        self.fitness = DEFAULT_FITNESS
        section = 0
        for layer in self.car.brain.layers:
            size = layer.weights.size
            # print(section, size)
            layer.weights = weights[section: section+size].reshape(layer.weights.shape)

            section += size

