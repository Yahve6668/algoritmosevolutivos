import numpy as np

# Definir la función objetivo
def objective_function(x):
    return x[0]**2 + x[1]**2

# PSO parámetros
num_particles = 30
num_iterations = 1000
dim = 2  # número de parámetros de la función objetivo
bounds = [-1, 10]

# Inicializar la población de partículas
particles_position = np.random.uniform(bounds[0], bounds[1], (num_particles, dim))
print(particles_position)
particles_velocity = np.zeros((num_particles, dim))
personal_best_position = particles_position.copy()
personal_best_value = np.array([objective_function(p) for p in particles_position])
global_best_position = personal_best_position[np.argmin(personal_best_value)]
global_best_value = np.min(personal_best_value)

# Parámetros de PSO
w = 0.5  # inercia
c1 = 1.5  # coeficiente cognitivo
c2 = 1.5  # coeficiente social

# PSO iteraciones
for iteration in range(num_iterations):
    for i in range(num_particles):
        # Actualizar velocidad
        r1 = np.random.random(dim)
        r2 = np.random.random(dim)
        particles_velocity[i] = (w * particles_velocity[i] +
                                 c1 * r1 * (personal_best_position[i] - particles_position[i]) +
                                 c2 * r2 * (global_best_position - particles_position[i]))
        
        # Actualizar posición
        particles_position[i] += particles_velocity[i]
        
        # Aplicar límites
        particles_position[i] = np.clip(particles_position[i], bounds[0], bounds[1])
        
        # Evaluar la nueva posición
        current_value = objective_function(particles_position[i])
        
        # Actualizar el mejor valor personal
        if current_value < personal_best_value[i]:
            personal_best_value[i] = current_value
            personal_best_position[i] = particles_position[i].copy()
        
        # Actualizar el mejor valor global
        if current_value < global_best_value:
            global_best_value = current_value
            global_best_position = particles_position[i].copy()
    
    print(f"Iteración {iteration+1}/{num_iterations}, Mejor valor: {global_best_value}")

print("Mejor posición encontrada:", global_best_position)
print("Mejor valor encontrado:", global_best_value)
