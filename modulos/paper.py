"""Aqui vamos a comparar las redes Regular vs Small-World vs Aleatoria
vamos a mostrar lo del articulo tablas, el modelo de propagacion y la comparacion visual de los tres tipos de red
 """
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import random

#tabla comparativa
def tabla(n=100, k=4, p=0.1):

    print("Tabla comparativa")

    G_sw=nx.watts_strogatz_graph(n,k,p)

    G_rand=nx.erdos_renyi_graph(n,(k*2)/n)
    if not nx.is_connected(G_sw):
        G_sw = G_sw.subgraph(max(nx.connected_components(G_sw), key=len)).copy()
    if not nx.is_connected(G_rand):
        G_rand = G_rand.subgraph(max(nx.connected_components(G_rand), key=len)).copy()
 
    L_sw   = nx.average_shortest_path_length(G_sw)
    C_sw   = nx.average_clustering(G_sw)
    L_rand = nx.average_shortest_path_length(G_rand)
    C_rand = nx.average_clustering(G_rand)
    print(f"  {'Red':<20} {'L (camino)':>12} {'C (clustering)':>15}")
    print(f"  {'Small-World':<20} {L_sw:>12.4f} {C_sw:>15.4f}")
    print(f"  {'Aleatoria':<20} {L_rand:>12.4f} {C_rand:>15.4f}")
    print(f"\n  ¿Es small-world? L_sw ≈ L_rand: {abs(L_sw - L_rand) < 2:.0f}  |  C_sw >> C_rand: {C_sw > C_rand * 2}")
    print(f"  Condición del paper: n({n}) >> k({k}) >> ln(n)({np.log(n):.1f}) >> 1")
    input("\n  Presiona Enter para continuar...")
#propagacion
def compararredes(n=50, k=4):
    print("Generando comparacion visual")
    redes={
        f"Regular(p=0)":       nx.watts_strogatz_graph(n, k, 0),
        f"Small-World(p=0.1)": nx.watts_strogatz_graph(n, k, 0.1),
        f"Aleatoria(p=1)":     nx.watts_strogatz_graph(n, k, 1.0),
    }
    fig, axes =plt.subplots(1,3, figsize=(16,6))
    fig.suptitle("Comparacion de la red regular vs small word vs aleatoria", fontsize=13, fontweight="bold")
    colores=["red", "blue", "yellow"]
    for ax, (titulo, G), color in zip(axes, redes.items(), colores):
        pos=nx.circular_layout(G)
        if not nx.is_connected(G):
            componentes=max(nx.connected_components(G), key=len)
            G=G.subgraph(componentes).copy()
        L=nx.average_shortest_path_length(G)
        C=nx.average_clustering(G)
        nx.draw_networkx(G, pos=pos, ax=ax, node_size=60, node_color=color,edge_color="blue", with_labels=False, width=0.5, alpha=0.9)
        ax.set_title(f"{titulo}\nL={L:.2f}  |  C={C:.2f}",
                     fontsize=11, fontweight="bold")
        ax.axis("off")
 
    plt.tight_layout()
    plt.show()

def ejecutar():
    while True:
        print("Comparacion de las redes ")
        print("1. Tabla comparativa L y C ")
        print("2. Comparación visual: Regular vs Small-World vs Aleatoria")
        print("0. Volver al menu principal")
        opcion = input("Seleccione una opción: ")

        if opcion=="1":
            try:
                n = int(input("  Número de nodos (N) si no coloca nada se toma 100: ") or "100") 
                k = int(input("  Vecinos por nodo (k) si no coloca nada se toma 4: ") or "4")
                p = float(input("  Probabilidad de reconexión (p) si no coloca nada se toma 0.1: ") or "0.1")

            except ValueError:
                n, k, p = 100, 4, 0.1
            
            tabla(n,k,p)
        elif opcion=="2":
            try:
                n = int(input("  Número de nodos (N) si no coloca nada se toma 100: ") or "100") 
                k = int(input("  Vecinos por nodo (k) si no coloca nada se toma 4: ") or "4")
            except ValueError:
                    n, k = 50, 4
            compararredes(n,k)
        elif opcion=="0":
            break
        else:
            print("opcion no valida")
                

            






