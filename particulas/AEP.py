import numpy as np
import math

# Parámetros
w=0.5       # Inercia
c1=1.5       # Coeficiente de aprendizaje 1
c2=1.5        # Coeficiente de aprendizaje 2
a=0         # Cota inferior para la función objetivo
b=4         # Cota superior para la función objetivo
p=5         # Número de partículas
n=10       # Número de iteraciones

# Función Objetivo
def f(x):
    f = (pow((x-2), 2) + 3)
    return f

# Algoritmo de enjambre de partículas
def AEP(particulas_de_x):
    # Posición inicial entre una cota inferior a y una cota superior b
    x_t = np.random.uniform(a, b, (p))
    # Velocidad inicial de 0
    v_t = np.zeros((p))

    # Mejores valores de x, f(x)
    p_best_x = np.copy(x_t)
    p_best_f_de_x = np.array([particulas_de_x(p) for p in x_t])
    g_best_x = p_best_x[np.argmin(p_best_f_de_x)]
    g_best_f_de_x = np.min(p_best_f_de_x)

    # Iteraciones que actualizan la posición y velocidad
    for i in range(n):
        # Números aleatorios uniformes entre 0 y 1
        r1 = np.random.uniform(0, 1, (p))
        r2 = np.random.uniform(0, 1, (p))

        # Nueva velocidad
        v_t = w * v_t + c1 * r1 * (p_best_x - x_t) + c2 * r2 * (g_best_x - x_t)

        # Nueva posición
        x_t = x_t + v_t

        # Valores f(x) para cada partícula
        valores_f_de_x = np.array([particulas_de_x(p) for p in x_t])

        # Los valores de x, f(x) se actualizan
        indices_de_las_particulas = np.where(valores_f_de_x < p_best_f_de_x)
        p_best_x[indices_de_las_particulas] = x_t[indices_de_las_particulas]
        p_best_f_de_x[indices_de_las_particulas] = valores_f_de_x[indices_de_las_particulas]
        if np.min(valores_f_de_x) < g_best_f_de_x:
            g_best_x = x_t[np.argmin(valores_f_de_x)]
            g_best_f_de_x = np.min(valores_f_de_x)

    # Regresa los mejores valores de x, f(x)
    return g_best_x, g_best_f_de_x

# Corre el algoritmo de enjambre de partículas para la función f(x)
solucion = AEP(f)

# Imprime los valores de la solución 
print('La solucion x, f(x):', solucion)