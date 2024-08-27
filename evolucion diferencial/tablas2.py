import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
mejor_valor = 2.75437;
data = pd.read_csv('rand7media.txt', sep=' ', header=None)

data = data.dropna(axis=1, how='all')

plt.figure(figsize=(10, 6))
box = plt.boxplot(data.values, tick_labels=[f'x{i+1}' for i in range(data.shape[1])], patch_artist=True)

for patch in box['boxes']:
    patch.set_facecolor('#ADD8E6')  # Color light blue en formato hexadecimal
    patch.set_edgecolor('black')
    patch.set_linewidth(1.5)

medians = [np.median(data.iloc[:, i]) for i in range(data.shape[1])]
for i, median in enumerate(medians):
    plt.text(i + 1, median, f'{median:.2f}', horizontalalignment='center', verticalalignment='center', fontsize=10, color='black')
plt.title(f'La media de la población en el mejor valor de: {mejor_valor:.2f}')

plt.ylabel('Valores')
plt.xlabel('Variables')
plt.grid(True) 
plt.show()



data = pd.read_csv('rand7mas_cerca.txt', sep=' ', header=None)
data = data.dropna(axis=1, how='all')

plt.figure(figsize=(10, 6))
box = plt.boxplot(data.values, tick_labels=[f'x{i+1}' for i in range(data.shape[1])], patch_artist=True)

for patch in box['boxes']:
    patch.set_facecolor('#ADD8E6')  
    patch.set_edgecolor('black')
    patch.set_linewidth(1.5)

medians = [np.median(data.iloc[:, i]) for i in range(data.shape[1])]
for i, median in enumerate(medians):
    plt.text(i + 1, median, f'{median:.2f}', horizontalalignment='center', verticalalignment='center', fontsize=10, color='black')

plt.title(f'El individuo más cerca de la media en el mejor valor de: {mejor_valor:.2f}')

plt.ylabel('Valores')
plt.xlabel('Variables')
plt.grid(True) 
plt.show()



data = pd.read_csv('rand7mas_lejano.txt', sep=' ', header=None)
data = data.dropna(axis=1, how='all')

plt.figure(figsize=(10, 6))
box = plt.boxplot(data.values, tick_labels=[f'x{i+1}' for i in range(data.shape[1])], patch_artist=True)

for patch in box['boxes']:
    patch.set_facecolor('#ADD8E6')  
    patch.set_edgecolor('black')
    patch.set_linewidth(1.5)

medians = [np.median(data.iloc[:, i]) for i in range(data.shape[1])]
for i, median in enumerate(medians):
    plt.text(i + 1, median, f'{median:.2f}', horizontalalignment='center', verticalalignment='center', fontsize=10, color='black')
plt.title(f'El individuo más lejos de la media  en el mejor valor de: {mejor_valor:.2f}')
plt.ylabel('Valores')
plt.xlabel('Variables')
plt.grid(True) 
plt.show()




