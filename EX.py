import operator
import math
import random
import numpy as np
from deap import algorithms, base, creator, tools, gp
import networkx as nx
import matplotlib.pyplot as plt
import sympy as sp

def not_cero(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

# Definir las funciones para el algoritmo genético  se toma cada una de ellas 
# toma dos parámetros:
#  individual: Un individuo en la población en  expresión simbólica representado en DEAP.
#  points: Una lista de pares (x, y) que representa los datos de entrenamiento para la regresión.
#  (func(x) - y) ** 2: Calcula el cuadrado del error entre la predicción func(x) y el valor real y.
#  math.fsum(...): Suma todos los errores cuadrados.
def evalSymbReg(individual, points):
    func = toolbox.compile(expr=individual)
    return math.fsum(((func(x) - y) ** 2 for x, y in points)) / len(points),

#datos de ejemplo 
x = [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
y = [0.0000, -0.1629, -0.2624, -0.3129, -0.3264, -0.3125, -0.2784, -0.2289, -0.1664, -0.0909, 0.0000, 0.1111, 0.2496, 0.4251, 0.6496, 0.9375, 1.3056, 1.7731, 2.3616, 3.0951, 4.0000]

#Definicion de las operaciones 
pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2) # operando y cuantos necesita el mismo 
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(not_cero, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)

#definicion de las contantes efimeras [-1,1]
pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
#renomaobramiento de los terminales a X 
pset.renameArguments(ARG0='x')


#Definicion de problema fitnes se quiere minimizar errores  Un valor negativo (-1.0)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
#creacion de los indiviudos  y se indica que son arboles primitivos  , y decimo que cada uno de lelos seran evaludos en la funcion fitnes 
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

# se usa para registrar operaciones y funciones necesarias para el algoritmo
toolbox = base.Toolbox()
# crear árboles de funciones. onjunto de primitivos y terminales definido  Especifican las profundidades mínima y máxima de los árboles generados.
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)

# función para generar la expresión (árbol de funciones).
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
# crear una lista de individuos.  , estrutura , La función para crear un individuo.
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#  convertir árboles de funciones en funciones ejecutables.
toolbox.register("compile", gp.compile, pset=pset)

# usa evalSymbReg para calcular el fitness de los individuos. toma los datos 
toolbox.register("evaluate", evalSymbReg, points=list(zip(x, y)))

# selección por torneo , El tamaño del torneo para la selección.El tamaño del torneo para la selección.
toolbox.register("select", tools.selTournament, tournsize=3)

#  utiliza el cruce de un punto cxOnePoint para combinar dos individuos.
toolbox.register("mate", gp.cxOnePoint)

#  crear árboles completos. Especifican las profundidades mínima y máxima de los árboles generados para la mutación.
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)

# El generador de expresiones para la mutación El conjunto de primitivos y terminales.
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


# Parámetros del algoritmo
pop_size = 300
num_generaciones = 50

# tamaño de la porblacion incial 
pop = toolbox.population(n=pop_size)

# mantendrá los mejores individuos encontrados durante la evolución.
hof = tools.HallOfFame(1)

# ecolectar estadísticas de la población durante la evolución ,extrae los valores de fitness de un individuo
stats = tools.Statistics(lambda ind: ind.fitness.values)

# Registra la estadística "avg" que calculará el promedio de los valores de fitness en la población utilizando
stats.register("avg", np.mean)

# calculará la desviación estándar de los valores de fitnes
stats.register("std", np.std)

#calculará el valor mínimo de los valores de fitness en la población 
stats.register("min", np.min)

# calculará el valor máximo de los valores de fitness en la población
stats.register("max", np.max)

# ejecuta el algoritmo evolutivo simple ,funciones necesarias para la evolución,La probabilidad de cruce (crossover),La probabilidad de mutación, numero generaciones,estaditicas, mejor , imprimir lo que pasa 
pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, num_generaciones, stats=stats, halloffame=hof, verbose=True)

# Imprimir el mejor individuo encontrado
print("Mejor individuo:", hof[0])
print("Fitness:", hof[0].fitness.values[0])


#"""
#generar el arbol en dibujuto 
def plot_tree(nodes, edges, labels):
    g = nx.Graph()
    g.add_edges_from(edges)
    pos = nx.spring_layout(g)
    
    plt.figure(figsize=(12, 8))
    nx.draw(g, pos, node_color='lightblue', 
            node_size=500, 
            with_labels=False, 
            arrows=False)
    
    nx.draw_networkx_labels(g, pos, labels, font_size=10)
    plt.title("Árbol de la solución")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Convertir el mejor individuo a un árbol
nodes, edges, labels = gp.graph(hof[0])

# Visualizar el árbol
plot_tree(nodes, edges, labels)

# Generar predicciones y visualizar los resultados
best_func = toolbox.compile(expr=hof[0])
y_pred = [best_func(xi) for xi in x]

plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Datos reales')
plt.plot(x, y_pred, color='red', label='Predicción')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Regresión Simbólica: Datos reales vs Predicción')
plt.legend()
plt.grid(True)
plt.show()

#"""

# evolucion genetica solo la presnetacion  

# 30 agtos els segundo examen 
# 28 implementacion 
# 29 jueves 
# 30 alforimo difecrncia 30
# presentacion 
# reporte 

