"""
Ejercicio 5 — Mochila fraccionaria (Fractional Knapsack) — 3 heurísticas
=========================================================================
Una empresa desea maximizar el valor de los objetos cargados en un
contenedor sin exceder el peso máximo. Los objetos PUEDEN fraccionarse.

"""

import os
import time


# ══════════════════════════════════════════════════════════════════
#  DATOS DEL ENUNCIADO
# ══════════════════════════════════════════════════════════════════

ITEMS_ENUNCIADO = [
    # (nombre, cantidad, peso_total, valor_total)
    ("Ítem 1", 3, 210, 15),
    ("Ítem 2", 2, 230, 50),
    ("Ítem 3", 4, 150, 20),
    ("Ítem 4", 5,  40, 55),
    ("Ítem 5", 1, 500, 300),
]
PESO_MAX_ENUNCIADO = 520


# ══════════════════════════════════════════════════════════════════
#  ALGORITMO PRINCIPAL — MOCHILA FRACCIONARIA VORAZ
# ══════════════════════════════════════════════════════════════════

def mochila_fraccionaria(items, W, criterio, pasos):
    """
    Resuelve la mochila fraccionaria con una heurística voraz.

    Parámetros:
        items    -- lista de tuplas (nombre, cantidad, peso, valor)
        W        -- capacidad máxima de la mochila
        criterio -- 'valor' | 'peso' | 'ratio'
        pasos    -- lista donde se registran los pasos

    Retorna:
        (valor_total, seleccion)
        - valor_total : float, valor obtenido
        - seleccion   : lista de (nombre, fraccion_tomada, peso_tomado, valor_tomado)
    """
    nombres_criterio = {
        'valor': 'Mayor valor total (H1)',
        'peso' : 'Menor peso total (H2)',
        'ratio': 'Mayor relación valor/peso (H3 — óptima)',
    }

    pasos.append({
        'tipo': 'inicio',
        'desc': (
            f"Heurística: {nombres_criterio[criterio]}\n"
            f"  Capacidad máxima W = {W} toneladas\n"
            f"  Ítems disponibles  : {len(items)}"
        )
    })

    # Calcular relación valor/peso y ordenar según criterio
    enriquecidos = []
    for nom, cant, peso, val in items:
        ratio = val / peso if peso > 0 else 0
        enriquecidos.append({
            'nombre': nom, 'cantidad': cant,
            'peso': peso, 'valor': val, 'ratio': ratio
        })

    if criterio == 'valor':
        enriquecidos.sort(key=lambda x: x['valor'], reverse=True)
    elif criterio == 'peso':
        enriquecidos.sort(key=lambda x: x['peso'])
    else:  # ratio
        enriquecidos.sort(key=lambda x: x['ratio'], reverse=True)

    pasos.append({
        'tipo': 'ordenar',
        'desc': (
            f"Orden de procesamiento según {nombres_criterio[criterio]}:\n"
            + "\n".join(
                f"    {it['nombre']:8}  peso={it['peso']:>4}  "
                f"valor={it['valor']:>4}  ratio={it['ratio']:.4f}"
                for it in enriquecidos
            )
        )
    })

    restante   = W
    valor_total = 0.0
    seleccion   = []

    for it in enriquecidos:
        if restante <= 0:
            break

        nombre = it['nombre']
        peso   = it['peso']
        valor  = it['valor']
        ratio  = it['ratio']

        if peso <= restante:
            # Tomar el ítem completo
            fraccion      = 1.0
            peso_tomado   = peso
            valor_tomado  = valor
            restante     -= peso
            valor_total  += valor

            pasos.append({
                'tipo': 'tomar_total',
                'desc': (
                    f"{nombre}: tomar el 100%  "
                    f"→  peso={peso_tomado}  valor={valor_tomado:.2f}  "
                    f"restante en mochila={restante}"
                )
            })
        else:
            # Tomar fracción
            fraccion      = restante / peso
            peso_tomado   = restante
            valor_tomado  = valor * fraccion
            valor_total  += valor_tomado
            restante      = 0

            pasos.append({
                'tipo': 'tomar_fraccion',
                'desc': (
                    f"{nombre}: tomar el {fraccion*100:.1f}%  "
                    f"→  peso={peso_tomado:.2f}  valor={valor_tomado:.2f}  "
                    f"mochila llena"
                )
            })

        seleccion.append((nombre, fraccion, peso_tomado, valor_tomado))

    pasos.append({
        'tipo': 'resultado',
        'valor_total': valor_total,
        'peso_usado': W - restante,
        'desc': (
            f"RESULTADO — {nombres_criterio[criterio]}\n"
            f"  Valor total obtenido : {valor_total:.4f}\n"
            f"  Peso utilizado       : {W - restante:.2f} / {W}"
        )
    })

    return valor_total, seleccion


# ══════════════════════════════════════════════════════════════════
#  PRUEBA DE ESCRITORIO EN CONSOLA
# ══════════════════════════════════════════════════════════════════

def sep(c='─', n=68):
    print(c * n)


def prueba_escritorio_mochila(items, W, pasos_h1, pasos_h2, pasos_h3,
                               res_h1, sel_h1, res_h2, sel_h2,
                               res_h3, sel_h3, modo_animado=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    sep('═')
    print("  PRUEBA DE ESCRITORIO — Mochila fraccionaria (3 heurísticas)")
    sep('═')
    print(f"  Capacidad W = {W} toneladas")
    print()
    print(f"  {'Ítem':8}  {'Cantidad':>9}  {'Peso':>6}  {'Valor':>7}  {'Ratio v/p':>10}")
    sep('─', 55)
    for nom, cant, peso, val in items:
        r = val / peso if peso > 0 else 0
        print(f"  {nom:8}  {cant:>9}  {peso:>6}  {val:>7}  {r:>10.4f}")
    sep()
    print()

    for etiqueta, pasos in [("H1 — Mayor valor", pasos_h1),
                             ("H2 — Menor peso",  pasos_h2),
                             ("H3 — Mayor ratio", pasos_h3)]:
        sep('═')
        print(f"  HEURÍSTICA: {etiqueta}")
        sep('═')
        for num, paso in enumerate(pasos, 1):
            tipo = paso['tipo']
            desc = paso.get('desc', '')
            print(f"  Paso {num:>3}  [{tipo.upper():^15}]")
            sep('─', 55)
            for linea in desc.split('\n'):
                print(f"  {linea}")
            print()
            if not modo_animado:
                entrada = input("  [Enter = siguiente | 'q' = saltar al final] ").strip().lower()
                if entrada == 'q':
                    modo_animado = True
                    print()
            else:
                time.sleep(0.05)

    # ── Tabla comparativa final ──
    sep('═')
    print()
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║           COMPARACIÓN DE HEURÍSTICAS                    ║")
    print("  ╠══════════════════╦═══════════════╦════════════════════╗  ║")
    print("  ║  Heurística      ║  Valor total  ║  ¿Es óptima?       ║  ║")
    print("  ╠══════════════════╬═══════════════╬════════════════════╣  ║")

    mejor = max(res_h1, res_h2, res_h3)
    for etiq, res in [("H1 Mayor valor", res_h1),
                      ("H2 Menor peso",  res_h2),
                      ("H3 Mayor ratio", res_h3)]:
        optima = "✓ Sí" if abs(res - mejor) < 1e-6 else "✗ No"
        print(f"  ║  {etiq:<16}║  {res:>13.4f}  ║  {optima:<18}║  ║")

    print("  ╚══════════════════╩═══════════════╩════════════════════╝  ║")
    print("  ╚════════════════════════════════════════════════════════════╝")
    print()
    print("  Justificación:")
    print("  H3 (mayor relación valor/peso) es la heurística óptima para")
    print("  la mochila fraccionaria. Al poder tomar fracciones, tomar")
    print("  primero los ítems con mayor valor por unidad de peso garantiza")
    print("  el máximo valor por unidad de capacidad consumida en cada paso.")
    print()
    print("  Complejidad temporal : O(n log n) por heurística")
    print("  Complejidad espacial : O(n)")

    input("\n  Presiona Enter para volver al menú...")


# ══════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("=" * 60)
    print("  Ejercicio 5 — Mochila fraccionaria")
    print("  Estrategia: Algoritmo Voraz — 3 heurísticas")
    print("=" * 60)
    print()
    print("  Se usarán los datos del enunciado:")
    print("  W = 520 toneladas")
    for nom, cant, peso, val in ITEMS_ENUNCIADO:
        print(f"    {nom}: cantidad={cant}, peso={peso}, valor={val}")
    print()
    print("  ¿Cómo quieres ver la prueba de escritorio?")
    print("  1. Interactivo (Enter en cada paso)")
    print("  2. Automático  (pausa breve entre pasos)")
    modo = input("  Modo [1/2]: ").strip()
    animado = (modo == '2')

    items = ITEMS_ENUNCIADO
    W     = PESO_MAX_ENUNCIADO

    pasos_h1 = []
    res_h1, sel_h1 = mochila_fraccionaria(items, W, 'valor', pasos_h1)

    pasos_h2 = []
    res_h2, sel_h2 = mochila_fraccionaria(items, W, 'peso',  pasos_h2)

    pasos_h3 = []
    res_h3, sel_h3 = mochila_fraccionaria(items, W, 'ratio', pasos_h3)

    prueba_escritorio_mochila(
        items, W,
        pasos_h1, pasos_h2, pasos_h3,
        res_h1, sel_h1,
        res_h2, sel_h2,
        res_h3, sel_h3,
        modo_animado=animado
    )


if __name__ == '__main__':
    main()