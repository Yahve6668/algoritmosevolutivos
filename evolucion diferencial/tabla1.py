import matplotlib.pyplot as plt
import numpy as np


def leer_datos(archivo):
    datos = []
    with open(archivo, 'r') as f:
        for linea in f:
            valores = list(map(float, linea.split()))
            datos.append(valores)
    return np.array(datos)

archivo = 'bestFCV.txt'  
datos = leer_datos(archivo)

data = datos.T.tolist()

plt.figure(figsize=(10, 6))
boxplot = plt.boxplot(data, patch_artist=True)

# Añadir el menor valor de cada generación como etiqueta
for i in range(len(data)):
    plt.text(i + 1, min(data[i]) - 1, f'Min: {min(data[i]):.2f}', 
             horizontalalignment='center', fontsize=10, color='blue')

plt.title('Evolución del Mejor Valor en Cada Generación')
plt.xlabel('Generación')
plt.ylabel('Mejor Valor')
plt.grid(True)
plt.show()
