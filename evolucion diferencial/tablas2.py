import matplotlib.pyplot as plt
import numpy as np
import csv


for iter in range(0, 10):
    medias = []
    cercanos = []
    lejanos = []
    mejor_global = 13.8968
    cadena = "randFCV" + str(iter) + ".txt"
    with open(cadena, 'r') as file:
        reader = csv.reader(file, delimiter=' ')
        for row in reader:
            # Convertir las filas en números flotantes y agregar a las listas correspondientes
            if len(row) == 3:
                medias.append(float(row[0]))
                cercanos.append(float(row[1]))
                lejanos.append(float(row[2]))
            elif len(row) == 1:
               mejor_global = float(row[0])


    generaciones = range(1, 11)

    fig, ax = plt.subplots(figsize=(14, 8))

    data = [medias, cercanos, lejanos]
    bp = ax.boxplot(data, positions=[1, 2, 3], widths=0.6, patch_artist=True)

    colors = ['lightblue', 'lightgreen', 'pink']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    for i, d in enumerate(data):
        y = d
        x = [i+1] * len(y)
        ax.plot(x, y, 'ro', alpha=0.5, markersize=5)

    ax.axhline(y=mejor_global, color='r', linestyle='--', label=f'Mejor global: {mejor_global}')

    ax.set_xlabel('Métricas', fontsize=12)
    ax.set_ylabel('Valor', fontsize=12)
    ax.set_title('Distribución de las métricas a lo largo de 10 generaciones', fontsize=14)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Media de la población', 'Individuo más cercano\na la media', 'Individuo más lejano\nde la media'], fontsize=10)

    ax.set_ylim(0, max(max(medias), max(cercanos), max(lejanos)) * 1.1)

    ax.legend([bp["boxes"][0], bp["boxes"][1], bp["boxes"][2], ax.get_lines()[-1]], 
              ['Media de la población', 'Individuo más cercano a la media', 'Individuo más lejano de la media', f'Mejor global: {mejor_global}'],
              fontsize=10)

    # Añadir etiquetas para el mejor valor y Q2 de cada caja
    for i, d in enumerate(data):
        mejor = min(d)
        q2 = np.median(d)
        ax.text(i+1, mejor, f'Mejor: {mejor:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=8)
        ax.text(i+1, q2, f'Q2: {q2:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()