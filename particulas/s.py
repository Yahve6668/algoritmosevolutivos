import numpy as np
import matplotlib.pyplot as plt

# Definir la función objetivo
def objective_function(x):
    return x[0]**2 + x[1]**2

# PSO parámetros
num_particles = 2
num_iterations = 20
num_positions_per_particle = 10
dim = 2  # número de parámetros de la función objetivo
bounds = [-1, 10]

# Inicializar la población de partículas con múltiples posiciones
particles_position = np.random.uniform(bounds[0], bounds[1], (num_particles, num_positions_per_particle, dim))
particles_velocity = np.zeros((num_particles, num_positions_per_particle, dim))
personal_best_position = np.zeros((num_particles, dim))
personal_best_value = np.full(num_particles, np.inf)

# Evaluar las posiciones iniciales
for i in range(num_particles):
    for j in range(num_positions_per_particle):
        current_value = objective_function(particles_position[i, j])
        if current_value < personal_best_value[i]:
            personal_best_value[i] = current_value
            personal_best_position[i] = particles_position[i, j].copy()

global_best_position = personal_best_position[np.argmin(personal_best_value)]
global_best_value = np.min(personal_best_value)

# Parámetros de PSO
w = 0.5  # inercia
c1 = 1.5  # coeficiente cognitivo
c2 = 1.5  # coeficiente social

# Almacenar los mejores valores de cada iteración
best_values = []
puntos_mejores = []
# PSO iteraciones
for iteration in range(num_iterations):
    for i in range(num_particles):
        for j in range(num_positions_per_particle):
            # Actualizar velocidad
            r1 = np.random.random(dim)
            r2 = np.random.random(dim)
            print(r1)
            print(r2)
            particles_velocity[i, j] = (w * particles_velocity[i, j] +
                                        c1 * r1 * (personal_best_position[i] - particles_position[i, j]) +
                                        c2 * r2 * (global_best_position - particles_position[i, j]))
            
            # Actualizar posición
            particles_position[i, j] += particles_velocity[i, j]
            
            # Aplicar límites
            particles_position[i, j] = np.clip(particles_position[i, j], bounds[0], bounds[1])
            
            # Evaluar la nueva posición
            current_value = objective_function(particles_position[i, j])
            
            # Actualizar el mejor valor personal
            if current_value < personal_best_value[i]:
                personal_best_value[i] = current_value
                personal_best_position[i] = particles_position[i, j].copy()
                
                # Actualizar el mejor valor global
                if current_value < global_best_value:
                    global_best_value = current_value
                    global_best_position = particles_position[i, j].copy()
    
    best_values.append(global_best_value)
    puntos_mejores.append(global_best_position)
    print(f"Iteración {iteration+1}/{num_iterations}, Mejor valor: {global_best_value}")

# Graficar los mejores valores de cada iteración

print("Mejor posición encontrada:", global_best_position)
print("Mejor valor encontrado:", global_best_value)

plt.plot(best_values)
plt.xlabel('Iteración')
plt.ylabel('Mejor valor')
plt.title('Evolución del mejor valor encontrado por PSO')
plt.show()