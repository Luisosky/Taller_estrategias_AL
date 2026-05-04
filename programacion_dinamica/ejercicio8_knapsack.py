import sys

# Asegurar que la consola pueda imprimir caracteres especiales
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def format_knapsack_table(dp, capacity, items_labels):
    """Formatea la tabla DP de la mochila para una visualización clara."""
    header = "Capacidad: " + "  ".join(f"{w:2}" for w in range(capacity + 1))
    lines = [header]
    lines.append("-" * len(header))
    
    for i, row in enumerate(dp):
        label = f"Item {items_labels[i-1]}" if i > 0 else "Base (0) "
        row_str = "  ".join(f"{val:2}" for val in row)
        lines.append(f"{label:9} | {row_str}")
    
    return "\n".join(lines)

def knapsack(W, wt, val, n=None, item_names=None):
    if n is None:
        n = len(val)
    if item_names is None:
        item_names = [chr(65 + i) for i in range(n)] # A, B, C...
        
    # Tabla DP inicializada con 0s
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    
    # Lógica de llenado
    
    print("════════════════════════════════════════════════════════════")
    print("  PRUEBA DE ESCRITORIO — Problema de la Mochila (0/1 DP)")
    print("════════════════════════════════════════════════════════════")
    print(f"  Capacidad máxima (W): {W}")
    print("  Objetos disponibles:")
    for i in range(n):
        print(f"    {item_names[i]}: Peso = {wt[i]}, Valor = {val[i]}")
    print("────────────────────────────────────────────────────────────")
    print()

    # Llenado de la tabla
    for i in range(1, n + 1):
        item_label = item_names[i-1]
        peso_actual = wt[i-1]
        valor_actual = val[i-1]
        
        print(f"Paso   {i}  [ ITEM {item_label} ]")
        print("──────────────────────────────────────────────────")
        print(f"  Evaluando el objeto {item_label} (P:{peso_actual}, V:{valor_actual}) para todas las capacidades:")
        
        for w in range(1, W + 1):
            if peso_actual <= w:
                # Opción 1: Incluir objeto
                inc = valor_actual + dp[i-1][w-peso_actual]
                # Opción 2: No incluir
                exc = dp[i-1][w]
                
                dp[i][w] = max(inc, exc)
                # Solo imprimimos detalles para capacidades clave o para entender la lógica
                if w == W or w == peso_actual:
                    print(f"    Capacidad {w}: max(Incluir: {valor_actual} + dp[{i-1}][{w-peso_actual}]={dp[i-1][w-peso_actual]}, Excluir: {exc}) = {dp[i][w]}")
            else:
                dp[i][w] = dp[i-1][w]
                if w == W:
                    print(f"    Capacidad {w}: Peso {peso_actual} excede capacidad {w}. Valor mantenido: {dp[i][w]}")

        print("\n  Tabla DP parcial:")
        print(format_knapsack_table(dp[:i+1], W, item_names))
        print()

    # Resultado final
    print("Paso FINAL [ RESULTADO ]")
    print("──────────────────────────────────────────────────")
    resultado = dp[n][W]
    print(f"  La ganancia máxima posible para una capacidad de {W} es: {resultado}")
    print()

    # RASTREO (Backtracking)
    print("RASTREO DE OBJETOS SELECCIONADOS:")
    print("  Revisamos desde la esquina inferior derecha para ver qué objetos sumaron valor:")
    
    selected_items = []
    curr_w = W
    for i in range(n, 0, -1):
        # Si el valor cambió respecto a la fila anterior, el objeto fue incluido
        if dp[i][curr_w] != dp[i-1][curr_w]:
            item_idx = i - 1
            selected_items.append(item_names[item_idx])
            print(f"    - Objeto {item_names[item_idx]} (Peso: {wt[item_idx]}, Valor: {val[item_idx]}) -> SELECCIONADO")
            curr_w -= wt[item_idx]
        else:
            print(f"    - Objeto {item_names[i-1]} -> NO seleccionado (el valor no aumentó)")
    
    print(f"\n  Resumen: {', '.join(reversed(selected_items))}")
    print(f"  Valor total: {resultado}")
    return resultado

if __name__ == "__main__":
    # Items: A, B, C, D, E
    nombres = ["A", "B", "C", "D", "E"]
    pesos = [1, 3, 4, 5, 7]
    valores = [2, 5, 10, 14, 15]
    capacidad = 8
    
    knapsack(capacidad, pesos, valores, item_names=nombres)
