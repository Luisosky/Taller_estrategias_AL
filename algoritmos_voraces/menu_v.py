"""
Menú — Algoritmos Voraces
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_v():
    from algoritmos_voraces.ejercicio3_convex_hull        import main as ej3
    from algoritmos_voraces.ejercicio4_devuelta_billetes  import main as ej4
    from algoritmos_voraces.ejercicio5_mochila_fraccion   import main as ej5
    from algoritmos_voraces.ejercicio6_kruskal_municipios import main as ej6

    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("   ALGORITMOS VORACES")
        print("=" * 60)
        print()
        print("  3. Convex Hull — Graham Scan")
        print("  4. Devuelta de billetes — Greedy")
        print("  5. Mochila fraccionaria — 3 heurísticas")
        print("  6. Red de municipios — Kruskal MST")
        print("  0. Volver al menú principal")
        print()
        opcion = input("  Elige una opción: ").strip()

        if opcion == '3':
            ej3()
        elif opcion == '4':
            ej4()
        elif opcion == '5':
            ej5()
        elif opcion == '6':
            ej6()
        elif opcion == '0':
            break
        else:
            print("\n  Opción no válida.")
            input("  Presiona Enter para continuar...")