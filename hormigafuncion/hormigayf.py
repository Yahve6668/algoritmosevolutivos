import numpy as np
import itertools
import random
NUM_HORMIGAS = 2
MAX_ITERACIONES = 30
ALPHA = 10.0  # Influencia de la feromona
BETA = 100.0   # Influencia de la distancia
RHO = 0.5    # Tasa de evaporación de la feromona ppp
Q = 100.0    # Cantidad de feromona depositada por una hormiga

def f(x,y):
    return (x)**2 + x*y + (y)**2

def evaluador(lista):

    for i, p in enumerate(lista):
        evaluacion_f[i] = f(p[0], p[1])

    return evaluacion_f;

def punto_medio(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    x_m = (x1 + x2) / 2
    y_m = (y1 + y2) / 2
    return (x_m, y_m)

def generar_puntos_med(puntos,fin):
    n = len(puntos) 
    arr2 = [0] * n  
    
    for i in range(1, n + 1):  
        if i != n:
            arr2[i - 1] = punto_medio(puntos[i] , puntos[i - 1])
        else:
            arr2[i - 1] = fin
    
    return arr2


def actualizar_feromonas(recorridos, longitudes, feromonas):
    feromonas *= (1.0 - RHO)
    for x in range(len(recorridos)):
        ciudad_actual = recorridos[x]
        delta_feromona = Q / (1 + longitudes[ciudad_actual])
        feromonas[ciudad_actual] += delta_feromona       

## bien
def seleccionar_proxima_ciudad(it,ciudad_actual,tam, visitadas, distancias, feromonas,puntos_medios):
    distancias = np.array(distancias)
    num_ciudades = distancias.shape[0]
    probabilidades = np.zeros(2)
    suma_probabilidades = 0.0   
    value = []
    maxpor = (1 if ciudad_actual == tam - 1 else 2)
    for j in range(maxpor):
        if ( distancias[ciudad_actual] != float('inf')): 
            s =(ciudad_actual-1 if j == 0 else ciudad_actual + 1)  if it != 0 else (((ciudad_actual + 1) if j == 0 else ciudad_actual) + (-1 if j == 0 else 1))
            value.append(s)
            probabilidades[j] = (feromonas[s] ** ALPHA) * ((1.0 / (1 + distancias[ s ]) ** BETA))
            suma_probabilidades += probabilidades[j]


    if suma_probabilidades == 0:
        return ciudad_actual  
   
    probabilidades_normalizadas = probabilidades / suma_probabilidades
    return value[np.argmax(probabilidades_normalizadas)]






def aco(distancias, puntos_medios,puntos_medios_vistos,puntos):
    distancias = np.array(distancias)
    num_ciudades = distancias.shape[0]
    feromonas = np.ones(num_ciudades)
    mejor_recorrido = None
    mejor_longitud = float('inf')
    recorridos_ante = []
    for iteracion in range(MAX_ITERACIONES):
        recorridos = []
        
        for k in range(NUM_HORMIGAS):
            recorrido = []
            ciudad_inicial = 0
            if iteracion == 0:
                ciudad_inicial =  random.randint(0, num_ciudades - 1)
            else :
                ciudad_inicial = recorridos_ante[k]
            
            ciudad_actual = ciudad_inicial  
            proxima_ciudad = seleccionar_proxima_ciudad(iteracion,ciudad_actual,num_ciudades ,recorrido, distancias, feromonas,puntos_medios)
            recorridos.append((ciudad_actual if ciudad_actual == proxima_ciudad else proxima_ciudad ))
            if distancias[proxima_ciudad]<mejor_longitud:
                 mejor_longitud = distancias[proxima_ciudad]
                 mejor_recorrido = puntos[proxima_ciudad]
        
        recorridos_ante = recorridos
        actualizar_feromonas(recorridos, distancias, feromonas)
        print(f"Iteración {iteracion + 1}: Mejor longitud de recorrido = {mejor_longitud}")
        print("Mejor recorrido encontrado:")
        print(mejor_recorrido)


if __name__ == "__main__":

    ini_inter = int(input("Ingrese el incio del intervalo: "))
    fin_inter = int(input("Ingrese el fin del intervalo: "))
    mapa = {}
    mapa2 = []

# Generar todos los pares posibles en el intervalo [-2, -2] a [2, 2]    
    for x in range(ini_inter, fin_inter + 1 ):
        for y in range(ini_inter, fin_inter + 1):
        # Usar tuplas como claves en el diccionario
            if (x, y) not in mapa and (y, x) not in mapa:
                mapa[(x, y)] = True
                mapa[(y, x)] = True
                mapa2.append((x, y))

    mapa3 = []
    mapa2 = sorted(mapa2, key=lambda x: f(x[0],x[1]))
    for x in range(1,len(mapa2)*2):
        mapa3.append( ((-1*mapa2[ len(mapa2) - x ][0],-1*mapa2[ len(mapa2) - x ][1] )  if x < len(mapa2)  else mapa2[x-len(mapa2)]) )

    evaluacion_f = [0] * len(mapa3)
    #print(len(mapa3))
    distancias = evaluador(mapa3) 
    print(distancias) 
    
    puntos_medios = generar_puntos_med(mapa3,mapa3[len(mapa3)-1] )
    #print(generar_puntos_med(mapa3,mapa3[len(mapa3)-1] )) 
    puntos_medios_vistos = np.full(len(mapa3), float('inf'))
    aco(distancias, puntos_medios,puntos_medios_vistos,mapa3)

