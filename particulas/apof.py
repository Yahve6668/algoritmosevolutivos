
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x[0]**2 + x[1]**2

numero_de_particulas = 3
iteraciones = 30
numero_posiciones_por_partícula = 10
dimenciones = 2  
bounds = [-1, 10]
w = 0.5 
c1 = 1.5  
c2 = 1.5  

posicion_particulas = np.random.uniform(bounds[0], bounds[1], (numero_de_particulas, numero_posiciones_por_partícula, dimenciones))
velocidad_particulas = np.zeros((numero_de_particulas, numero_posiciones_por_partícula, dimenciones))
mejor_posicion_part = np.zeros((numero_de_particulas, dimenciones))
mejor_valor_part = np.full(numero_de_particulas, np.inf)

# Evaluar las posiciones iniciales
for i in range(numero_de_particulas):
    for j in range(numero_posiciones_por_partícula):
        evaluacion = f(posicion_particulas[i, j])
        if evaluacion < mejor_valor_part[i]:
            mejor_valor_part[i] = evaluacion
            mejor_posicion_part[i] = posicion_particulas[i, j].copy()

mejor_posicion_global = mejor_posicion_part[np.argmin(mejor_valor_part)]
mejor_valor_global= np.min(mejor_valor_part)


mejores_valores = []
puntos_mejores = []
iteraciones_mejores = []


for iteration in range(iteraciones):
    for i in range(numero_de_particulas):
        for j in range(numero_posiciones_por_partícula):
            r1 = np.random.random(dimenciones)
            r2 = np.random.random(dimenciones)

            velocidad_particulas[i, j] = (w * velocidad_particulas[i, j] +
                                        c1 * r1 * (mejor_posicion_part[i] - posicion_particulas[i, j]) +
                                        c2 * r2 * (mejor_posicion_global - posicion_particulas[i, j]))
            
            
            posicion_particulas[i, j] += velocidad_particulas[i, j]
            
            #limitar a que este en lo limites
            posicion_particulas[i, j] = np.clip(posicion_particulas[i, j], bounds[0], bounds[1])
            
            evaluacion = f(posicion_particulas[i, j])
            
            # mejor actual
            if evaluacion < mejor_valor_part[i]:
                mejor_valor_part[i] = evaluacion
                mejor_posicion_part[i] = posicion_particulas[i, j].copy()
                
                # mejor global
                if evaluacion < mejor_valor_global:
                    mejor_valor_global= evaluacion
                    mejor_posicion_global = posicion_particulas[i, j].copy()
    
    mejores_valores.append(mejor_valor_global)
    puntos_mejores.append(mejor_posicion_global.copy())
    iteraciones_mejores.append(iteration)
    print(f"Iteración {iteration+1}/{mejor_posicion_global}, Mejor valor: {mejor_valor_global}")


print("Mejor posición encontrada:", mejor_posicion_global)
print("Mejor valor encontrado:", mejor_valor_global)
print(puntos_mejores)

plt.plot(mejores_valores, label='Mejor valor')
plt.scatter(iteraciones_mejores, mejores_valores, color='red', marker='o', label='Mejores posiciones')

for i, txt in enumerate(puntos_mejores):
    plt.text(iteraciones_mejores[i], mejores_valores[i], f"({txt[0]:.2f}, {txt[1]:.2f})", fontsize=8, ha='right')

plt.xlabel('Iteración')
plt.ylabel('Mejor valor')
plt.title('Evolución del mejor valor encontrado por PSO')
plt.yscale('log')  
plt.legend()
plt.show()

def f(x, y):
    return x**2 + y**2

x = np.linspace(-1, 10, 400)
y = np.linspace(-1, 10, 400)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

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