import numpy as np

DEFAULT_FITNESS = -1 * np.inf


class Individual:

    """
    Para efectos del desafío debe recibir una red completa
    """
    size_flattened = 0

    def __init__(self, shape_network):
        # TODO: Crear red dentro de individuo
        self.network = None
        Individual.size_flattened = sum(shape_network)
        self.fitness = DEFAULT_FITNESS

    def calculate_fitness(self):
        fitness = 0

        self.fitness = fitness
        return fitness
        pass

    def get_genes(self):
        """
        Obtiene los pesos de la red neuronal aplanados
        :return:
        """
        layers = []
        for layer in self.network.layers:
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
        for layer in self.network.layers:
            size = layer.weights.size
            layer.weights = weights[section: size].reshape(layer.weights.shape)

            section += size
