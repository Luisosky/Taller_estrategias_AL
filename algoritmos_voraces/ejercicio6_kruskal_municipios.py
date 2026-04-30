"""
Ejercicio 6 — Red de municipios con fibra óptica — Kruskal MST
==============================================================
Un proveedor de internet quiere conectar N municipios de un departamento
de Colombia con fibra óptica al menor costo posible, sin formar ciclos.
"""

import os
import time
from functools import cmp_to_key


# ══════════════════════════════════════════════════════════════════
#  DATOS DEL EJEMPLO — Departamento del Quindío
# ══════════════════════════════════════════════════════════════════

MUNICIPIOS = [
    "Armenia",    # 0
    "Calarcá",    # 1
    "Montenegro", # 2
    "Quimbaya",   # 3
    "Circasia",   # 4
    "La Tebaida", # 5
]

# Aristas: (municipio_i, municipio_j, costo_en_millones_COP)
ARISTAS = [
    (0, 1,  8),   # Armenia    ↔ Calarcá       — 8M
    (0, 2, 15),   # Armenia    ↔ Montenegro    — 15M
    (0, 4, 10),   # Armenia    ↔ Circasia      — 10M
    (0, 5,  6),   # Armenia    ↔ La Tebaida    —  6M
    (1, 2, 12),   # Calarcá    ↔ Montenegro    — 12M
    (1, 4,  9),   # Calarcá    ↔ Circasia      —  9M
    (2, 3,  7),   # Montenegro ↔ Quimbaya      —  7M
    (2, 4, 11),   # Montenegro ↔ Circasia      — 11M
    (3, 4, 14),   # Quimbaya   ↔ Circasia      — 14M
    (3, 5, 20),   # Quimbaya   ↔ La Tebaida    — 20M
    (4, 5, 13),   # Circasia   ↔ La Tebaida    — 13M
]


# ══════════════════════════════════════════════════════════════════
#  ESTRUCTURA CONJUNTOS DISJUNTOS (Union-Find / DSU)
# ══════════════════════════════════════════════════════════════════

class DSU:
    """
    Conjuntos Disjuntos con compresión de camino y unión por rango.
    Permite determinar si dos nodos pertenecen al mismo componente
    y unirlos en O(α(n)) amortizado.
    """
    def __init__(self, n):
        self.padre = list(range(n))
        self.rango  = [0] * n

    def encontrar(self, i):
        """Encuentra el representante del conjunto de i (con compresión)."""
        if self.padre[i] != i:
            self.padre[i] = self.encontrar(self.padre[i])  # compresión de camino
        return self.padre[i]

    def unir(self, x, y):
        """Une los conjuntos de x e y. Retorna True si eran distintos."""
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx == ry:
            return False  # Ya estaban conectados → agregar formaría ciclo
        # Unión por rango
        if self.rango[rx] < self.rango[ry]:
            self.padre[rx] = ry
        elif self.rango[rx] > self.rango[ry]:
            self.padre[ry] = rx
        else:
            self.padre[ry] = rx
            self.rango[rx] += 1
        return True


# ══════════════════════════════════════════════════════════════════
#  ALGORITMO PRINCIPAL — KRUSKAL
# ══════════════════════════════════════════════════════════════════

def kruskal_mst(municipios, aristas, pasos):
    """
    Calcula el Árbol de Expansión Mínima usando Kruskal.

    Parámetros:
        municipios -- lista de nombres de municipios
        aristas    -- lista de tuplas (i, j, costo)
        pasos      -- lista donde se registran los pasos

    Retorna:
        (costo_total, aristas_mst)
        - costo_total  : int, costo total del MST
        - aristas_mst  : lista de tuplas (nombre_i, nombre_j, costo)
    """
    V = len(municipios)
    E = len(aristas)

    pasos.append({
        'tipo': 'inicio',
        'desc': (
            f"Municipios ({V}): {', '.join(municipios)}\n"
            f"  Total de posibles conexiones (aristas): {E}\n"
            f"  Objetivo: árbol de expansión mínima con {V-1} aristas"
        )
    })

    # Paso 1: Ordenar aristas por costo
    aristas_ord = sorted(aristas, key=lambda a: a[2])

    pasos.append({
        'tipo': 'ordenar',
        'desc': (
            "Aristas ordenadas por costo (menor → mayor):\n"
            + "\n".join(
                f"    {municipios[i]:12} ↔ {municipios[j]:12}  "
                f"costo = {c:>3} M COP"
                for i, j, c in aristas_ord
            )
        )
    })

    dsu          = DSU(V)
    costo_total  = 0
    aristas_mst  = []
    conteo       = 0

    pasos.append({
        'tipo': 'proceso',
        'desc': "Inicio del proceso voraz — evaluar cada arista en orden:"
    })

    for i, j, costo in aristas_ord:
        if conteo == V - 1:
            break  # MST completo

        nom_i = municipios[i]
        nom_j = municipios[j]

        if dsu.unir(i, j):
            # No forma ciclo → incluir en MST
            costo_total += costo
            conteo      += 1
            aristas_mst.append((nom_i, nom_j, costo))

            pasos.append({
                'tipo': 'incluir',
                'arista': (nom_i, nom_j, costo),
                'mst_actual': list(aristas_mst),
                'costo_acum': costo_total,
                'aristas_mst': conteo,
                'desc': (
                    f"✓ INCLUIR: {nom_i} ↔ {nom_j}  "
                    f"costo={costo} M  |  "
                    f"no forma ciclo  |  "
                    f"costo acumulado={costo_total} M  "
                    f"({conteo}/{V-1} aristas del MST)"
                )
            })
        else:
            pasos.append({
                'tipo': 'descartar',
                'arista': (nom_i, nom_j, costo),
                'desc': (
                    f"✗ DESCARTAR: {nom_i} ↔ {nom_j}  "
                    f"costo={costo} M  |  "
                    f"formaría un ciclo → se descarta"
                )
            })

    pasos.append({
        'tipo': 'resultado',
        'costo_total': costo_total,
        'aristas_mst': aristas_mst,
        'desc': (
            f"MST COMPLETO — {len(aristas_mst)} conexiones  |  "
            f"Costo total = {costo_total} millones de COP\n"
            + "\n".join(
                f"    {a} ↔ {b}  — {c} M"
                for a, b, c in aristas_mst
            )
        )
    })

    return costo_total, aristas_mst


# ══════════════════════════════════════════════════════════════════
#  VISUALIZACIÓN ASCII DEL ÁRBOL
# ══════════════════════════════════════════════════════════════════

def dibujar_mst_ascii(municipios, aristas_mst, costo_total):
    """Imprime el MST como lista de adyacencia."""
    print()
    print("  Árbol de expansión mínima (lista de conexiones):")
    print()
    adyacencia = {m: [] for m in municipios}
    for a, b, c in aristas_mst:
        adyacencia[a].append((b, c))
        adyacencia[b].append((a, c))

    for mun in municipios:
        vecinos = adyacencia[mun]
        if vecinos:
            linea = f"  {mun:12} ──"
            for v, c in vecinos:
                linea += f"── [{c}M] ──── {v}   "
            print(linea)


# ══════════════════════════════════════════════════════════════════
#  PRUEBA DE ESCRITORIO EN CONSOLA
# ══════════════════════════════════════════════════════════════════

def sep(c='─', n=68):
    print(c * n)


def prueba_escritorio_kruskal(municipios, aristas, costo_total,
                               aristas_mst, pasos, modo_animado=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    sep('═')
    print("  PRUEBA DE ESCRITORIO — Red de municipios (Kruskal MST)")
    sep('═')
    print(f"  Municipios ({len(municipios)}): {', '.join(municipios)}")
    print(f"  Aristas posibles  : {len(aristas)}")
    sep()
    print()

    for num, paso in enumerate(pasos, 1):
        tipo = paso['tipo']
        desc = paso.get('desc', '')
        print(f"  Paso {num:>3}  [{tipo.upper():^12}]")
        sep('─', 58)
        for linea in desc.split('\n'):
            print(f"  {linea}")
        print()

        if not modo_animado:
            entrada = input("  [Enter = siguiente | 'q' = saltar al final] ").strip().lower()
            if entrada == 'q':
                modo_animado = True
                print()
        else:
            time.sleep(0.07)

    # Tabla final
    sep('═')
    print()
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║           RESULTADO FINAL — MST KRUSKAL                 ║")
    print("  ╠════════════════════════╦═══════════════════╦════════════╣")
    print("  ║  Municipio A           ║  Municipio B      ║  Costo (M) ║")
    print("  ╠════════════════════════╬═══════════════════╬════════════╣")
    for a, b, c in aristas_mst:
        print(f"  ║  {a:<22}║  {b:<17}║  {c:>8}  ║")
    print("  ╠════════════════════════╩═══════════════════╬════════════╣")
    print(f"  ║  COSTO TOTAL (millones COP)               ║  {costo_total:>8}  ║")
    print("  ╚═══════════════════════════════════════════╩════════════╝")
    print()

    dibujar_mst_ascii(municipios, aristas_mst, costo_total)

    print()
    print("  Complejidad temporal : O(E log E)  donde E = nro. de aristas")
    print("  Complejidad espacial : O(V + E)")
    print()
    print("  ¿Por qué Kruskal es voraz?")
    print("  En cada paso elige la arista más barata que no forme ciclo.")
    print("  La propiedad del 'corte mínimo' garantiza que esta elección")
    print("  local siempre lleva al árbol de costo mínimo global.")

    input("\n  Presiona Enter para volver al menú...")


# ══════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("=" * 60)
    print("  Ejercicio 6 — Red de fibra óptica entre municipios")
    print("  Algoritmo: Kruskal (Árbol de Expansión Mínima)")
    print("=" * 60)
    print()
    print("  Ejemplo: 6 municipios del Quindío, Colombia")
    print("  Costos en millones de pesos colombianos (COP)")
    print()
    print("  ¿Cómo quieres ver la prueba de escritorio?")
    print("  1. Interactivo (Enter en cada paso)")
    print("  2. Automático  (pausa breve entre pasos)")
    modo = input("  Modo [1/2]: ").strip()
    animado = (modo == '2')

    pasos = []
    costo_total, aristas_mst = kruskal_mst(MUNICIPIOS, ARISTAS, pasos)
    prueba_escritorio_kruskal(MUNICIPIOS, ARISTAS, costo_total,
                               aristas_mst, pasos, modo_animado=animado)


if __name__ == '__main__':
    main()