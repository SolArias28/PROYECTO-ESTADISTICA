"""
Transición Small World
Validación estadística de L(p) y C(p) normalizados basados en Watts & Strogatz
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def calcularmetricas(n=100, k=4, valores_p=None, repeticiones=5):
    if valores_p is None:
        # FIX: 25 estaba fuera del paréntesis
        valores_p = np.concatenate([[0], np.logspace(-3, 0, 25)])

    L_valores, L_espacios = [], []
    C_valores, C_espacios = [], []

    print(f"  Calculando métricas para {len(valores_p)} valores de p "
          f"con {repeticiones} repeticiones cada uno")

    for p in valores_p:
        L_repeticiones = []
        C_repeticiones = []
        for _ in range(repeticiones):
            # FIX: semilla ahora se pasa a watts_strogatz_graph
            semilla = int(np.random.randint(0, 2**31))
            G = nx.watts_strogatz_graph(n, k, p, seed=semilla)
            if nx.is_connected(G):
                L_repeticiones.append(nx.average_shortest_path_length(G))
            C_repeticiones.append(nx.average_clustering(G))

        L_valores.append(np.mean(L_repeticiones) if L_repeticiones else np.nan)
        C_valores.append(np.mean(C_repeticiones))
        L_espacios.append(np.std(L_repeticiones) if L_repeticiones else np.nan)
        C_espacios.append(np.std(C_repeticiones))

    L_array      = np.array(L_valores,  dtype=float)
    C_array      = np.array(C_valores,  dtype=float)
    L_desviacion = np.array(L_espacios, dtype=float)
    C_desviacion = np.array(C_espacios, dtype=float)

    L0 = np.nanmin(L_array) if np.isnan(L_array[0]) else L_array[0]
    C0 = C_array[0]

    L_normalizado = L_array / L0
    C_normalizado = C_array / C0

    # FIX: retorna arrays completos para que graficar_bandas pueda indexarlos
    return valores_p, L_normalizado, C_normalizado, L_array, C_array, L_desviacion, C_desviacion

def graficar_transicion(valores_p, L_normalizado, C_normalizado):
    # FIX: filtrar p=0 para escala logarítmica
    mascarilla = valores_p > 0
    p_tramo    = valores_p[mascarilla]
    L_tramo    = L_normalizado[mascarilla]
    C_tramo    = C_normalizado[mascarilla]

    fig, ax = plt.subplots(figsize=(10, 6))
    # FIX: usar p_tramo, L_tramo, C_tramo en vez de valores_p completos
    ax.semilogx(p_tramo, L_tramo, 's-', color='red',  linewidth=2, markersize=6,
                label="$L(p) / L(0)$  — Distancia promedio")
    ax.semilogx(p_tramo, C_tramo, 'o-', color='blue', linewidth=2, markersize=6,
                label="$C(p) / C(0)$  — Coeficiente de agrupamiento")

    ax.axvspan(0.001, 0.1, color='gray', alpha=0.08, label="zona Small World")
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel("Probabilidad de reconexión (p)", fontsize=12)
    ax.set_ylabel("Métricas normalizadas", fontsize=12)
    ax.set_title("Transición Small World: L(p) y C(p) normalizados del Modelo de Watts-Strogatz\n"
                 "C cae lentamente, L cae drásticamente", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10, loc="upper right")
    ax.set_ylim(0, 1.05)
    ax.grid(True, which="both", alpha=0.3)
    ax.set_xlim(p_tramo[0], p_tramo[-1])

    idx_critico = np.nanargmin(np.abs(L_tramo - 0.5))
    p_critico   = p_tramo[idx_critico]
    ax.annotate(
        f"p crítico ≈ {p_critico:.3f}",
        xy=(p_critico * 5, 0.6), xytext=(p_critico * 0.5, 0.6),
        arrowprops=dict(arrowstyle="->", color="black"),
        fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="gray")
    )
    plt.tight_layout()
    plt.show()

def graficar_bandas(valores_p, L_array, C_array, L_desviacion, C_desviacion):
    mascara = valores_p > 0
    p_tramo = valores_p[mascara]
    L_tramo = L_array[mascara]
    C_tramo = C_array[mascara]
    ls      = L_desviacion[mascara]
    cs      = C_desviacion[mascara]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Variabilidad estadística de L(p) y C(p)\nBanda ±1 desviación estándar",
                 fontsize=13, fontweight="bold")

    ax1 = axes[0]
    ax1.semilogx(p_tramo, L_tramo, 's-', color='red', linewidth=2, markersize=6,
                 label="L(p) promedio")
    ax1.fill_between(p_tramo, L_tramo - ls, L_tramo + ls, color='red', alpha=0.2, label="±1σ")
    ax1.axhline(6, ls='--', color='darkred', lw=1.5, label="6 grados de separación")
    ax1.set_xlabel("p", fontsize=12)
    ax1.set_ylabel("Distancia promedio L", fontsize=12)
    ax1.set_title("L(p) — Distancia media", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=10)
    ax1.grid(True, which="both", alpha=0.3)

    ax2 = axes[1]
    ax2.semilogx(p_tramo, C_tramo, 'o-', color='blue', linewidth=2, markersize=6,
                 label="C(p) promedio")
    ax2.fill_between(p_tramo, C_tramo - cs, C_tramo + cs, color='blue', alpha=0.2, label="±1σ")
    ax2.set_xlabel("p", fontsize=12)
    ax2.set_ylabel("Clustering C", fontsize=12)
    ax2.set_title("C(p) — Coeficiente de clustering", fontsize=12, fontweight="bold")
    ax2.legend(fontsize=10)
    ax2.grid(True, which="both", alpha=0.3)

    plt.tight_layout()
    plt.show()

def ejecutar():
    while True:
        print("\nTransición Small World L(p) y C(p)")
        print("1. Grafica con parametros por defecto N=100, K=4")
        print("2. Configurar parametros")
        print("3. Gráfica con bandas ±σ")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            resultados = calcularmetricas(n=100, k=4, repeticiones=5)
            graficar_transicion(resultados[0], resultados[1], resultados[2])

        elif opcion == "2":
            print("Configurar parámetros para la transición small world")
            try:
                n = int(input("  Número de nodos (N) si no coloca nada se toma 100: ") or "100")
                k = int(input("  Vecinos por nodo (k) si no coloca nada se toma 4: ") or "4")
                repeticiones = int(input("  Número de repeticiones si no coloca nada se toma 5: ") or "5")
            except ValueError:
                print("No válido, se usarán valores por defecto")
                n, k, repeticiones = 100, 4, 5
            resultados = calcularmetricas(n=n, k=k, repeticiones=repeticiones)
            graficar_transicion(resultados[0], resultados[1], resultados[2])

        elif opcion == "3":
            print("Gráfica con bandas de desviación estándar")
            try:
                n = int(input("  Número de nodos (N) si no coloca nada se toma 100: ") or "100")
                k = int(input("  Vecinos por nodo (k) si no coloca nada se toma 4: ") or "4")
                repeticiones = int(input("  Número de repeticiones si no coloca nada se toma 10: ") or "10")
            except ValueError:
                print("No válido, se usarán valores por defecto")
                n, k, repeticiones = 100, 4, 10
            # FIX: fuera del except para ejecutarse siempre
            resultados = calcularmetricas(n=n, k=k, repeticiones=repeticiones)
            graficar_bandas(resultados[0], resultados[3], resultados[4],
                            resultados[5], resultados[6])

        elif opcion == "0": 
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")