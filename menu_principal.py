"""
Taller - Estrategias de Programación
=====================================
Menú principal para navegar entre las secciones del taller.

Secciones:
  1. Divide y Vencerás
  2. Algoritmos Voraces
  3. Programación Dinámica
"""

import os
import sys

# ── Añadir el directorio raíz al path para importaciones relativas ──
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def encabezado():
    print("=" * 60)
    print("   TALLER - ESTRATEGIAS DE PROGRAMACIÓN")
    print("=" * 60)


def menu_divide_y_venceras():
    from divide_y_venceras.menu_dv import menu_dv
    menu_dv()


def menu_voraces():
    print("\n  [Próximamente] Algoritmos Voraces\n")
    input("  Presiona Enter para volver...")


def menu_prog_dinamica():
    from programacion_dinamica.menu_pd import menu_pd
    menu_pd()


def menu_principal():
    while True:
        limpiar_pantalla()
        encabezado()
        print()
        print("  1. Divide y Vencerás")
        print("  2. Algoritmos Voraces         (próximamente)")
        print("  3. Programación Dinámica")
        print("  0. Salir")
        print()
        opcion = input("  Elige una opción: ").strip()

        if opcion == '1':
            menu_divide_y_venceras()
        elif opcion == '2':
            menu_voraces()
        elif opcion == '3':
            menu_prog_dinamica()
        elif opcion == '0':
            print("\n  ¡Hasta luego!\n")
            break
        else:
            print("\n  Opción no válida. Intenta de nuevo.")
            input("  Presiona Enter para continuar...")


if __name__ == '__main__':
    menu_principal()