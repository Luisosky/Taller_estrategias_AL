"""
Menú — Divide y Vencerás
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_dv():
    from divide_y_venceras.ejercicio1_elementos_menores import main as ej1
    from divide_y_venceras.ejercicio2_elemento_mayoritario import main as ej2

    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("   DIVIDE Y VENCERÁS")
        print("=" * 60)
        print()
        print("  1. Conteo de elementos menores  (MergeSort modificado)")
        print("  2. Elemento mayoritario          (Recursivo D&V)")
        print("  0. Volver al menú principal")
        print()
        opcion = input("  Elige una opción: ").strip()

        if opcion == '1':
            ej1()
        elif opcion == '2':
            ej2()
        elif opcion == '0':
            break
        else:
            print("\n  Opción no válida.")
            input("  Presiona Enter para continuar...")