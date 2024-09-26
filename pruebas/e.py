import random

def main():
    n = int(input())
    print(n)
    mat = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if j != i and mat[i][j] == 0:
                r = random.randint(0, 1000000)  
                print(r, end=" ")
                mat[i][j] = r
                mat[j][i] = r
            else:
                print(mat[j][i], end=" ")
        print()

    print(n // 5 + (1 if n % 5 != 0 else 0))

if __name__ == "__main__":
    main()
/*
import random
import sys
from typing import List, Tuple

v = []
globaleva = []

# Función objetivo
def funcion(s: List[int]) -> int:
    dism = 0
    for i in range(len(v)):
        dis = sys.maxsize
        for a in s:
            dis = min(dis, v[i][a])
        dism += dis
    return dism

# Combinación de resultados
def comsol(a: List[List[int]], n: int) -> List[List[int]]:
    for i in range(len(a)):
        for j in range(len(a[i]) // 2):
            a[i][j] = (a[i][j] + a[i][j + len(a[i]) // 2]) % n
    return a

# Reemplazamiento de soluciones
def remplaza(a: List[List[int]], b: List[int]):
    for i in range(len(a)):
        if funcion(a[i]) > funcion(b):
            a[i] = b
            break

# Generador de conjunto
def conjuntop(n: int, tam: int, espacio: int) -> List[List[int]]:
    conjunto = []
    for _ in range(n):
        per = [random.randint(0, espacio - 1) for _ in range(tam)]
        conjunto.append(per)
    return conjunto

# Mejoramiento del conjunto
def mejora_conjuntop(n: int, tam: int, conjunto: List[List[int]]) -> List[List[int]]:
    m = sys.maxsize
    eval_pr = []
    for a in conjunto:
        m = min(m, funcion(a))
        eval_pr.append(funcion(a))
    
    s = [(i, abs(m - eval_pr[i])) for i in range(len(eval_pr))]
    s.sort(key=lambda x: (x[1], x[0]))

    for i in range(len(s)):
        if s[i][1] <= s[len(s) // 2][1]:
            for j in range(len(conjunto[s[i][0]])):
                conjunto[s[i][0]][j] = (conjunto[s[i][0]][j] + 1) % n
        else:
            break
    return conjunto

# Generador del espacio de referencia
def b(conjunto: List[List[int]], tam: int) -> List[List[int]]:
    r = []
    evaludor = [(i, funcion(conjunto[i])) for i in range(len(conjunto))]
    global evaludor
    
    evaludor.sort(key=lambda x: (x[1], x[0]))

    for i in range(tam // 2):
        r.append(conjunto[evaludor[i][0]])
    
    for i in range(tam // 2):
        r.append(conjunto[random.randint(0, len(conjunto) - 1)])

    return r

iteraciones = 100

# Algoritmo principal
def solve(p: int, n: int):
    e = conjuntop(50, p, n)
    e = mejora_conjuntop(n, p, e)
    espacios = b(e, 10)

    for a in espacios:
        print("f", funcion(a), end=" ")
        print(" ".join(map(str, a)))

    m_dis_gl = sys.maxsize
    mejorCombinacion = []
    
    for _ in range(iteraciones):
        for c in e:
            remplaza(espacios, c)
        
        mejorCombinacion = espacios[0]
        m_dis_gl = funcion(espacios[0])
        
        # Combinación
        temp = comsol(espacios, n)
        for j in temp:
            remplaza(espacios, j)
        
        # Mejora de soluciones
        e = mejora_conjuntop(n, p, e)

    print("La mejor solución fue:")
    print(" ".join(map(str, mejorCombinacion)))
    print(f"Con un valor de distancia máxima de {m_dis_gl}. La distancia máxima fue {mejorCombinacion}.")

# Función principal
if __name__ == "__main__":
    n = int(input())
    for _ in range(n):
        arr = list(map(int, input().split()))
        v.append(arr)
    p = int(input())
    solve(p, n)

# Búsqueda dispersa
"""
1. Generación de diversificación
2. Mejoramiento
3. Actualización de conjunto de referencia
4. Generación de subconjuntos
5. Combinación de soluciones
"""


*/