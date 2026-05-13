"""
Transición Small World
Validación estadística de L(p) y C(p) normalizados
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def calcularmetricas(n=100, k=4, valores_p=None, repeticiones=5):

    if valores_p is None:
        valores_p = np.logspace(-3, 0, 25)  

    L_valores = []
    C_valores = []
    print(f"  Calculando métricas para {len(valores_p)} valores de p "
          
          f"con {repeticiones} repeticiones cada uno")
    for p in valores_p:
        L_repeticiones = []
        C_repeticiones = []         
        for _ in range(repeticiones):
            G = nx.watts_strogatz_graph(n, k, p)
            if nx.is_connected(G): 
                L_repeticiones.append(nx.average_shortest_path_length(G))
            C_repeticiones.append(nx.average_clustering(G))
        L_valores.append(np.mean(L_repeticiones) if L_repeticiones else np.nan)
        C_valores.append(np.mean(C_repeticiones))
    L_array = np.array(L_valores, dtype=float)
    C_array = np.array(C_valores, dtype=float)

    # FIX: lógica de normalización estaba invertida
    L0 = np.nanmin(L_array) if np.isnan(L_array[0]) else L_array[0]
    C0 = C_array[0]

    L_normalizado = L_array / L0
    C_normalizado = C_array / C0
    return valores_p, L_normalizado, C_normalizado

def graficar_transicion(valores_p, L_normalizado, C_normalizado):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogx(valores_p, L_normalizado, 's-', color='red', linewidth=2, markersize=6, label="$L(p) / L(0)$  — Distancia promedio")
    ax.semilogx(valores_p, C_normalizado, 'o-', color='blue', linewidth=2, markersize=6, label="$C(p) / C(0)$  — Coeficiente de agrupamiento")

    ax.axvspan(0.001, 0.1, color='gray', alpha=0.08, label="zona Small World") 
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel("Probabilidad de reconexión (p)", fontsize=12) 
    ax.set_ylabel("Métricas normalizadas", fontsize=12)
    ax.set_title("Transición Small World: L(p) y C(p) normalizados del Modelo de Watts-Strogatz\n"
                 "C cae lentamente, L cae drasticamente", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10, loc="upper right")
    ax.set_ylim(0, 1.05)
    ax.grid(True, which="both", alpha=0.3)
    ax.set_xlim(valores_p[0], valores_p[-1])

    idx_critico = np.nanargmin(np.abs(L_normalizado - 0.5))
    p_critico = valores_p[idx_critico]
    ax.annotate(
        f"p crítico ≈ {p_critico:.3f}",
        xy=(p_critico * 5, 0.6), xytext=(p_critico * .5, 0.6),
        arrowprops=dict(arrowstyle="->", color="black"),
        fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="gray")
    )
    plt.tight_layout()
    plt.show()

def ejecutar():
    while True:
        print("\nTransición Small World L(p) y C(p) ")
        print("1. Grafica con parametros por defecto N=100, K=4")
        print("2. Configurar parametros")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            valores_p, L_normalizado, C_normalizado = calcularmetricas(n=100, k=4, repeticiones=5)
            graficar_transicion(valores_p, L_normalizado, C_normalizado)
        elif opcion == "2":
          
            print("configurar parámetros para la transición small world")
            try:
                n= int(input("  Número de nodos (N) si no coloca nada se toma 100: ") or "100")
                k= int(input("  Vecinos por nodo (k) si no coloca nada se toma 4: ") or "4")
                repeticiones= int(input("  Número de repeticiones si no coloca nada se toma 5: ") or "5")
            except ValueError:
                print("No valido")
                n, k, repeticiones = 100, 4, 5
            valores_p, L_normalizado, C_normalizado = calcularmetricas(n=n, k=k, repeticiones=repeticiones)
            graficar_transicion(valores_p, L_normalizado, C_normalizado)
        elif opcion == "0":
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")