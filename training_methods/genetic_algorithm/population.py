from . import individual
import numpy as np


def create_population(nb_population: int):
    """
    Crea una población para el algoritmo genético.

    :param nb_population: Cantidad de individuos en la población
    :return: Arreglo de numpy con la población creada
    """
    population = np.ndarray((nb_population,), dtype=np.object)
    for i in range(nb_population):
        population[i] = individual.Individual()

    return population


class GeneticAlgorithm:

    def __init__(self, initial_population, lambda_, mu, selection, mutation,
                 crossover, problem, stop_condition):
        self.initial_population = initial_population
        self.population = create_population(initial_population)
        self.problem = problem
        self.lambda_ = lambda_
        self.mu = mu
        self.selection = selection
        self.mutation = mutation
        self.crossover = crossover
        self.stop_condition = stop_condition

    def parent_selection(self):
        """
        Realiza la seleccion de padres de la nueva generación

        :return:
        """
        pass

    def crossover(self):
        """
        Lleva a cbao la combinación genética de los padres para crear una nueva
        entidad.

        :return:
        """
        pass

    def mutation(self):
        """
        Realiza modificaciones sobre un individuo para mejorar la
        diversificación de la búsqueda.

        :return:
        """
        pass

    def selection(self):
        """
        Selecciona los individuos que sobrevivirán para la próxima iteración.

        :return:
        """
        pass

    def stop_condition(self):
        """
        Evalúa la condición de termino asignada para finalizar la búsqueda.

        :return:
        """
        pass
