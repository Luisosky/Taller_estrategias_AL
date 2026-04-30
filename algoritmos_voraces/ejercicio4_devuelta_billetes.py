"""
Ejercicio 4 — Problema de la devuelta (billetes con disponibilidad limitada)
=============================================================================
Dado un monto (múltiplo de 10.000) y una cantidad limitada de billetes por
denominación, determinar la forma de entregar el dinero usando el MÍNIMO
número de billetes.

Ejemplo del enunciado:
  Denominaciones : [10000, 20000, 50000, 100000]
  Disponibilidad  : [3, 2, 1, 5]
  Monto           : ingresado por el usuario (múltiplo de 10.000)
"""

import os
import time


# ══════════════════════════════════════════════════════════════════
#  ALGORITMO PRINCIPAL — GREEDY DEVUELTA
# ══════════════════════════════════════════════════════════════════

def devuelta_greedy(monto, denominaciones, disponibilidad, pasos):
    """
    Calcula la devuelta con el mínimo número de billetes usando voraz.

    Parámetros:
        monto           -- entero, monto a entregar (múltiplo de 10.000)
        denominaciones  -- lista de enteros en orden DESCENDENTE
        disponibilidad  -- lista de enteros, cantidad disponible por denom.
        pasos           -- lista donde se registran los pasos

    Retorna:
        (usado, posible)
        - usado    : lista de cuántos billetes de cada denominación se usan
        - posible  : True si se pudo hacer exactamente el monto
    """
    # Ordenar de mayor a menor para garantizar el enfoque voraz
    pares = sorted(zip(denominaciones, disponibilidad), reverse=True)
    dens_ord  = [p[0] for p in pares]
    disp_ord  = [p[1] for p in pares]

    pasos.append({
        'tipo': 'inicio',
        'desc': (
            f"Monto a entregar : ${monto:,}\n"
            f"  Denominaciones ordenadas (mayor → menor): {dens_ord}\n"
            f"  Disponibilidad                          : {disp_ord}"
        )
    })

    restante = monto
    usado    = [0] * len(dens_ord)

    for idx, (den, disp) in enumerate(zip(dens_ord, disp_ord)):
        if restante == 0:
            break
        if den > restante:
            pasos.append({
                'tipo': 'saltar',
                'denominacion': den,
                'restante': restante,
                'desc': (
                    f"Denominación ${den:,}  >  restante ${restante:,}  "
                    f"→  saltar esta denominación"
                )
            })
            continue

        # Máximo de billetes de esta denominación que podemos usar
        cantidad = min(disp, restante // den)
        usado[idx] = cantidad
        restante  -= cantidad * den

        pasos.append({
            'tipo': 'usar',
            'denominacion': den,
            'disponible': disp,
            'cantidad': cantidad,
            'subtotal': cantidad * den,
            'restante': restante,
            'desc': (
                f"Denominación ${den:,}  |  "
                f"disponible={disp}  |  "
                f"caben={restante + cantidad*den}//{{den}}={cantidad}  →  "
                f"usar {cantidad} billete(s)  "
                f"(${cantidad*den:,})  |  "
                f"restante=${restante:,}"
            )
        })

    posible = (restante == 0)

    if posible:
        total_billetes = sum(usado)
        detalle = [
            f"  ${dens_ord[i]:>7,} × {usado[i]}"
            for i in range(len(dens_ord)) if usado[i] > 0
        ]
        pasos.append({
            'tipo': 'resultado',
            'usado': list(zip(dens_ord, usado)),
            'total': total_billetes,
            'desc': (
                f"SOLUCIÓN ENCONTRADA — {total_billetes} billete(s) en total\n"
                + "\n".join(detalle)
            )
        })
    else:
        pasos.append({
            'tipo': 'imposible',
            'restante': restante,
            'desc': (
                f"NO ES POSIBLE entregar exactamente ${monto:,}.\n"
                f"  Faltan ${restante:,} que no pueden cubrirse con los billetes disponibles."
            )
        })

    return list(zip(dens_ord, usado)), posible


# ══════════════════════════════════════════════════════════════════
#  PRUEBA DE ESCRITORIO EN CONSOLA
# ══════════════════════════════════════════════════════════════════

def sep(c='─', n=65):
    print(c * n)


def prueba_escritorio_devuelta(monto, denominaciones, disponibilidad,
                               resultado, posible, pasos, modo_animado=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    sep('═')
    print("  PRUEBA DE ESCRITORIO — Devuelta de billetes (Greedy)")
    sep('═')
    print(f"  Monto a entregar  : ${monto:,}")
    print(f"  Denominaciones    : {denominaciones}")
    print(f"  Disponibilidad    : {disponibilidad}")
    sep()
    print()

    for num, paso in enumerate(pasos, 1):
        tipo = paso['tipo']
        desc = paso.get('desc', '')

        print(f"  Paso {num:>3}  [{tipo.upper():^12}]")
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
            time.sleep(0.07)

    # Tabla resumen
    sep('═')
    print()
    if posible:
        print("  ╔═════════════════════════════════════════════════╗")
        print("  ║           RESULTADO FINAL — SOLUCIÓN            ║")
        print("  ╠═══════════════╦══════════════╦══════════════════╣")
        print("  ║  Denominación ║   Cantidad   ║     Subtotal     ║")
        print("  ╠═══════════════╬══════════════╬══════════════════╣")
        total_b = 0
        total_v = 0
        for den, cant in resultado:
            if cant > 0:
                sub = den * cant
                total_b += cant
                total_v += sub
                print(f"  ║  ${den:>9,}  ║  {cant:>10}  ║  ${sub:>13,}  ║")
        print("  ╠═══════════════╬══════════════╬══════════════════╣")
        print(f"  ║  TOTAL        ║  {total_b:>10}  ║  ${total_v:>13,}  ║")
        print("  ╚═══════════════╩══════════════╩══════════════════╝")
        print()
        print("  Complejidad temporal : O(d)  donde d = nro. de denominaciones")
        print("  Complejidad espacial : O(d)")
    else:
        print("  ╔═════════════════════════════════════════════════╗")
        print("  ║       RESULTADO: NO HAY SOLUCIÓN POSIBLE        ║")
        print("  ╚═════════════════════════════════════════════════╝")

    input("\n  Presiona Enter para volver al menú...")


# ══════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("=" * 60)
    print("  Ejercicio 4 — Devuelta de billetes")
    print("  Estrategia: Algoritmo Voraz (Greedy)")
    print("=" * 60)
    print()
    print("  Denominaciones del ejemplo: [10000, 20000, 50000, 100000]")
    print("  Disponibilidad del ejemplo: [3, 2, 1, 5]")
    print()
    print("  Opciones:")
    print("  1. Usar los datos del enunciado (ingresar solo el monto)")
    print("  2. Ingresar todos los datos manualmente")
    print()
    opcion = input("  Opción [1/2]: ").strip()

    if opcion == '2':
        print()
        try:
            raw_den = input("  Denominaciones (sep. por coma): ").strip()
            denominaciones = [int(x.strip()) for x in raw_den.split(',')]
            raw_dis = input("  Disponibilidad (sep. por coma): ").strip()
            disponibilidad = [int(x.strip()) for x in raw_dis.split(',')]
            if len(denominaciones) != len(disponibilidad):
                print("  Error: la cantidad de denominaciones y disponibilidades debe coincidir.")
                input("  Presiona Enter para volver..."); return
        except ValueError:
            print("  Error al parsear. Usando datos del enunciado.")
            denominaciones = [10000, 20000, 50000, 100000]
            disponibilidad = [3, 2, 1, 5]
    else:
        denominaciones = [10000, 20000, 50000, 100000]
        disponibilidad = [3, 2, 1, 5]

    print()
    try:
        monto = int(input("  Monto a entregar (múltiplo de 10.000): $").strip())
    except ValueError:
        print("  Valor inválido. Usando $230.000 como ejemplo.")
        monto = 230000

    print()
    print("  ¿Cómo quieres ver la prueba de escritorio?")
    print("  1. Interactivo (Enter en cada paso)")
    print("  2. Automático  (pausa breve entre pasos)")
    modo = input("  Modo [1/2]: ").strip()
    animado = (modo == '2')

    pasos = []
    resultado, posible = devuelta_greedy(monto, denominaciones, disponibilidad, pasos)
    prueba_escritorio_devuelta(monto, denominaciones, disponibilidad,
                               resultado, posible, pasos, modo_animado=animado)


if __name__ == '__main__':
    main()