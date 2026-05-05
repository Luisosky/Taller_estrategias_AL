import sys

# Asegurar que la consola pueda imprimir caracteres especiales
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def format_matrix(matrix):
    """Formatea la matriz para imprimirla con corchetes y comas."""
    lines = []
    for row in matrix:
        # Convertir elementos a string, reemplazando None o 'x' adecuadamente
        row_str = ", ".join(str(x) if x != "x" else "x" for x in row)
        lines.append(f"    [{row_str}]")
    return "\n".join(lines)

def min_cost_path(cost):
    if not cost or not cost[0]:
        return
        
    m, n = len(cost), len(cost[0])
    dp = [["x" for _ in range(n)] for _ in range(m)]
    
    print("════════════════════════════════════════════════════════════")
    print("  PRUEBA DE ESCRITORIO — Ruta de Costo Mínimo (Grid DP)")
    print("════════════════════════════════════════════════════════════")
    print(f"  Matriz de entrada ({m}x{n}):")
    for row in cost:
        print(f"    {row}")
    print("  Movimientos evaluados: Derecha, Abajo, Diagonal (Abajo-Derecha)")
    print("────────────────────────────────────────────────────────────")
    print()

    # Paso 1: Inicio
    print("Paso   1  [  INICIO  ]")
    print("──────────────────────────────────────────────────")
    print("  Inicializar la matriz de memoria (DP) para guardar los costos acumulados.")
    dp[0][0] = cost[0][0]
    print(f"  Punto de partida en la esquina superior izquierda (0,0) → Costo = {dp[0][0]}")
    print("  Matriz DP actual:")
    print(format_matrix(dp))
    print()

    # Paso 2: Fila 0
    print("Paso   2  [  FILA 0  ]")
    print("──────────────────────────────────────────────────")
    print("  Llenar la primera fila. Solo se puede llegar a estas celdas moviéndose desde la izquierda:")
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + cost[0][j]
        print(f"    Celda (0,{j}) = dp[0][{j-1}] + {cost[0][j]}  →  {dp[0][j-1]} + {cost[0][j]} = {dp[0][j]}")
    print("  Matriz DP actual:")
    print(format_matrix(dp))
    print()

    # Paso 3 y 4: Resto de las filas
    for i in range(1, m):
        print(f"Paso   {i + 2}  [  FILA {i}  ]")
        print("──────────────────────────────────────────────────")
        print("  Llenar la fila calculando la ruta más barata (mínimo entre la celda de Arriba, Izquierda o Diagonal-Arriba) más el valor de la celda actual:")
        
        # Primera columna de la fila i
        dp[i][0] = dp[i-1][0] + cost[i][0]
        print(f"    Celda ({i},0) = (Viene de arriba) dp[{i-1}][0] + {cost[i][0]}  →  {dp[i-1][0]} + {cost[i][0]} = {dp[i][0]}")
        
        # Resto de la fila i
        for j in range(1, n):
            # Arriba, Izquierda, Diagonal
            val_arriba = dp[i-1][j]
            val_izq = dp[i][j-1]
            val_diag = dp[i-1][j-1]
            
            min_prev = min(val_arriba, val_izq, val_diag)
            dp[i][j] = min_prev + cost[i][j]
            
            print(f"    Celda ({i},{j}) = min(arriba:{val_arriba}, izq:{val_izq}, diagonal:{val_diag}) + {cost[i][j]}  →  {min_prev} + {cost[i][j]} = {dp[i][j]}")
            
        print("  Matriz DP actual:")
        print(format_matrix(dp))
        print()

    # Paso final: Resultado
    print(f"Paso   {m + 2}  [ RESULTADO ]")
    print("──────────────────────────────────────────────────")
    print(f"  El costo mínimo almacenado en la esquina inferior derecha dp[{m-1}][{n-1}] es {dp[m-1][n-1]}.")
    print()

    # RASTREO DE LA RUTA ÓPTIMA
    print("RASTREO DE LA RUTA ÓPTIMA:")
    print("  Para lograr este costo, el algoritmo hizo los siguientes saltos:")
    
    path = []
    curr_i, curr_j = m - 1, n - 1
    
    while curr_i > 0 or curr_j > 0:
        path.append((curr_i, curr_j))
        if curr_i > 0 and curr_j > 0:
            # Comparar para ver de dónde vino
            val_arriba = dp[curr_i-1][curr_j]
            val_izq = dp[curr_i][curr_j-1]
            val_diag = dp[curr_i-1][curr_j-1]
            
            min_val = min(val_arriba, val_izq, val_diag)
            
            # Prioridad de retroceso (puede haber empates, pero el ejemplo sugiere una ruta específica)
            # El ejemplo: (0,0) -> (0,1) -> (1,2) -> (2,2)
            # Inverso: (2,2) -> (1,2) -> (0,1) -> (0,0)
            # De (2,2) va a (1,2) (Arriba)
            # De (1,2) va a (0,1) (Diagonal)
            # De (0,1) va a (0,0) (Izquierda)
            
            if val_arriba == min_val:
                curr_i -= 1
            elif val_diag == min_val:
                curr_i -= 1
                curr_j -= 1
            else:
                curr_j -= 1
        elif curr_i > 0:
            curr_i -= 1
        else:
            curr_j -= 1
            
    path.append((0, 0))
    path.reverse()
    
    for idx, (r, c) in enumerate(path):
        if idx == 0:
            print(f"    1. Inicia en (0,0)  → Costo: {cost[0][0]}")
        else:
            prev_r, prev_c = path[idx-1]
            mov = ""
            if r > prev_r and c > prev_c:
                mov = "Mueve en Diagonal hasta"
            elif r > prev_r:
                mov = "Mueve Abajo hasta"
            else:
                mov = "Mueve a la Derecha hasta"
            
            print(f"    {idx + 1}. {mov} ({r},{c})  → Costo acumulado: {dp[prev_r][prev_c]} + {cost[r][c]} = {dp[r][c]}")

    print()
    return dp[m-1][n-1], path, dp

if __name__ == "__main__":
    grid = [
        [1, 2, 3],
        [4, 8, 2],
        [1, 5, 3]
    ]
    min_cost_path(grid)
