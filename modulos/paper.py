"""
Dashboard — Resumen estadístico completo
Simulación Watts-Strogatz (1998) — Seis Grados de Separación
"""
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def calcularmetricas(n=100, k=4, valores_p=None, repeticiones=10):
    if valores_p is None:
        valores_p = np.concatenate([[0], np.logspace(-3, 0, 25)])

    L_medias, L_stds = [], []
    C_medias, C_stds = [], []

    print(f"  Calculando métricas para {len(valores_p)} valores de p "
          f"con {repeticiones} repeticiones cada uno...")

    for p in valores_p:
        L_repeticiones = []
        C_repeticiones = []
        for _ in range(repeticiones):
            seed = int(np.random.randint(0, 2**31))
            G = nx.watts_strogatz_graph(n, k, p, seed=seed)
            if nx.is_connected(G):
                L_repeticiones.append(nx.average_shortest_path_length(G))
            C_repeticiones.append(nx.average_clustering(G))

        L_medias.append(np.mean(L_repeticiones) if L_repeticiones else np.nan)
        L_stds.append(np.std(L_repeticiones)    if L_repeticiones else np.nan)
        C_medias.append(np.mean(C_repeticiones))
        C_stds.append(np.std(C_repeticiones))

    L_array = np.array(L_medias, dtype=float)
    C_array = np.array(C_medias, dtype=float)
    L_std   = np.array(L_stds,   dtype=float)
    C_std   = np.array(C_stds,   dtype=float)

    L0 = np.nanmin(L_array) if np.isnan(L_array[0]) else L_array[0]
    C0 = C_array[0]

    L_normalizado = L_array / L0
    C_normalizado = C_array / C0

    return valores_p, L_normalizado, C_normalizado, L_array, C_array, L_std, C_std


def graficar_dashboard(valores_p, L_normalizado, C_normalizado,
                       L_array, C_array, L_std, C_std):
    mask   = valores_p > 0
    p_plot = valores_p[mask]

    fig = plt.figure(figsize=(14, 9))
    gs  = gridspec.GridSpec(2, 2, hspace=0.4, wspace=0.35)
    fig.suptitle("Dashboard — Simulación Watts-Strogatz (1998)\nSeis Grados de Separación",
                 fontsize=14, fontweight="bold", y=1.01)

    # Arriba-izquierda: normalizada (réplica del paper)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.semilogx(p_plot, L_normalizado[mask], 'o-', color='#2563EB', lw=2, ms=5,
                 label=r"$L/L_0$")
    ax1.semilogx(p_plot, C_normalizado[mask], 's-', color='#DC2626', lw=2, ms=5,
                 label=r"$C/C_0$")
    ax1.set_ylim(-0.05, 1.1)
    ax1.set_title("Normalizado (réplica Fig. 2 W&S 1998)", fontsize=10, fontweight="bold")
    ax1.set_xlabel("p"); ax1.set_ylabel("Valor normalizado")
    ax1.legend(fontsize=9); ax1.grid(True, which="both", alpha=0.3)

    # Arriba-derecha: L absoluta con banda ±σ
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.semilogx(p_plot, L_array[mask], 'o-', color='#2563EB', lw=2, ms=5)
    ax2.fill_between(p_plot, L_array[mask] - L_std[mask],
                              L_array[mask] + L_std[mask], alpha=0.2, color='#2563EB',
                              label="±1σ")
    ax2.axhline(6, ls='--', color='red', lw=1.5, label="6 grados")
    ax2.set_title("Distancia promedio L(p)", fontsize=10, fontweight="bold")
    ax2.set_xlabel("p"); ax2.set_ylabel("L")
    ax2.legend(fontsize=9); ax2.grid(True, which="both", alpha=0.3)

    # Abajo-izquierda: C absoluta con banda ±σ
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.semilogx(p_plot, C_array[mask], 's-', color='#DC2626', lw=2, ms=5)
    ax3.fill_between(p_plot, C_array[mask] - C_std[mask],
                              C_array[mask] + C_std[mask], alpha=0.2, color='#DC2626',
                              label="±1σ")
    ax3.set_title("Clustering C(p)", fontsize=10, fontweight="bold")
    ax3.set_xlabel("p"); ax3.set_ylabel("C")
    ax3.legend(fontsize=9); ax3.grid(True, which="both", alpha=0.3)

    # Abajo-derecha: tabla zona small-world
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis("off")
    mask_sw = (L_normalizado[mask] < 0.3) & (C_normalizado[mask] > 0.5)
    p_sw  = p_plot[mask_sw]
    L_sw  = L_array[mask][mask_sw]
    C_sw  = C_array[mask][mask_sw]
    Ln_sw = L_normalizado[mask][mask_sw]
    Cn_sw = C_normalizado[mask][mask_sw]

    if len(p_sw) > 0:
        encabezados = ["p", "L", "C", "L/L₀", "C/C₀", "6 grados"]
        celdas = []
        for i in range(len(p_sw)):
            seis = "✓" if 4 <= L_sw[i] <= 8 else "✗"
            celdas.append([f"{p_sw[i]:.4f}", f"{L_sw[i]:.2f}",
                           f"{C_sw[i]:.4f}", f"{Ln_sw[i]:.3f}",
                           f"{Cn_sw[i]:.3f}", seis])
        tabla = ax4.table(cellText=celdas, colLabels=encabezados,
                          loc="center", cellLoc="center")
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(8)
        tabla.scale(1, 1.4)
    else:
        ax4.text(0.5, 0.5, "No se encontró\nzona small-world\ncon estos parámetros",
                 ha="center", va="center", fontsize=11, color="gray",
                 transform=ax4.transAxes)

    ax4.set_title("Zona Small-World\n(L pequeño + C alto)", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.savefig("dashboard_transicion.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("  Dashboard guardado como dashboard_transicion.png")


def ejecutar():
    while True:
        print("\nDashboard — Resumen Watts-Strogatz (1998)")
        print("1. Generar dashboard con parámetros por defecto (N=100, K=4)")
        print("2. Configurar parámetros")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            resultado = calcularmetricas(n=100, k=4, repeticiones=10)
            graficar_dashboard(*resultado)

        elif opcion == "2":
            print("Configurar parámetros")
            try:
                n = int(input("  Nodos (Enter = 100): ") or "100")
                k = int(input("  Vecinos (Enter = 4): ") or "4")
                repeticiones = int(input("  Repeticiones (Enter = 10): ") or "10")
            except ValueError:
                print("  Entrada no válida, se usarán los valores por defecto")
                n, k, repeticiones = 100, 4, 10
            resultado = calcularmetricas(n=n, k=k, repeticiones=repeticiones)
            graficar_dashboard(*resultado)

        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
            






