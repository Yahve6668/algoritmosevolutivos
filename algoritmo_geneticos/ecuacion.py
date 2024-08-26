import random
import itertools
from itertools import combinations

Tasa_Cruzamiento = 0.9
Tasa_Mutacion = 0.025
num_generaciones = 600
def generador_poblacion(ini, fin, t_p):
    unique_numbers_p = []
    for _ in range(10):
        unique_numbers = [random.choice(range(ini, fin + 1)) for _ in range(3)]
        unique_numbers_p.append(unique_numbers)
    print(unique_numbers_p)
    return unique_numbers_p

def fitnets(poblacion):
    unique_numbers_f = []
    for individuo in poblacion:
        x, y, z = individuo
        fitness = (
            (3*x + 8*y + 2*z - 25)**2 +
            (x - 2*y + 4*z - 12)**2 +
            (-5*x + 3*y + 11*z - 4)**2
        )
        unique_numbers_f.append(fitness)
    return unique_numbers_f

def seleccionar_mejores(poblacion, aptitudes):
    aptitud_individuo = list(zip(aptitudes, poblacion))
    aptitud_individuo.sort()
    
    mejores_individuos = [aptitud_individuo[0][1], aptitud_individuo[1][1]]

    #print("Mejores individuos seleccionados:", mejores_individuos)
    return mejores_individuos

def torneo(poblacion):
    ganadores = []
    num_pares = len(poblacion)    
    aptitudes = fitnets(poblacion)
    
    indices = range(len(poblacion))
    pares_posibles = list(combinations(indices, 2))
    
    pares_seleccionados = random.sample(pares_posibles, min(num_pares, len(pares_posibles)))
    
    for par in pares_seleccionados:
        i1, i2 = par
        if aptitudes[i1] < aptitudes[i2]:
            ganadores.append(poblacion[i1])
        else:
            ganadores.append(poblacion[i2])
    
    return ganadores

def cruza(x, y):
    #print("Antes del cruzamiento:", x, y)
    numero_aleatorio = random.choice([0, 1, 2])
    temp = x[numero_aleatorio]
    x[numero_aleatorio] = y[numero_aleatorio]
    y[numero_aleatorio] = temp
    #print("Después del cruzamiento:", x, y)
    return x, y

def ajustar_valor_circular(valor, min_val=-10, max_val=10):
    rango = max_val - min_val
    while valor > max_val or valor < min_val:
        if valor > max_val:
            valor -= rango
        elif valor < min_val:
            valor += rango
    return valor

def muta(x):
    numero_aleatorio = random.choice([0, 1, 2])
    arr = [3,0.5,2]
    nuevo_valor = x[numero_aleatorio] * 0.25 +  random.choice(range(0, 8))*.6
    x[numero_aleatorio] = ajustar_valor_circular(nuevo_valor)
    return x

m_b = [[20,20,20]]
def new_p(poblacion, amplitud,itera):
    arr_p = []
    global m_b  
    mejores = seleccionar_mejores(poblacion, amplitud)
    
    for x in range(len(mejores)):
        if fitnets(m_b)[0] > fitnets([mejores[ x ]])[0]:
            m_b = [mejores[ x ]]

        
    if itera == num_generaciones/2 :
        arr_p = generador_poblacion(-10, 10, 3)
        arr_p[0] = m_b[0]
        #print("--------------------------------------------------------------------------------------------------------------------------------------")
    else:
        arr_p.extend(mejores)
        mejores_set = set(map(tuple, mejores))  
        poblacion_filtrada = [individuo for individuo in poblacion if tuple(individuo) not in mejores_set]
        ganadores_torneo = torneo(poblacion_filtrada)
        arr_p.extend(ganadores_torneo)
    
    if len(arr_p) < 10:
        for x in range(10 - len(arr_p)):
                arr_p.extend([mejores[0]])   
    for x in range(0, 10, 2):      
        numero_aleatorio = random.random()
        if numero_aleatorio <= Tasa_Cruzamiento:
            hijo1, hijo2 = cruza(arr_p[x], arr_p[ x + 1 ])
            arr_p[ x ] = hijo1
            arr_p[ x + 1 ] = hijo2
        numero_aleatorio = random.random()
        if numero_aleatorio <= Tasa_Mutacion:
            arr_p[x] = muta(arr_p[x])
    print("Nueva población:", arr_p)
    return arr_p

if __name__ == "__main__":

    poblacion = generador_poblacion(-10, 10, 3)
    for x in range(num_generaciones):
        #print("lo mejor global es ",m_b)
        aptitudes = fitnets(poblacion)
        #print("Aptitudes:", aptitudes)
        mejores = seleccionar_mejores(poblacion, aptitudes)
        #print("Mejores individuos:", mejores)
        nueva_poblacion = new_p(poblacion, aptitudes,x)
        #print("Nueva población:", nueva_poblacion)
        poblacion=nueva_poblacion

    print(fitnets(m_b))
    print(m_b)