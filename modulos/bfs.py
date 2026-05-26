"""Aqui buscamos el camino más corto entre dos nodos en una red small world utilizando el algoritmo de búsqueda en anchura (BFS) y pues se muestra"""
import networkx as nx
import matplotlib.pyplot as plt 
import numpy as np
#creamos un diccionario para almacenar el estado de la red y las posiciones de los nodos para evitar recalcularlos cada vez que se ejecuta el algoritmo

_estado={"G": None, "posicion": None, "nombres": None}
def _nombresnodos(n):
    #Generamos una lista de nombres para los nodos de la redes
    nombre_gente=["Ivanna", "Juliana", "Majo", "Sol", "Andres", "Gabriela", "Luna", "Sofia",
        "Santiago", "Joshua", "Martin", "Julio", "Luisa", "Yarilis", "Sara", "Esteban",
        "Angie", "Angela", "David", "Jaime", "Elias", "Alejandro", "Maria", "Camilo",
        "Raul", "Dany", "Shiloh", "Cesar", "Mario", "Diego",
    ]
    if n <= len(nombre_gente):
        return{i: nombre_gente[i] for i in range(n)} #si el número de nodos es menor o igual a la cantidad de nombres disponibles, asignamos un nombre único a cada nodo
    else:
        return {i: f"Persona {i}" for i in range(n)} #si el número de nodos es mayor, asignamos nombres genéricos
    
def crearred(n=30, k=4, p=0.15):

    #creamos una red small world utilizando el modelo de Watts-Strogatz y almacenamos su estado en un diccionario global

    """
    n : nodos en la red
    k :  vecinos más cercanos a los que cada nodo está conectado
    p : probabilidad de rewireo de las conexiones"""
    

    G = nx.watts_strogatz_graph(n, k, p) # modelo de Watts-Strogatz

    posicion = nx.spring_layout(G, seed=42, k=0.5) #posiciones de los nodos para visualización

    nombres = _nombresnodos(n) 

    _estado["G"] = G #almacenamos la red en el diccionario global
    _estado["posicion"] = posicion  
    _estado["nombres"] = nombres 
def dibujaered(G, posicion, nombres,camino=None, titulo="Red Social de Sol y Andres"):
    fig, ax = plt.subplots(figsize=(11, 8))
    etiquetas = {n: nombres.get(n, str(n)) for n in G.nodes()}
    colores=[]
    for nodo in G.nodes():

        if camino and nodo == camino[0]:

            colores.append("red") #origen

        elif camino and nodo == camino[-1] :

            colores.append("#F2770C") #destino
        elif camino and nodo in camino:
    
            colores.append("yellow") #ruta intermedia

        else:
            colores.append("blue") #normalitos

    tamaños=[
        300 if (camino and nodo in camino) else 150
        for nodo in G.nodes()
    ]
    #aristas

    aristas=set()
    if camino:
        aristas=set(zip(camino, camino[1:])) 
    coloresaristas=[]    
    ancho=[]    
    for u, v in G.edges():
        if (u, v) in aristas or (v, u) in aristas:
            coloresaristas.append("red") #arista en el camino
            ancho.append(3.5)
        else:
            coloresaristas.append("#AAAAAA") #arista normal
            ancho.append(0.8)
    nx.draw_networkx_edges(G, pos=posicion, ax=ax, edge_color=coloresaristas, width=ancho, alpha=0.8)
    nx.draw_networkx_nodes(G, pos=posicion, ax=ax, node_color=colores, node_size=tamaños, alpha=0.9)
    nx.draw_networkx_labels(G, pos=posicion, ax=ax, labels=etiquetas, font_size=7, font_weight="bold")

    if camino:
        ruta_str = " → ".join(nombres.get(n, str(n)) for n in camino)
        saltos=len(camino) - 1
        ax.set_title(
            f"{titulo}\n Camino más corto: {ruta_str}\n({saltos} salto{'s' if saltos != 1 else ''})",
            fontsize=11, fontweight="bold", color="darkblue")
    else:
        ax.set_title(titulo, fontsize=11, fontweight="bold")
    from matplotlib.patches import Patch

    leyenda=[
        Patch(color="red", label="Origen/ ruta"),
        Patch(color="#F2770C", label="Destino"),
        Patch(color="yellow", label="Ruta Intermedia"),
        Patch(color="blue", label="Nodo normal"),
    ]
    ax.legend(handles=leyenda, loc="upper left", fontsize=9)
    ax.axis("off")
    plt.tight_layout()
    plt.show()

def listarnodos():
    G = _estado["G"]
    if G is None:
        print("La red no ha sido creada aún")
        return
    nombres = _estado["nombres"]
    print("\nNodos en la red:")
    nodos=sorted(G.nodes())
    colas=5
    filas=[nodos[i:i+colas] for i in range(0, len(nodos), colas)]
    for fila in filas:

        print("  ".join(f"{n:>3}: {nombres.get(n, str(n))}" for n in fila))
#buscar el camino más corto entre dos nodos utilizando BFS y mostrarlo en la red


def buscar():
    G = _estado["G"]
    posicion = _estado["posicion"]
    nombres = _estado["nombres"]
    if G is None:
       crearred()
       G, posicion, nombres = _estado["G"], _estado["posicion"], _estado["nombres"]
    listarnodos()
    print()
    try:
        origen = int(input("Ingrese el número del nodo de origen: "))
        destino = int(input("Ingrese el número del nodo de destino: "))
    except ValueError:
        print("ingrese números de nodo válidos.")
        return
    if origen not in G.nodes() or destino not in G.nodes():
        print("Nodo de origen o destino no válido.")
        return
    if origen == destino:
        print("El nodo de origen y destino son el mismo.")
        return
    if not nx.has_path(G, origen, destino):
        print("No hay camino entre el nodo de origen y destino.")
        return
    camino = nx.shortest_path(G, source=origen, target=destino)
    rutanombre = " → ".join(nombres.get(n, str(n)) for n in camino)
    print(f"Camino más corto encontrado: {rutanombre}")
    print(f"saltos: {len(camino) - 1}")

    dibujaered(G, posicion, nombres, camino=camino, titulo="Buscador de caminos BFS")
def ejecutar():
    crearred() #creamos la red 
    while True:
        print("\nBuscador de caminos BFS en Red Small World")
        print("1. Buscar camino entre dos nodos")
        print("2. Regenerar la red small world")
        print("3. Ver red actual sin caminos")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            buscar() #función de búsqueda
        elif opcion == "2":
           try:
                n = int(input("  Número de nodos si no coloca nada se toma 30: ") or "30")
                k = int(input("  Vecinos por nodo si no coloca nada se toma 4: ") or "4")
                p = float(input("  Probabilidad de reconexión  si no coloca nada se toma 0.15: ") or "0.15")
           except ValueError:
                print("  Entrada no válida, se usarán los anteriores")
                n, k, p = 30, 4, 0.15
           crearred(n, k, p)
           print(f"Nueva red creada con N={n}, K={k}, p={p}")
           G, posicion, nombres = _estado["G"], _estado["posicion"], _estado["nombres"]
           dibujaered(G, posicion, nombres, titulo="Red Small World Actual") #sin caminos

        elif opcion == "0":
            break
        else:
            print("Opción no válida")


   

