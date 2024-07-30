import numpy as np
import random

NUM_HORMIGAS = 0
MAX_ITERACIONES = 0 
ALPHA = 0 # Influencia de la feromona
BETA = 0 # Influencia de la distancia
RHO  = 0 # Tasa de evaporación de la feromona ppp
Q   = 0  # Cantidad de feromona depositada por una hormiga


def actualizar_feromonas(recorridos, longitudes, feromonas):
    feromonas *= (1.0 - RHO)
    for k in range(len(recorridos)):
        delta_feromona = Q / longitudes[k]
        for i in range(len(recorridos[k]) - 1):
            ciudad_actual = recorridos[k][i]
            ciudad_siguiente = recorridos[k][i + 1]
            feromonas[ciudad_actual][ciudad_siguiente] += delta_feromona
            feromonas[ciudad_siguiente][ciudad_actual] += delta_feromona
    #print(feromonas)            

def seleccionar_proxima_ciudad(ciudad_actual, visitadas, distancias, feromonas):
    num_ciudades = distancias.shape[0]
    probabilidades = np.zeros(num_ciudades)
    suma_probabilidades = 0.0
    

    for j in range(num_ciudades):
        if not visitadas[j] and distancias[ciudad_actual][j] != float('inf'):
            probabilidades[j] = (feromonas[ciudad_actual][j] ** ALPHA) * ((1.0 / distancias[ciudad_actual][j]) ** BETA)
            suma_probabilidades += probabilidades[j]
    
    # Evitar división por cero si todas las probabilidades son cero
    if suma_probabilidades == 0:
        return -1  # O manejar de otra forma si no hay probabilidades válidas
    
    # Normalizar las probabilidades
    probabilidades_normalizadas = probabilidades / suma_probabilidades
    
    # Selección de la próxima ciudad basada en la probabilidad normalizada ciudad proximas
    valor_aleatorio = random.uniform(0, 1)
    suma_parcial = 0.0
    for j in range(num_ciudades):
        if not visitadas[j] and distancias[ciudad_actual][j] != float('inf'):
            suma_parcial += probabilidades_normalizadas[j]
            if suma_parcial >= valor_aleatorio:
                return j
    
    return -1


def aco(distancias,ciudad_inicio,valor_tau):
    num_ciudades = distancias.shape[0]
    feromonas = np.full((num_ciudades, num_ciudades), valor_tau)
    mejor_recorrido = None
    mejor_longitud = float('inf')

    for iteracion in range(MAX_ITERACIONES):
        recorridos = []
        longitudes = []

        for k in range(NUM_HORMIGAS):
            visitadas = [False] * num_ciudades
            ciudad_inicial = ciudad_inicio
            recorrido = [ciudad_inicial]
            visitadas[ciudad_inicial] = True

            for i in range(1, num_ciudades):
                ciudad_actual = recorrido[-1]
                proxima_ciudad = seleccionar_proxima_ciudad(ciudad_actual, visitadas, distancias, feromonas)
                recorrido.append(proxima_ciudad)
                visitadas[proxima_ciudad] = True

            recorrido.append(recorrido[0])
            longitud = sum(distancias[recorrido[i]][recorrido[i + 1]] for i in range(num_ciudades))

            recorridos.append(recorrido)
            longitudes.append(longitud)

            if longitud < mejor_longitud:
                mejor_longitud = longitud
                mejor_recorrido = recorrido

        actualizar_feromonas(recorridos, longitudes, feromonas)

        print(f"Iteración {iteracion + 1}: Mejor longitud de recorrido = {mejor_longitud}")

    print("Mejor recorrido encontrado:")
    print(mejor_recorrido)

    

if __name__ == "__main__":
    num_ciudades = int(input("Ingrese el número de ciudades: "))
    ciudad_ini = int(input("Ingrese el número de la ciudad ciudad inicial: "))
    NUM_HORMIGAS = int(input("N de hormigas: "))
    MAX_ITERACIONES = int(input("N iteraciones"))
    ALPHA = float(input("N alfa"))
    BETA = float(input("N beta"))
    RHO = float(input("N rho(p) "))
    Q = float(input("N DE q"))
    tau = float(input("tau "))
    matriz = np.zeros((num_ciudades, num_ciudades))
    for i in range(num_ciudades):
        fila = input(f"Ciudad {i + 1}: ").split()
        for j in range(num_ciudades):
            if i == j:
                matriz[i][j] = float('inf')
            else:
                matriz[i][j] = float('inf') if fila[j] == 'inf' else float(fila[j])

    aco(matriz,ciudad_ini,tau)