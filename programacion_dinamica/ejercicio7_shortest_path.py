def min_cost_path(cost):
    """
    Encuentra el costo mínimo desde (0,0) hasta (m-1,n-1) 
    moviéndose a la derecha, abajo o en diagonal.
    Espacio optimizado a O(n).
    """
    if not cost or not cost[0]:
        return 0
        
    m, n = len(cost), len(cost[0])
    
    # En lugar de una matriz m*n, usamos un arreglo 1D de tamaño n
    dp = [0] * n
    
    # 1. Inicializamos la celda de origen
    dp[0] = cost[0][0]
    
    # 2. Inicializamos la primera fila (solo se puede llegar desde la izquierda)
    for j in range(1, n):
        dp[j] = dp[j-1] + cost[0][j]
        
    # 3. Procesamos el resto de las filas
    for i in range(1, m):
        # prev_diag almacena el valor de dp[i-1][j-1] antes de que se sobrescriba
        prev_diag = dp[0] 
        
        # La primera columna de la fila actual solo puede alcanzarse desde arriba
        dp[0] = dp[0] + cost[i][0]
        
        for j in range(1, n):
            temp = dp[j] # Guardamos el valor actual para que sea el prev_diag de la siguiente iteración (j+1)
            
            # dp[j] actual representa venir de arriba: (i-1, j)
            # dp[j-1] representa venir de la izquierda: (i, j-1)
            # prev_diag representa venir en diagonal: (i-1, j-1)
            dp[j] = min(dp[j], dp[j-1], prev_diag) + cost[i][j]
            
            # Actualizamos la diagonal para el siguiente paso
            prev_diag = temp
            
    return dp[n-1]

if __name__ == "__main__":
    # Prueba de escritorio
    grid = [
        [1, 2, 3],
        [4, 8, 2],
        [1, 5, 3]
    ]
    print("Costo mínimo (Grid):", min_cost_path(grid))
    # Salida esperada: 8 (Ruta: 1 -> 2 -> 2 -> 3)
