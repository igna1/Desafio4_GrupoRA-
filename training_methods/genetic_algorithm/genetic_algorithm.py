from . import individual
import numpy as np
import random


def create_population(nb_population: int, hidden_layers, world, x, y, rotation):
    """
    Crea una población para el algoritmo genético.

    :param hidden_layers: Forma de la red
    :param nb_population: Cantidad de individuos en la población
    :return: Arreglo de numpy con la población creada
    """
    population = np.ndarray((nb_population,), dtype=np.object)
    for i in range(nb_population):
        population[i] = individual.Individual(world, x, y, rotation, hidden_layers)

    return population


class GeneticAlgorithm:

    def __init__(self, initial_population, lambda_, mu, selection,
                 mutation, crossover, world, hidden_layers, x, y, rotation, fitness=np.inf, generations=50,
                 instances=None):
        self.initial_population = initial_population
        self.population = create_population(initial_population, hidden_layers, world, x, y, rotation)
        self.problem = world
        self.lambda_ = lambda_
        self.mu = mu
        self.mutation_rate = mutation
        self.best_agent = None
        self.best_fitness = -1 * np.inf
        self.generations = 0
        self.max_fitness = fitness
        self.max_gen = generations
        self.instances = instances if instances is not None else None

    def execute(self):
        while not self.stop_condition():
            self.evaluate()
            self.population = sorted(self.population,
                                     key=lambda x: x.fitness,
                                     reverse=True)

            self.best_agent = self.population[0]
            self.best_fitness = self.population[0].fitness

            offsprings = self.crossover()
            self.mutation(offsprings)

            self.selection(offsprings)

            self.generations += 1
            print(f'{self.generations} '
                  f'best current fitness: {self.best_fitness} '
                  f'{self.population[1].fitness} '
                  f'{self.population[2].fitness}\t '
                  f'size: {len(self.population)}')

        print(f'best agent fitness: {self.best_agent.fitness}')
        self.best_agent.save()
        return self.best_agent

    def pick_weights(self):
        self.population[0].load()

    def parent_selection(self):
        """
        Realiza la seleccion de padres de la nueva generación

        :return:
        """
        # Ordenando entidades de acuerdo a su fitness

        self.population = sorted(self.population,
                                 key=lambda x: x.fitness,
                                 reverse=True)
        # Selección de elementos padre de la siguiente generación
        fitness_list = np.array([agent.fitness for agent in self.population])

        first_parent = self.__pick_parent(random.random(),
                                          fitness_list/sum(fitness_list))
        np.delete(fitness_list, first_parent)
        second_parent = self.__pick_parent(random.random(),
                                           fitness_list/sum(fitness_list))

        return self.population[first_parent], self.population[second_parent]

    def __pick_parent(self, probability, candidates):
        """
        Selecciona un padre de acuerdo a un valor aleatorio
        :param probability: valor aleatorio entregado
        :param candidates: lista de padres candidatos
        :return: indice del padre candidato
        """
        counter = 0

        while True:
            if sum(candidates[0: counter+1]) >= probability:
                break
            counter += 1
        return counter

    def crossover(self):
        """
        Lleva a cbao la combinación genética de los padres para crear una nueva
        entidad.

        :return:
        """
        offsprings = np.empty([self.lambda_,
                               individual.Individual.size_flattened],
                              dtype=np.object)

        for i in range(0, self.lambda_, 2):
            first_parent, second_parent = self.parent_selection()
            split_point = random.randint(0,
                                         individual.Individual.size_flattened-1)

            genes_1 = first_parent.get_genes()
            genes_2 = second_parent.get_genes()

            # print(genes_1[0:split_point-1], genes_1[0:split_point-1].shape)
            # print(genes_2[split_point:-1], genes_2[split_point:-1].shape)

            offsprings[i] = np.concatenate((genes_1[0:split_point+1],
                                           genes_2[split_point:-1]))
            offsprings[i+1] = np.concatenate((genes_2[0:split_point+1],
                                             genes_1[split_point:-1]))

        return offsprings

    def mutation(self, offsprings):
        """
        Realiza modificaciones sobre un individuo para mejorar la
        diversificación de la búsqueda.

        :return:
        """
        for child in offsprings:
            for i in range(random.randint(1, 10)):
                random_value = random.uniform(-1, 1)
                random_choice = random.randint(0,
                                               individual.Individual.size_flattened-1)

                if random.random() <= self.mutation_rate:
                    child[random_choice] = random_value

    def evaluate(self):
        # Calcular el fitness de cada individuo
        # Propuesta: ejecutar solamente los nuevos individuos creados
        for car in self.population:
            car.calculate_fitness(self.instances)
            print('.', end='')

        print('\n')

    def selection(self, offsprings):
        """
        Selecciona los individuos que sobrevivirán para la próxima iteración.

        :return:
        """
        if self.lambda_ < self.mu:
            for i in range(self.lambda_):
                agent = self.population[-1*(i+1)]
                agent.overwrite(offsprings[i])
        elif self.lambda_ > self.mu:
            pass
        else:
            raise ValueError("Lambda no puede ser igual a mu")

    def stop_condition(self):
        """
        Evalúa la condición de termino asignada para finalizar la búsqueda.
        :return:
        """
        if self.best_fitness > self.max_fitness or self.generations > self.max_gen:
            return True
        return False

