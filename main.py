from src.grapher import Grapher
from src.problem.segment import Segment
from training_methods.genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from training_methods.genetic_algorithm.individual import Individual
from src.problem.world import World


def load_instances(path):
    return 0

WORLD = 'world_large.json'
# WORLD = 'ezworld.json'
# WORLD = 'world3.json'

def main():
    # Cargar los archivos de pistas
    instances = load_instances(".")  # cargar un circuito
    # stop_condition = None  # Condicion de termino para AG (no implementado)
    population = 100  # Poblacion inicial
    lambda_ = 12  # Cantidad de nuevos hijos
    mu = 100  # Cantidad de padres
    mutation = 0.07  # Probabilidad de mutacion
    crossover = None  # dejar siempre en None

    shape_network = [5]  # Forma que tiene la red
    world = World(WORLD)
    x = 162
    y = 302
    rotation = -1.6

    fitness= 3000
    generations = 50

    genetic = GeneticAlgorithm(initial_population=population,
                               lambda_=lambda_,
                               mu=mu,
                               selection=None,
                               mutation=mutation,
                               crossover=crossover,
                               world=world,
                               hidden_layers=shape_network,
                               x=x, y=y, rotation=rotation, fitness=fitness,
                               generations=generations)

    genetic.execute()

    print(f"Ejecución terminada. Mejor fitness encontrado: {genetic.best_fitness}.")

    pass

def main_indivual():
    world = World()
    indiv = Individual(world, 162, 301, -1.6, [3])
    indiv.print_status()

def main_old():
    grapher = Grapher(WORLD)
    grapher.run()


if __name__ == "__main__":
    # main()
    main_old()
