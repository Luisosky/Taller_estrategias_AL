"""
Ejercicio 1 — Conteo de elementos menores (Small elements count)
================================================================
Para cada posición i del arreglo, cuenta cuántos elementos que están
a la derecha de arr[i] son estrictamente menores que arr[i].

Estrategia: Divide y Vencerás mediante MergeSort modificado.
  - Se ordenan los elementos de forma descendente.
  - Cuando v[i] > v[j] durante la combinación, TODOS los elementos
    desde j hasta h son menores que v[i], por lo que se suman de golpe.

Complejidad:
  - Tiempo: O(n log n)
  - Espacio: O(n)

Ejemplo:
  Entrada:  [5, 2, 6, 1, 3]
  Salida:   [3, 1, 2, 0, 0]
    → 5 tiene a su derecha: 2, 1, 3  → 3 menores
    → 2 tiene a su derecha: 1        → 1 menor
    → 6 tiene a su derecha: 1, 3     → 2 menores
    → 1 no tiene menores a su derecha
    → 3 no tiene menores a su derecha
"""

import os
import time

PAUSA = 0.05  # segundos entre pasos en la prueba de escritorio animada


# ══════════════════════════════════════════════════════════════════
#  LÓGICA PRINCIPAL
# ══════════════════════════════════════════════════════════════════

def combinar(v, ans, l, mid, h, pasos):
    """
    Combina las dos mitades [l..mid] y [mid+1..h] de v (ya ordenadas
    descendentemente) y actualiza ans con los conteos de menores.

    Parámetros:
        v    -- lista de pares (valor_original, índice_original)
        ans  -- arreglo de conteos que se va actualizando
        l    -- límite izquierdo del subarreglo actual
        mid  -- punto medio
        h    -- límite derecho del subarreglo actual
        pasos -- lista donde se registran los pasos para la prueba de escritorio
    """
    temporal = []
    i, j = l, mid + 1

    while i <= mid and j <= h:
        if v[i][0] > v[j][0]:
            # v[i] es mayor que todos los elementos desde j hasta h
            # (porque la mitad derecha también está ordenada desc.)
            cantidad = h - j + 1
            ans[v[i][1]] += cantidad

            pasos.append({
                'tipo': 'conteo',
                'l': l, 'mid': mid, 'h': h,
                'i': i, 'j': j,
                'val_i': v[i][0], 'idx_i': v[i][1],
                'val_j': v[j][0],
                'cantidad': cantidad,
                'ans': ans[:],
                'desc': (
                    f"v[{i}]={v[i][0]} > v[{j}]={v[j][0]}  "
                    f"→  ans[{v[i][1]}] += {cantidad}  "
                    f"(hay {cantidad} elemento(s) en [{j}..{h}] que son menores)"
                )
            })
            temporal.append(v[i])
            i += 1
        else:
            pasos.append({
                'tipo': 'pasar',
                'l': l, 'mid': mid, 'h': h,
                'i': i, 'j': j,
                'val_i': v[i][0], 'val_j': v[j][0],
                'ans': ans[:],
                'desc': (
                    f"v[{i}]={v[i][0]} ≤ v[{j}]={v[j][0]}  "
                    f"→  mover v[{j}]={v[j][0]} al arreglo temporal"
                )
            })
            temporal.append(v[j])
            j += 1

    # Copiar elementos restantes de la mitad izquierda
    while i <= mid:
        temporal.append(v[i])
        i += 1

    # Copiar elementos restantes de la mitad derecha
    while j <= h:
        temporal.append(v[j])
        j += 1

    # Poner los elementos de vuelta en v (orden descendente)
    for k, pos in enumerate(range(l, h + 1)):
        v[pos] = temporal[k]

    pasos.append({
        'tipo': 'combinar',
        'l': l, 'mid': mid, 'h': h,
        'v_actual': [x[0] for x in v],
        'ans': ans[:],
        'desc': f"Combinación completa del rango [{l}..{h}] — arreglo local ordenado descendente"
    })


def mergesort(v, ans, i, j, pasos):
    """
    MergeSort recursivo sobre v en el rango [i..j].
    Divide en mitades, ordena cada mitad y combina acumulando conteos.
    """
    if i < j:
        mid = (i + j) // 2

        pasos.append({
            'tipo': 'dividir',
            'l': i, 'mid': mid, 'h': j,
            'desc': (
                f"Dividir rango [{i}..{j}]  →  "
                f"izquierda [{i}..{mid}] | derecha [{mid+1}..{j}]"
            )
        })

        mergesort(v, ans, i, mid, pasos)
        mergesort(v, ans, mid + 1, j, pasos)
        combinar(v, ans, i, mid, j, pasos)
    else:
        pasos.append({
            'tipo': 'base',
            'l': i, 'h': j,
            'desc': f"Caso base: subarreglo de un solo elemento en posición {i} → valor {v[i][0]}"
        })


def construir_arreglo_menores(arr):
    """
    Función principal. Recibe un arreglo de enteros y devuelve
    (ans, pasos) donde:
      - ans[i] = cantidad de elementos a la derecha de arr[i] que son menores
      - pasos  = lista de diccionarios con el registro paso a paso
    """
    n = len(arr)
    # Crear pares (valor, índice_original) para no perder la posición
    v = [(arr[i], i) for i in range(n)]
    ans = [0] * n
    pasos = []

    pasos.append({
        'tipo': 'inicio',
        'arr': arr[:],
        'desc': f"Arreglo de entrada: {arr}  |  Crear pares (valor, índice): {v}"
    })

    mergesort(v, ans, 0, n - 1, pasos)

    pasos.append({
        'tipo': 'resultado',
        'arr': arr[:],
        'ans': ans[:],
        'desc': f"RESULTADO FINAL: {ans}"
    })

    return ans, pasos


# ══════════════════════════════════════════════════════════════════
#  PRUEBA DE ESCRITORIO EN CONSOLA
# ══════════════════════════════════════════════════════════════════

def separador(char='─', ancho=60):
    print(char * ancho)


def imprimir_arreglo_con_marcas(arr, l=None, h=None, i=None, j=None):
    """Imprime el arreglo resaltando los índices activos."""
    linea_vals  = "  Arreglo: [ "
    linea_marks = "  Marcas:  [ "

    for k, val in enumerate(arr):
        campo = f"{val:>3}"
        marca = "   "

        if i is not None and k == i:
            marca = " i "
        elif j is not None and k == j:
            marca = " j "
        elif l is not None and h is not None and l <= k <= h:
            marca = " · "

        linea_vals  += campo + "  "
        linea_marks += marca + "  "

    linea_vals  += "]"
    linea_marks += "]"
    print(linea_vals)
    print(linea_marks)


def prueba_escritorio(arr, pasos, modo_animado=False):
    """
    Muestra la prueba de escritorio paso a paso en la consola.
    Si modo_animado=True, imprime cada paso con una pausa breve.
    En modo interactivo (False), el usuario presiona Enter en cada paso.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    separador('═')
    print("  PRUEBA DE ESCRITORIO — Conteo de elementos menores")
    separador('═')
    print(f"  Arreglo de entrada : {arr}")
    print(f"  Tamaño             : {len(arr)}")
    separador()
    print()

    tabla_pasos = []  # Acumula filas para la tabla resumen final

    for num, paso in enumerate(pasos, 1):
        tipo = paso['tipo']
        desc = paso.get('desc', '')
        l    = paso.get('l')
        mid  = paso.get('mid')
        h    = paso.get('h')
        i_   = paso.get('i')
        j_   = paso.get('j')
        ans  = paso.get('ans', [])

        print(f"  Paso {num:>3}  [{tipo.upper():^10}]")
        separador('─', 50)
        print(f"  {desc}")
        print()

        if tipo in ('conteo', 'pasar', 'combinar', 'resultado'):
            imprimir_arreglo_con_marcas(arr, l, h, i_, j_)
            if ans:
                print(f"  ans actual : {ans}")
            print()

        if tipo == 'conteo':
            tabla_pasos.append((
                num, paso.get('l'), paso.get('mid'), paso.get('h'),
                paso.get('i'), paso.get('j'),
                f"ans[{paso.get('idx_i')}] += {paso.get('cantidad')}",
                str(ans)
            ))

        if tipo == 'resultado':
            separador('═')
            print()
            print("  ╔═══════════════════════════════════════════╗")
            print("  ║           RESULTADO FINAL                 ║")
            print("  ╠═══════════════════════════════════════════╣")
            for k, (val, cnt) in enumerate(zip(paso['arr'], paso['ans'])):
                print(f"  ║  arr[{k}] = {val:<4}  →  {cnt} elemento(s) menor(es) a la derecha  ║")
            print("  ╚═══════════════════════════════════════════╝")
            print()

        if modo_animado:
            time.sleep(PAUSA)
        else:
            entrada = input("  [Enter = siguiente paso | 'q' = saltar al final] ").strip().lower()
            if entrada == 'q':
                modo_animado = True  # Saltar al final automáticamente
                print()

    # Tabla resumen de conteos
    if tabla_pasos:
        print()
        separador('═')
        print("  TABLA RESUMEN DE CONTEOS")
        separador('═')
        print(f"  {'Paso':>5}  {'l':>3}  {'mid':>4}  {'h':>3}  {'i':>3}  {'j':>3}  {'Operación':<25}  {'ans'}")
        separador()
        for fila in tabla_pasos:
            num, l, mid, h, i, j, op, ans_str = fila
            print(f"  {num:>5}  {str(l):>3}  {str(mid):>4}  {str(h):>3}  {str(i):>3}  {str(j):>3}  {op:<25}  {ans_str}")
        separador()

    input("\n  Presiona Enter para volver al menú...")


# ══════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("=" * 60)
    print("  Ejercicio 1 — Conteo de elementos menores")
    print("  Estrategia: Divide y Vencerás (MergeSort modificado)")
    print("=" * 60)
    print()
    print("  Ingresa el arreglo de enteros separado por comas.")
    print("  Ejemplo: 5, 2, 6, 1, 3")
    print("  (Enter para usar el ejemplo por defecto)")
    print()
    entrada = input("  Arreglo: ").strip()

    if entrada == '':
        arr = [5, 2, 6, 1, 3]
    else:
        try:
            arr = [int(x.strip()) for x in entrada.split(',')]
        except ValueError:
            print("  Error: ingresa solo números enteros separados por comas.")
            input("  Presiona Enter para volver...")
            return

    print()
    print("  ¿Cómo quieres ver la prueba de escritorio?")
    print("  1. Interactivo (Enter en cada paso)")
    print("  2. Automático  (pausa breve entre pasos)")
    print()
    modo = input("  Modo [1/2]: ").strip()
    animado = (modo == '2')

    print()
    print("  Ejecutando algoritmo...")
    ans, pasos = construir_arreglo_menores(arr)

    prueba_escritorio(arr, pasos, modo_animado=animado)


if __name__ == '__main__':
    main()