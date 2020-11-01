from src.grapher import Grapher
from src.problem.segment import Segment
from training_methods.genetic_algorithm.genetic_algorithm import GeneticAlgorithm


def load_instances(path):
    return 0


def main():
    # Cargar los archivos de pistas
    instances = load_instances(".")  # cargar un circuito
    stop_condition = None  # Condicion de termino para AG (no implementado)
    population = 100  # Poblacion inicial
    lambda_ = 4  # Cantidad de nuevos hijos
    mu = 100  # Cantidad de padres
    mutation = 0.2  # Probabilidad de mutacion
    crossover = None  # dejar siempre en None

    shape_network = [5, 15, 2]  # Forma que tiene la red

    genetic = GeneticAlgorithm(initial_population=population,
                               lambda_=lambda_,
                               mu=mu,
                               selection=None,
                               mutation=mutation,
                               crossover=crossover,
                               problem=instances,
                               stop_condition=stop_condition,
                               shape_network=shape_network
                               )

    genetic.execute()

    print(f"Ejecución terminada. Mejor fitness encontrado: {genetic.best_fitness}.")

    pass


def main_old():
    grapher = Grapher()
    grapher.run()


if __name__ == "__main__":
    main()
