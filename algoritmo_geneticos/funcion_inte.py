import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import math
from numpy.random import randint
from numpy.random import rand
import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import itertools
import math
import bisect
# PARAMETROS
limites = [[0, 15]]         # limites de la funcion
generaciones = 100          # numero de generaciones (iteraciones)
bits = 32                   # cantidad de bits
poblacion = 100             # tamano de poblacion
cruzamiento = 0.9           # tasa de cruzamiento 
k=2 
def f(x):
    r = abs((x[0] - 5) / (2 + math.sin(x[0])))
    return r  

rango_mutacion = 0.06

def decodificacion(limites, bits, cadena_bits):
    decodificado = list()
    largo = 2**bits
    for i in range(len(limites)):
        a = i * bits
        b = (i * bits)+bits
        subcadena = cadena_bits[a:b]
        caracteres = ''.join([str(s) for s in subcadena])
        integrado = int(caracteres, k)
        valor = limites[i][0] + (integrado/largo) * (limites[i][1] - limites[i][0])
        decodificado.append(valor)
    return decodificado

#torneo 

def selection(padres, mejores, k=k):
    seleccionados = randint(len(padres))
    for i in randint(0, len(padres), k-1):
        if mejores[i] < mejores[seleccionados]:
            seleccionados = i
    return padres[seleccionados]

def selection_ruleta(padres, mejores, k=k):
    amplitud = padres;
    arr = []
    suma = 0.0
    seleccionados =  [0] * poblacion
    for i in padres:
        valor_transformado = 1 / (1 + f(decodificacion(limites, bits, i) ))
        arr.append(valor_transformado)
        suma += valor_transformado
    
    probabilidad_acumulada = [x / suma for x in arr]
    print("la poblacion",poblacion)
    s = 0
    for x in range(poblacion):
        s += probabilidad_acumulada[x]
        probabilidad_acumulada[x] = s
        #print(s)
    #print(probabilidad_acumulada)  
    

    for x in range(poblacion):
        valor = random.random()
        pos = bisect.bisect_left(probabilidad_acumulada, valor)
        seleccionados[ x ] = pos
    #print(seleccionados)
    return [padres[i] for i in seleccionados] 

    

# Cruza 2 padres y crea 2 hijos
def crossover(P1, P2, cruzamiento):
    H1 = P1.copy()
    H2 = P2.copy()
    if rand() < cruzamiento:
        pt = randint(1, len(P1)-k)
        H1 = P1[:pt] + P2[pt:]
        H2 = P2[:pt] + P1[pt:]
    return [H1, H2]

def mutacion(cadena_bits, rango_mutacion):
    for i in range(len(cadena_bits)):
        if rand() < rango_mutacion:
            cadena_bits[i] = 1 - cadena_bits[i]

mejorglobal = 1000000.0 
def algoritmo_genetico(f, limites, bits, generaciones, poblacion, cruzamiento, rango_mutacion,op):
    padres = [randint(0, 2, bits*len(limites)).tolist() for _ in range(poblacion)]
    x = 0
    f_de_x = f(decodificacion(limites, bits, padres[0]))
    print(op)
    for gen in range(generaciones):
        decodificado = [decodificacion(limites, bits, p) for p in padres]
        mejores = [f(d) for d in decodificado]

        for i in range(poblacion):
            if mejores[i] < f_de_x:
                x, f_de_x = padres[i], mejores[i]
                global mejorglobal
                mejorglobal = mejores[i]
                print(">%d, new x f(%s) = %f" % (gen,  decodificado[i], mejores[i]))
        seleccionados = []
        if op == "Torneo":
            seleccionados = [selection(padres, mejores) for _ in range(poblacion)]
        else: 
            seleccionados =  selection_ruleta(padres, mejores)           
        hijos = list()
        for i in range(0, poblacion, 2):
            P1, P2 = seleccionados[i], seleccionados[i+1]
            for j in crossover(P1, P2, cruzamiento):
                mutacion(j, rango_mutacion)
                hijos.append(j)
        padres = hijos
    return [x, f_de_x]




            
class GeneticAlgorithmApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Configuración del Algoritmo Genético")
        self.geometry("600x600")

        self.lbl_individuals = tk.Label(self, text="Número de Individuos")
        self.lbl_individuals.pack(pady=5)
        self.ent_individuals = tk.Entry(self)
        self.ent_individuals.pack(pady=5)


        self.lbl_generations = tk.Label(self, text="Número de Generaciones")
        self.lbl_generations.pack(pady=5)
        self.ent_generations = tk.Entry(self)
        self.ent_generations.pack(pady=5)


        self.lbl_crossover = tk.Label(self, text="Probabilidad de Cruza")
        self.lbl_crossover.pack(pady=5)
        self.ent_crossover = tk.Entry(self)
        self.ent_crossover.pack(pady=5)


        self.lbl_mutation = tk.Label(self, text="Probabilidad de Mutación")
        self.lbl_mutation.pack(pady=5)
        self.ent_mutation = tk.Entry(self)
        self.ent_mutation.pack(pady=5)


        self.lbl_method = tk.Label(self, text="Seleccionar Método")
        self.lbl_method.pack(pady=5)
        self.method_var = tk.StringVar(value="torneo")
        self.rb_tournament = tk.Radiobutton(self, text="Torneo", variable=self.method_var, value="torneo")
        self.rb_tournament.pack(pady=5)
        self.rb_roulette = tk.Radiobutton(self, text="Ruleta", variable=self.method_var, value="ruleta")
        self.rb_roulette.pack(pady=5)


        self.btn_plot = tk.Button(self, text="Graficar Función", command=self.plot_function)
        self.btn_plot.pack(pady=20)


        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def plot_function(self):
        # Obtener valores de entrada
        try:
            individuals = int(self.ent_individuals.get())
            generations = int(self.ent_generations.get())
            crossover_prob = float(self.ent_crossover.get())
            mutation_prob = float(self.ent_mutation.get())
            method = self.method_var.get()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")
            return
        #algoritmo 
        global poblacion,generaciones,cruzamiento,rango_mutacion
        poblacion = individuals
        generaciones = generations
        cruzamiento = crossover_prob 
        rango_mutacion = mutation_prob

        x, aciertos = algoritmo_genetico(f, limites, bits, generaciones, poblacion, cruzamiento, rango_mutacion,method)

        decodificado = decodificacion(limites, bits, x)
        
        messagebox.showinfo("Información", f"Opción seleccionada: {method}\nRango: {0} a {15}\nMinimo de la funcion fue : {decodificado} con un valor de {mejorglobal} ")
        # grafica 
        # Borrar gráfica anterior
        self.ax.clear()

        x = np.linspace(-15, 15, 400)
        y = np.abs((x - 5) / (2 + np.sin(x)))

        min_y = np.min(y)
        min_x = x[np.argmin(y)]


        self.ax.plot(x, y, label='Función Ejemplo')
        self.ax.axhline(0, color='black',linewidth=0.5)
        self.ax.axvline(0, color='black',linewidth=0.5)
        self.ax.set_title(f'Gráfica de Función - Método: {method}\nMínimo: ({min_x:.2f}, {min_y:.2f})')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.legend()

        self.ax.set_ylim([-1.5, 1.5])

        self.canvas.draw()

if __name__ == "__main__":
    app = GeneticAlgorithmApp()
    app.mainloop()
