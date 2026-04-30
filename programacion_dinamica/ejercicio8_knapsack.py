def knapsack(W, wt, val, n):
    """
    Resuelve el problema de la mochila 0/1 maximizando el valor
    sin fraccionar los objetos.
    """
    # Crear la tabla DP (n+1 filas x W+1 columnas) llena de ceros
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Construcción de la tabla
    for i in range(n + 1):
        for w in range(W + 1):
            # Caso base: 0 elementos o mochila con 0 de capacidad
            if i == 0 or w == 0:
                dp[i][w] = 0
            
            # Si el peso del elemento actual es menor o igual a la capacidad que estamos evaluando
            elif wt[i-1] <= w:
                # Maximizamos entre: (incluir el objeto) vs (NO incluir el objeto)
                dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]], dp[i-1][w])
            
            # Si el peso del objeto supera la capacidad, tomamos el valor anterior
            else:
                dp[i][w] = dp[i-1][w]
                
    return dp[n][W]

if __name__ == "__main__":
    # Prueba de escritorio con los datos del ejercicio
    # Items: A, B, C, D, E
    peso_w = [1, 3, 4, 5, 7]
    valor_v = [2, 5, 10, 14, 15]
    capacidad_W = 8
    n_elementos = len(valor_v)
    print("Ganancia máxima (Mochila 0/1):", knapsack(capacidad_W, peso_w, valor_v, n_elementos))
    # Salida esperada: 19 (Seleccionando B(3) + D(5) = Peso 8, Valor 5+14=19)
