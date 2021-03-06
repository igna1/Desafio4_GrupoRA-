from src.grapher import Grapher
from training_methods.genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from training_methods.genetic_algorithm.individual import Individual
from src.problem.world import World


# WORLD = 'worlds/world_large.json'
# WORLD = 'worlds/ezworld.json'
# WORLD = 'worlds/world3.json'
# WORLD = 'worlds/001.json'
# WORLD = 'worlds/002.json'
# WORLD = 'worlds/003.json'
# WORLD = 'worlds/004.json'
WORLD = 'worlds/005.json'


def main():
    import random
    ran =random.randint(1, 1234567)
    random.seed(ran)
    print(f'seed: {ran}')
    # stop_condition = None  # Condicion de termino para AG (no implementado)
    worlds_list = [
        'worlds/ezworld.json',
        # 'worlds/world3.json',
        # 'worlds/001.json',
        # 'worlds/002.json',
        # 'worlds/003.json',
        # 'worlds/004.json',
        #  'worlds/005.json'
    ]
    population = 15  # Poblacion inicial
    lambda_ = 12  # Cantidad de nuevos hijos
    mu = 15  # Cantidad de padres
    mutation = 0.07  # Probabilidad de mutacion
    crossover = None  # dejar siempre en None

    shape_network = [5]  # Forma que tiene la red
    world = World(WORLD)
    x = 162
    y = 302
    rotation = -1.6
    worlds = [World(w) for w in worlds_list]

    fitness = 3000
    generations = 30

    genetic = GeneticAlgorithm(initial_population=population,
                               lambda_=lambda_,
                               mu=mu,
                               selection=None,
                               mutation=mutation,
                               crossover=crossover,
                               world=world,
                               hidden_layers=shape_network,
                               x=x, y=y, rotation=rotation, fitness=fitness,
                               generations=generations,
                               instances=worlds
                               )

    try:
        genetic.pick_weights()
    except FileNotFoundError:
        print('no existen pesos guardados')

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
