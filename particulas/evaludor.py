import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir la función objetivo
def objective_function(x, y):
    return x**2 + y**2

# Crear una malla de puntos en el intervalo [-1, 10]
x = np.linspace(-1, 10, 400)
y = np.linspace(-1, 10, 400)
X, Y = np.meshgrid(x, y)
Z = objective_function(X, Y)

# Graficar la función objetivo en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

# Etiquetas y título
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Valor de la función objetivo')
ax.set_title('Función objetivo en 3D en el intervalo [-1, 10]')

plt.show()
