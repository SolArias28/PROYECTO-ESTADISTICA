"En esta parte degenero y visualizo la red small world"
"modelo de Watts-Strogatz"
import networkx as nx #Importamos la librería de grafos
import matplotlib.pyplot as plt #vizualización
import numpy as np 
import matplotlib.gridspec as gridspec #para organizar la visualización


def generarred(n=50, k=4, p=0.1):
    """red small world utilizando el modelo de Watts-Strogatz

        n : número de nodos en la red
        k : número de vecinos más cercanos a los que cada nodo está conectado
        p : probabilidad de rewireo de las conexiones"""
    G = nx.watts_strogatz_graph(n, k, p)
    return G    

#aqui dibujo la red en un eje matplolib dado
def visualizarred(G, titulo=" Red small world", p=None, ax=None):
    standole =ax is None
    if standole:
        fig, ax = plt.subplots(figsize=(7, 7)) #creamos una figura y un eje para dibujar la red
    pos =nx.circular_layout(G) #posiciones de los nodos en un layout circular
    nx.draw_networkx(
        G, 
        pos=pos,
        ax=ax,
        node_size=80,
         node_color="#A94AD9",
        edge_color="#AAAAAA",
        with_labels=False,
        width=0.6,
        alpha=0.9,
    )
    label= titulo if p is None else f"{titulo} (p={p})"
    ax.set_title(label, fontsize=12, fontweight="bold", pad=10) 
    ax.axis("off")
    if standole:
        plt.tight_layout() #ajustamos el diseño para que no se solapen los elementos
    
        plt.show()


# muestra la evolución de la red small world a medida que se aumenta la probabilidad 
def mostrarevolucion():
    print("\n Se esta generando la evolución de la red para distintos valores de p")
    valores_p = [0, 0.01,0.05,0.1,0.3,1.0] #valores de p para mostrar la evolución
    n, k = 50, 4 #número de nodos y vecinos
    fig= plt.figure(figsize=(18,10))
    fig.suptitle("Evolución de la red de Watts-Strogatz\n" 
             "De red regular (p=0) a red aleatoria (p=1)", 
             fontsize=14, 
             fontweight="bold", 
             y=1.01)
    gs = gridspec.GridSpec(2, 3, figure=fig , hspace=0.4, wspace=0.3) #creamos una cuadrícula de 2 filas y 3 columnas para organizar las subplots
    for i, p in enumerate(valores_p):
        G = generarred(n, k, p)
        ax = fig.add_subplot(gs[i])
        visualizarred(G, titulo="Watts-Strogatz", p=p, ax=ax)
    plt.tight_layout()
    plt.show()
    print("Visualización completa\n")        
#aqui sse pueden configurar los parametros y ver una sola red
def configurar():
    print("Configurar la red small world")
    try:
        n = int(input("  Número de nodos (N) si no coloca nada se toma 50: ") or "50") #
        k = int(input("  Vecinos por nodo (k) si no coloca nada se toma 4: ") or "4")
        p = float(input("  Probabilidad de reconexión (p) si no coloca nada se toma 0.1: ") or "0.1")
    except ValueError:
        print("  Entrada no válida, se usarán los valores por defecto (N=50, k=4, p=0.1)")
        n, k, p = 50, 4, 0.1
    G = generarred(n, k, p) #generamos la red con los parámetros configurados
    print(f"Distancia promedio L: {nx.average_shortest_path_length(G)}")
    print(f"Coeficiente de agrupamiento C: {nx.average_clustering(G)}")

    visualizarred(G, titulo="Red small world configurada", p=p) #visualizamos
def ejecutar():
     while True:
         
         print("\nRed Small World")
         print("1. Ver evolución de la red")
         print("2. Configurar y visualizar una red  ")
         print("0. Volver al menú principal")
         opcion = input("  Selecciona una opción: ")
         if opcion == "1":
             mostrarevolucion()
         elif opcion == "2":
                configurar()
         elif opcion == "0":
                print("Volviendo al menú principal")
                break
         else:
                print("Opción no válida, por favor selecciona una opción del menú.")
