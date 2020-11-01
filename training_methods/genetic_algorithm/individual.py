import numpy as np
import neural_network as nn

DEFAULT_FITNESS = -1 * np.inf


class Individual:

    """
    Para efectos del desafío debe recibir una red completa
    """
    size_flattened = 0

    def __init__(self, shape_network):
        self.network = nn.Neural_Network(shape_network[0])
        for i in range(1, len(shape_network)):
            self.network.add_layer(shape_network[i])
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


if __name__ == '__main__':
    ind = Individual([4,10,4])
    print(ind.network.layers)
