import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import copy

def generarred(n=100, k=4, p=0.1):
    G = nx.watts_strogatz_graph(n, k, p)
    return G
def mayorcomponente(G):
    if G.number_of_nodes() == 0:
        return 0.0
    componentes = list(nx.connected_components(G))
    return max(len(c) for c in componentes) / G.number_of_nodes()
def calcularrobustez(G, estrategia="grado", repeticiones=5):
    G_copia = copy.deepcopy(G)
    nodostotales = G_copia.number_of_nodes()
    eliminada=[0]
    mayorcomp=[mayorcomponente(G_copia)]

    nodoorden= []

    if estrategia == "grado":
        nodoorden = sorted(G_copia.degree, key=lambda x: x[1], reverse=True) 
        nodoorden = [n for n, d in nodoorden]

    elif estrategia == "aleatoria":
        import random
        nodoorden = list(G_copia.nodes())
        random.shuffle(nodoorden)
    elif estrategia == "betweenness":        
        centrality = nx.betweenness_centrality(G_copia)
        nodoorden = sorted(centrality, key=centrality.get, reverse=True)

    for i, nodo in enumerate(nodoorden):
        G_copia.remove_node(nodo)
        eliminada.append((i + 1) / nodostotales)
        mayorcomp.append(mayorcomponente(G_copia))
    return np.array(eliminada), np.array(mayorcomp)

def graficarrobustez(G):
    print("\nCalculando curvas de robustez para eliminación por grado y aleatoria...")
    fig,axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Análisis de Robustez — Analogía con Asteroides (Asphaug)\n", fontsize=14, fontweight="bold", y=1.02)

    estilos={
        "grado": ("red", "Ataque dirigido por grado", "s-"),
        "betweenness": ("blue", "Ataque por betweenness", "--"),
        "aleatoria": ("green", "Ataque aleatorio", ":")
    }
    ax1=axes[0]
    for estrategia, (color, label, ls) in estilos.items():
        fx,comp=calcularrobustez(G, estrategia)
        ax1.plot(fx, comp, ls, color=color, label=label, linewidth=2)
    ax1.set_xlabel("Fracción de nodos eliminados", fontsize=12)
    ax1.set_ylabel("Tamaño relativo del mayor componente conectado", fontsize=12)
    ax1.set_title("Curvas de Robustez\n", fontsize=14, fontweight="bold")
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1.05)
    ax2=axes[1]
    G_copia= copy.deepcopy(G)
    nodooreden= sorted(G_copia.degree, key=lambda x: x[1], reverse=True)
    nodoorden= [n for n, d in nodooreden]
    eliminar=int(len(nodoorden)*0.2)
    eliminados= nodoorden[:eliminar]
    for nodo in nodoorden[:eliminar]:
        if nodo in G_copia:
            G_copia.remove_node(nodo)
    pos=nx.spring_layout(G_copia, seed=42)
    poscopia= {n: pos[n] for n in G_copia.nodes() if n in pos}
    colores= ["blue" for _ in G_copia.nodes()]
    componentes= list(nx.connected_components(G_copia))
    palleta=plt.cm.Set2(np.linspace(0, 1, len(componentes)))
    colorsnodes={}
    for i, comp in enumerate(componentes):
        for nodo in comp:
            colorsnodes[nodo]= palleta[i%len(palleta)]
    coloresfinales=[colorsnodes.get(n, "blue") for n in G_copia.nodes()]

    nx.draw_networkx(
        G_copia, pos=poscopia,ax=ax2, node_color=coloresfinales, edge_color="#AAAAAA", with_labels=False, node_size=100, alpha=0.9,width=0.6)

    ax2.set_title(f"Red después de eliminar el 20% de nodos por grado\n" 
                  f"({len(componentes)} componentes — {eliminar} nodos removidos)", fontsize=14, fontweight="bold")
    ax2.axis("off")
    plt.tight_layout()
    plt.show()
def analogia():
    texto = "Esta analogía explica que la resistencia de una red social es idéntica a la de un asteroide: ambos no son bloques sólidos, sino estructuras compuestas por fragmentos (nodos) y conexiones (canales de energía). Así como un asteroide poroso sobrevive mejor a un impacto nuclear porque absorbe la energía localmente en lugar de romperse, una red social es más resiliente si su estructura es uniforme; por el contrario, si la red depende de unos pocos puntos críticos, un ataque dirigido puede desintegrarla en múltiples pedazos, demostrando que la diversidad estructural es la clave para la supervivencia de cualquier sistema complejo."
    print(texto)
    input("\nPresiona Enter para continuar")
def ejecutar():
    G =generarred()
    print(f"Red cargada: {G.number_of_nodes()}nodos,{G.number_of_edges()}aristas ")

    while True:
        print("Analogia Asteroides & Robustez")
        print("1. Leer analogia cientifica( Asphaug)")
        print("2. Gaficar analisis de robustez")
        print("3. Regenerar red con nuevos parametros")
        print("0. Volver al menu principal")
        opcion = input("  Selecciona una opción: ")
        if opcion=="1":
            analogia()
        elif opcion=="2":
            graficarrobustez(G)
        elif opcion=="3":
            try:
                n = int(input("  Número de nodos si no coloca nada se toma 80: ") or "80")
                k = int(input("  Vecinos por nodo si no coloca nada se toma 4: ") or "4")
                p = float(input("  Probabilidad de reconexión  si no coloca nada se toma 0.15: ") or "0.15")
            except ValueError:
                print("  Entrada no válida se usara los anterirores")
                n, k, p = 80, 4, 0.15
            G= generarred(n,k,p)
            print(f"Nueva red: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")      
            
        elif opcion=="0":
            break
        else:
            print("opcion no valida")


