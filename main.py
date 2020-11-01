from src.grapher import Grapher
from src.problem.segment import Segment
from training_methods.genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from training_methods.genetic_algorithm.individual import Individual
from src.problem.world import World


WORLD = 'worlds/world_large.json'
# WORLD = 'world/ezworld.json'
# WORLD = 'world/world3.json'
# WORLD = 'world/001.json'
# WORLD = 'world/002.json'
# WORLD = 'world/003.json'
# WORLD = 'world/004.json'
# WORLD = 'world/005.json'


def main():
    import random
    ran =random.randint(1, 1234567)
    random.seed(ran)
    print(f'seed: {ran}')
    # stop_condition = None  # Condicion de termino para AG (no implementado)
    worlds_list = [
        'worlds/ezworld.json',
        'worlds/world3.json',
        'worlds/001.json',
        'worlds/002.json',
        'worlds/003.json',
        'worlds/004.json',
         'worlds/005.json'
    ]
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
    worlds = [World(w) for w in worlds_list]

    fitness = 3000
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
                               generations=generations, instances=worlds)

    genetic.pick_weights()
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
    main()
    main_old()
