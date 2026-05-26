# Simulación de Redes Small World — Watts & Strogatz (1998)

**Autores:** Sol Arias y Andrés González  
**Materia:** Estadística

---

## Descripción

Simulación interactiva del modelo de redes Small World propuesto por Watts y Strogatz en su paper "Collective dynamics of small-world networks" . El proyecto reproduce los resultados principales del paper y añade análisis estadístico, búsqueda de caminos y análisis de robustez.



## Módulos

| # | Módulo | Descripción |
|---|--------|-------------|
| 1 | **Red Small World** | Genera y visualiza redes Watts-Strogatz. Muestra la evolución de la red para distintos valores de p (de regular a aleatoria) |
| 2 | **Transición L(p) & C(p)** | Valida estadísticamente las métricas del paper. Incluye gráfica normalizada (réplica Fig. 2 del paper) y gráfica con bandas ±σ |
| 3 | **Buscador BFS** | Encuentra el camino más corto entre dos nodos de la red usando BFS. Visualiza la ruta con nombres de personas |
| 4 | **Análisis de Robustez** | Analiza cómo se fragmenta la red al eliminar nodos por grado, betweenness o aleatoriamente. Analogía con asteroides (Asphaug) |
| 5 | **Dashboard** | Resumen visual completo: réplica del paper, L(p) y C(p) con bandas ±σ, y tabla de la zona small-world con verificación de los 6 grados de separación |


PROYECTO ESTADISTICA/
├── main.py
└── modulos/
    ├── __init__.py
    ├── red.py
    ├── transicion.py
    ├── bfs.py
    ├── robustez.py
    └── paper.py
