import os
from programacion_dinamica.ejercicio7_shortest_path import min_cost_path
from programacion_dinamica.ejercicio8_knapsack import knapsack

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_pd():
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("   PROGRAMACIÓN DINÁMICA")
        print("=" * 60)
        print("\n  7. Shortest Path in Grid (Costo Mínimo)")
        print("  8. Knapsack 0/1 (Problema de la Mochila)")
        print("  0. Volver al menú principal")
        
        opcion = input("\n  Seleccione una opción: ").strip()
        
        if opcion == "7":
            print("\n--- Shortest Path in Grid ---")
            grid = [
                [1, 2, 3],
                [4, 8, 2],
                [1, 5, 3]
            ]
            print("Matriz de costos:")
            for fila in grid:
                print(f"  {fila}")
            resultado = min_cost_path(grid)
            print(f"\nResultado: El costo mínimo es {resultado}")
            input("\nPresione Enter para continuar...")
            
        elif opcion == "8":
            print("\n--- Knapsack 0/1 ---")
            peso_w = [1, 3, 4, 5, 7]
            valor_v = [2, 5, 10, 14, 15]
            capacidad_W = 8
            n_elementos = len(valor_v)
            
            print(f"Pesos: {peso_w}")
            print(f"Valores: {valor_v}")
            print(f"Capacidad máxima: {capacidad_W}")
            
            resultado = knapsack(capacidad_W, peso_w, valor_v, n_elementos)
            print(f"\nResultado: La ganancia máxima es {resultado}")
            input("\nPresione Enter para continuar...")
            
        elif opcion == "0":
            break
        else:
            print("\nOpción no válida.")
            input("\nPresione Enter para intentar de nuevo...")

if __name__ == "__main__":
    menu_pd()
