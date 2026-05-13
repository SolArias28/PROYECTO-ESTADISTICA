"""
SIMULACION DE REDES SMALL WORLD 
Sol Arias y Andres Gonzales 
ESTADISTICA

"""
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modulos import (
    red,
    transicion,
    bfs,
    robustez,
    paper,
)
banner="""
SIMULACION DE REDES SMALL WORLD - Watts & Strogatz

"""
Menuprincipal="""
MODULOS
1. Red Small World: generacion y vizualizacion
2.Transición L(p) & C(p):validacion
3.Buscador de caminos BFS: seis grados de separacion
4. Análisis de Robustez: analogia astroides Asphaug
5. Comparacion de redes
0. salir 

"""
MODULOS = {
    "1": ("Red Small World",              red),
    "2": ("Transición L(p) & C(p)",       transicion),
    "3": ("Buscador BFS",                 bfs),
    "4": ("Análisis de Robustez",         robustez),
    "5": ("Comparación Redes",         paper),
    
}

def main():
    print(banner)
    while True:
        print(Menuprincipal)
        opcion=input("Seleccione el modulo: ")
        if opcion == "0":
            print("\n   Small World cerrado.\n")
            break

        elif opcion in MODULOS:
                nombre, modulo = MODULOS[opcion]
                print(f"\n  Abriendo: {nombre}...\n")
                try:
                    modulo.ejecutar()
                except KeyboardInterrupt:
                    print("\n\n    Regresando al menú principal")

        else:
                print("  Opción no válida. ")
if __name__ == "__main__":
    main()




