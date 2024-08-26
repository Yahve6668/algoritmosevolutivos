
from sympy import symbols, cos, sin, simplify, Add, Mul, sympify
import operator
import math
import random
import numpy as np
from deap import algorithms, base, creator, tools, gp
import networkx as nx
import matplotlib.pyplot as plt

# Define la variable simbólica
x = symbols('x')

# Función para convertir la cadena de la expresión
def parse_expression(expr_str):
    # Define un diccionario de funciones simbólicas
    func_map = {
        'add': 'Add',
        'mul': 'Mul',
        'sub': '-',
        'cos(0)': '1',
        'sin': 'sin'
    }

    # Reemplaza las funciones simbólicas con las correspondientes
    for func, sym_func in func_map.items():
        expr_str = expr_str.replace(func, sym_func)
    
    # Transforma la cadena en una expresión simbólica usando `sympify`
    return sympify(expr_str)

# Función para convertir un árbol de DEAP en una cadena
def stringify_tree(expr):
    if isinstance(expr, gp.Terminal):
        return str(expr.value)
    elif isinstance(expr, creator.Individual):
        return stringify_tree(expr[0])
    elif isinstance(expr, gp.Primitive):
        name = expr.name
        args = [stringify_tree(arg) for arg in expr.args]
        if name in ["add", "sub", "mul", "protectedDiv"]:
            return f"({args[0]} {expr.format_string} {args[1]})"
        elif name == "neg":
            return f"(-{args[0]})"
        elif name in ["cos", "sin"]:
            return f"{name}({args[0]})"
        else:
            return f"{name}({', '.join(args)})"
    elif isinstance(expr, float):
        return f"{expr:.4f}"
    elif isinstance(expr, int):
        return str(expr)
    else:
        return "x" 

# Definir los datos
x = [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
y = [0.0000, -0.1629, -0.2624, -0.3129, -0.3264, -0.3125, -0.2784, -0.2289, -0.1664, -0.0909, 0.0000, 0.1111, 0.2496, 0.4251, 0.6496, 0.9375, 1.3056, 1.7731, 2.3616, 3.0951, 4.0000]

# Define las funciones primitivas y otros componentes
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1
 
pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

def evalSymbReg(individual, points):
    func = toolbox.compile(expr=individual)
    return math.fsum(((func(x) - y) ** 2 for x, y in points)) / len(points),

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", evalSymbReg, points=list(zip(x, y)))
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

pop_size = 300
num_generations = 50

pop = toolbox.population(n=pop_size)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, num_generations, stats=stats, halloffame=hof, verbose=True)

print("Mejor individuo:", hof[0])
print("Fitness:", hof[0].fitness.values[0])

# Extraer la expresión del mejor individuo en hof
expr_str = stringify_tree(hof[0])

# Convierte la cadena en una expresión simbólica
parsed_expr = parse_expression(expr_str)

# Simplifica la expresión
simplified_expr = simplify(parsed_expr)

# Muestra la expresión simplificada
print("Expresión simplificada:", simplified_expr)

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
