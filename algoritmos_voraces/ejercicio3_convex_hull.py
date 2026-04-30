"""
Ejercicio 3 — Convex Hull (Envolvente Convexa) — Graham Scan
=============================================================
Encuentra el polígono convexo más pequeño que contiene todos los puntos
de un conjunto dado en el plano 2D.

Ejemplo del enunciado:
  Entrada : [[0,0],[1,-4],[-1,-5],[-5,-3],[-3,-1],
             [-1,-3],[-2,-2],[-1,-1],[-2,-1],[-1,1]]
  Salida  : puntos del casco en orden antihorario
"""

import os
import math
from functools import cmp_to_key


# ══════════════════════════════════════════════════════════════════
#  CLASES Y FUNCIONES AUXILIARES
# ══════════════════════════════════════════════════════════════════

class Punto:
    """Representa un punto en el plano 2D."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


def orientacion(a, b, c):
    """
    Determina la orientación del triplete (a, b, c).

    Calcula el producto vectorial cruzado (b-a) × (c-a).
      - Negativo  → sentido horario (clockwise)
      - Positivo  → sentido antihorario (counter-clockwise)
      - Cero      → colineal

    Retorna: -1 (horario) | 1 (antihorario) | 0 (colineal)
    """
    val = (a.x * (b.y - c.y) +
           b.x * (c.y - a.y) +
           c.x * (a.y - b.y))
    if val < 0:
        return -1   # Horario
    elif val > 0:
        return 1    # Antihorario
    return 0        # Colineal


def dist_cuadrada(a, b):
    """Distancia al cuadrado entre dos puntos (evita usar sqrt)."""
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


# ══════════════════════════════════════════════════════════════════
#  ALGORITMO PRINCIPAL — GRAHAM SCAN
# ══════════════════════════════════════════════════════════════════

def graham_scan(puntos_raw, pasos):
    """
    Ejecuta el algoritmo Graham Scan sobre una lista de pares [x, y].

    Parámetros:
        puntos_raw -- lista de listas [[x1,y1], [x2,y2], ...]
        pasos      -- lista donde se registran los pasos de la prueba
                      de escritorio

    Retorna:
        Lista de [x, y] de los vértices de la envolvente en orden
        antihorario, o [[-1]] si no es posible calcularla.
    """
    n = len(puntos_raw)

    pasos.append({
        'tipo': 'inicio',
        'desc': f"Conjunto de {n} puntos de entrada: {puntos_raw}"
    })

    if n < 3:
        pasos.append({'tipo': 'error', 'desc': "Se necesitan al menos 3 puntos."})
        return [[-1]]

    # Convertir a objetos Punto
    puntos = [Punto(p[0], p[1]) for p in puntos_raw]

    # ── Paso 1: Elegir el punto ancla (menor Y, desempate menor X) ──
    p0 = min(puntos, key=lambda p: (p.y, p.x))
    pasos.append({
        'tipo': 'ancla',
        'desc': f"Punto ancla p0 = ({p0.x}, {p0.y})  "
                f"[menor Y, desempate menor X]"
    })

    # ── Paso 2: Ordenar por ángulo polar respecto a p0 ──
    def comparar(p1, p2):
        o = orientacion(p0, p1, p2)
        if o == 0:
            # Colineales: primero el más cercano
            return dist_cuadrada(p0, p1) - dist_cuadrada(p0, p2)
        return -1 if o > 0 else 1   # antihorario primero

    ordenados = sorted(puntos, key=cmp_to_key(comparar))

    pasos.append({
        'tipo': 'ordenar',
        'puntos': [(p.x, p.y) for p in ordenados],
        'desc': (
            f"Puntos ordenados por ángulo polar desde p0:\n"
            + "    " + "  →  ".join(f"({p.x},{p.y})" for p in ordenados)
        )
    })

    # ── Paso 3: Eliminar colineales intermedios ──
    m = 1
    i = 1
    while i < len(ordenados):
        while (i < len(ordenados) - 1 and
               orientacion(p0, ordenados[i], ordenados[i + 1]) == 0):
            i += 1
        ordenados[m] = ordenados[i]
        m += 1
        i += 1

    if m < 3:
        pasos.append({'tipo': 'error',
                      'desc': "Menos de 3 puntos no colineales — envolvente no posible."})
        return [[-1]]

    ordenados = ordenados[:m]

    pasos.append({
        'tipo': 'sin_colineales',
        'puntos': [(p.x, p.y) for p in ordenados],
        'desc': (
            f"Después de eliminar colineales intermedios ({m} puntos):\n"
            + "    " + "  →  ".join(f"({p.x},{p.y})" for p in ordenados)
        )
    })

    # ── Paso 4: Construcción de la pila (núcleo voraz) ──
    pila = [ordenados[0], ordenados[1]]

    pasos.append({
        'tipo': 'pila_inicio',
        'pila': [(p.x, p.y) for p in pila],
        'desc': f"Inicializar pila con los dos primeros puntos: {[(p.x,p.y) for p in pila]}"
    })

    for i in range(2, m):
        punto_nuevo = ordenados[i]

        while (len(pila) > 1 and
               orientacion(pila[-2], pila[-1], punto_nuevo) >= 0):
            descartado = pila.pop()
            pasos.append({
                'tipo': 'descartar',
                'descartado': (descartado.x, descartado.y),
                'nuevo': (punto_nuevo.x, punto_nuevo.y),
                'pila': [(p.x, p.y) for p in pila],
                'desc': (
                    f"Giro NO antihorario al agregar ({punto_nuevo.x},{punto_nuevo.y})  "
                    f"→  descartar ({descartado.x},{descartado.y}) de la pila\n"
                    f"    Pila ahora: {[(p.x,p.y) for p in pila]}"
                )
            })

        pila.append(punto_nuevo)
        pasos.append({
            'tipo': 'agregar',
            'nuevo': (punto_nuevo.x, punto_nuevo.y),
            'pila': [(p.x, p.y) for p in pila],
            'desc': (
                f"Agregar ({punto_nuevo.x},{punto_nuevo.y}) a la pila  →  "
                f"pila: {[(p.x,p.y) for p in pila]}"
            )
        })

    if len(pila) < 3:
        pasos.append({'tipo': 'error',
                      'desc': "Envolvente inválida (menos de 3 vértices)."})
        return [[-1]]

    resultado = [[int(p.x), int(p.y)] for p in pila]

    pasos.append({
        'tipo': 'resultado',
        'vertices': resultado,
        'desc': (
            f"Envolvente convexa con {len(resultado)} vértices "
            f"(orden antihorario):\n"
            + "    " + "  →  ".join(f"({p[0]},{p[1]})" for p in resultado)
            + f"  →  ({resultado[0][0]},{resultado[0][1]}) [cierre]"
        )
    })

    return resultado


# ══════════════════════════════════════════════════════════════════
#  PRUEBA DE ESCRITORIO EN CONSOLA
# ══════════════════════════════════════════════════════════════════

def sep(c='─', n=65):
    print(c * n)


def dibujar_hull_ascii(puntos_raw, hull):
    """
    Muestra una cuadrícula ASCII muy sencilla con los puntos
    marcando cuáles son parte del casco y cuáles son interiores.
    """
    if not puntos_raw:
        return

    hull_set = set(tuple(p) for p in hull)
    xs = [p[0] for p in puntos_raw]
    ys = [p[1] for p in puntos_raw]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Escalar a una cuadrícula de 40 × 16 celdas
    COLS, ROWS = 40, 16
    grid = [['·'] * COLS for _ in range(ROWS)]

    def mapear(px, py):
        col = int((px - min_x) / max(max_x - min_x, 1) * (COLS - 1))
        row = int((max_y - py) / max(max_y - min_y, 1) * (ROWS - 1))
        return row, col

    for p in puntos_raw:
        r, c = mapear(p[0], p[1])
        grid[r][c] = '○'   # Punto interior

    for p in hull:
        r, c = mapear(p[0], p[1])
        grid[r][c] = '●'   # Vértice del casco

    print()
    print("  Visualización ASCII  (● = vértice del casco  ○ = interior)")
    sep('─', 50)
    for fila in grid:
        print("  " + ' '.join(fila))
    sep('─', 50)
    print()


def prueba_escritorio_convex(puntos_raw, hull, pasos, modo_animado=False):
    import time
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    sep('═')
    print("  PRUEBA DE ESCRITORIO — Convex Hull (Graham Scan)")
    sep('═')
    print(f"  Puntos de entrada ({len(puntos_raw)}): {puntos_raw}")
    sep()
    print()

    for num, paso in enumerate(pasos, 1):
        tipo = paso['tipo']
        desc = paso.get('desc', '')

        print(f"  Paso {num:>3}  [{tipo.upper():^15}]")
        sep('─', 55)
        # Imprimir desc respetando saltos de línea internos
        for linea in desc.split('\n'):
            print(f"  {linea}")
        print()

        if not modo_animado:
            entrada = input("  [Enter = siguiente | 'q' = saltar al final] ").strip().lower()
            if entrada == 'q':
                modo_animado = True
                print()
        else:
            time.sleep(0.06)

    # Visualización ASCII al final
    if hull != [[-1]]:
        dibujar_hull_ascii(puntos_raw, hull)

        sep('═')
        print()
        print("  ╔══════════════════════════════════════════════════╗")
        print("  ║              RESULTADO FINAL                     ║")
        print("  ╠══════════════════════════════════════════════════╣")
        print(f"  ║  Vértices del casco: {len(hull):<29}║")
        for v in hull:
            print(f"  ║    ({v[0]:>4}, {v[1]:>4}){' '*38}║")
        print("  ╚══════════════════════════════════════════════════╝")
        print()
        print("  Complejidad temporal : O(n log n)")
        print("  Complejidad espacial : O(n)")
    else:
        print("  Resultado: -1 (no fue posible calcular la envolvente)")

    input("\n  Presiona Enter para volver al menú...")


# ══════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("=" * 60)
    print("  Ejercicio 3 — Convex Hull (Envolvente Convexa)")
    print("  Algoritmo: Graham Scan")
    print("=" * 60)
    print()
    print("  Opciones de entrada:")
    print("  1. Usar el ejemplo del enunciado")
    print("  2. Ingresar puntos manualmente")
    print()
    opcion = input("  Opción [1/2]: ").strip()

    if opcion == '2':
        print()
        print("  Ingresa los puntos como pares x,y separados por punto y coma.")
        print("  Ejemplo: 0,0; 1,-4; -1,-5; -5,-3")
        print()
        raw = input("  Puntos: ").strip()
        try:
            puntos = []
            for par in raw.split(';'):
                xy = par.strip().split(',')
                puntos.append([int(xy[0].strip()), int(xy[1].strip())])
        except Exception:
            print("  Error al parsear. Usando ejemplo por defecto.")
            puntos = [[0,0],[1,-4],[-1,-5],[-5,-3],[-3,-1],
                      [-1,-3],[-2,-2],[-1,-1],[-2,-1],[-1,1]]
    else:
        puntos = [[0,0],[1,-4],[-1,-5],[-5,-3],[-3,-1],
                  [-1,-3],[-2,-2],[-1,-1],[-2,-1],[-1,1]]

    print()
    print("  ¿Cómo quieres ver la prueba de escritorio?")
    print("  1. Interactivo (Enter en cada paso)")
    print("  2. Automático  (pausa breve entre pasos)")
    modo = input("  Modo [1/2]: ").strip()
    animado = (modo == '2')

    pasos = []
    hull = graham_scan(puntos, pasos)
    prueba_escritorio_convex(puntos, hull, pasos, modo_animado=animado)


if __name__ == '__main__':
    main()