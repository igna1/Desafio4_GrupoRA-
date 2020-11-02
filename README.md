# Desafío 4 Grupo RA

## Descripción
	
El programa consiste en el entrenamiento de un carrito, el cual se mueve por un circuito cerrado, para que logre completar el circuito sin chocar. Esto, se realiza a través del entrenamiento de varias generaciones, todas entrenadas a través de una red neuronal (MLP), utilizando un algoritmo genético. 


## Estructura

Para la realización del aprendizaje se utilizó un modelo MLP para la red neuronal y un algoritmo genético para el entrenamiento de dicha red. Además, se crearon clases enfocadas en la representación gráfica de la solución, una vez completado el entrenamiento.

### Car

Entre las principales clases tenemos el auto como tal, representa los individuos que serán entrenados a través de la red y se hace relevante entregar una descripción de sus principales variables:

**x e y**: Son valores que representan su ubicación dentro del espacio. 
**rotation**: Representa el ángulo en que se encuentra el auto, representado en radianes.
**crashed**: Valor booleano que representa si el auto ha chocado o no.
**segments**: Una lista con segmentos, que dan forma al vehículo. 
lidar: Es la representación de los láseres que salen desde el vehículo y permiten la detección de segmentos cercanos.

### MLP

Se define mediante dos clases, Neural Network y Layer. La primera contiene un conjunto de Layer y se encarga de recibir las entradas y retornar las predicciones. Estas predicciones se llevan a cabo usando la función sigmoidea como función de activación en todos sus niveles lo que permite obtener resultados entre 0 y 1.

La clase Layer, está encargada de administrar los pesos y sesgos de una determinada capa dentro de la red neuronal. Estos pesos y sesgos son representados como arreglos de numpy los cuales alimentan a la función de activación.

El modelo de red utilizado consiste en tres capas. La primera es la capa de entrada. Recibe la información proveniente del carro y por defecto son nueve valores, los que informan acerca de los alrededores de éste. Luego, está la capa oculta que concentra cinco neuronas por defecto, estas cinco neuronas son alimentadas desde las nueve entradas mencionadas anteriormente y trabajan la información recibida. Además, esta capa oculta y cualquier otra que sea agregada llevan una neurona  de sesgo que permite equilibrar el comportamiento de la red. Finalmente, se tiene una capa de salida que recibe el contenido de la capa oculta previa; contiene sólo dos neuronas y entregan la información de la predicción realizada.

Estas salidas representan la dirección que debe tomar el carrito en la situación evaluada. dichas direcciones pueden ser izquierda, derecha o continuar en la misma dirección. Cabe mencionar que los virajes a izquierda son pequeños, para que se puedan afrontar diferentes tipos de curvas.


| Dirección         | Salida 1 | Salida 2 |
|-------------------|----------|----------|
| Izquierda         | 1        | X        |
| Derecha           | X        | 1        |
| Continuar derecho | 0        | 0        |


### Algoritmo Genético

El entrenamiento de la red descrita previamente es realizada por una implementación simple de algoritmo genético formado por dos clases, Individual y Genetic Algorithm.

La clase Individual representa a una entidad dentro de la población a crear, en este caso es un carrito. Contiene métodos para cálculo de fitness, preparación de cromosomas y sobreescritura de datos (explicado más abajo). Mientras que la clase de algoritmo genético se encarga de orquestar todo el proceso evolutivo.

En un principio, se crea la población de individuos solicitada. cada individuo contiene un carro (el cual tiene una red neuronal) y el fitness de dicho carro; debido a que en esta situación se evalúa un problema de maximización, el valor de fitness default es - infinito. Luego, se calcula el fitness de cada individuo de la población que tenga asignado el fitness default para luego ordenar cada elemento de acuerdo a la calidad de su solución. Entonces, se realiza la recombinación y selección de padres. Para esto, se seleccionan dos padres utilizando un método de ruleta, de los cuales se obtienen sus genes. Una vez obtenidos los cromosomas de ambos padres, se define el índice donde los vectores se dividen para formar dos nuevos hijos. Luego, cuando los hijos han sido creados, se someten a un proceso de mutación, donde se itera diez veces sobre cada nuevo set de cromosomas y se evalúa la probabilidad de que ocurra una modificación en un cromosoma, si esto ocurre, un elemento seleccionado del genotipo es alterado por un valor aleatorio. 

Cuando el proceso de cruzamiento de padres y mutación de hijos ha finalizado, se seleccionan los n peores individuos de la iteración anterior y sus contenidos son reemplazados por los nuevos hijos. Con esto, termina el proceso de reproducción de individuos y se evalúa la condición de término. Para términos prácticos se definen por defecto un fitness máximo de 3000 y un total de 30 generaciones. Si la condición de término no es satisfecha, se evalúan los nuevos individuos y el proceso es realizado nuevamente.

#### Obtención de genes

Para obtener los genes de un individuo se acude a la red neuronal asociada a un individuo. Luego se obtiene cada capa de la red neuronal y de estas sus pesos y sesgos. Estos se agregan a una lista a través de un proceso iterativo para luego concatenarlos. Este vector de valores concatenados corresponde a los genes del individuo.
