"""
Ejercicio 2 — Elemento mayoritario (Majority Element)
======================================================
Encuentra el elemento que aparece más de n/2 veces en un arreglo.

Estrategia: Divide y Vencerás recursivo.
  - Caso base: si el subarreglo tiene un solo elemento, ese es el
    candidato.
  - Paso recursivo: se divide el arreglo en dos mitades y se obtiene
    el candidato mayoritario de cada mitad.
  - Combinación: si ambos candidatos son iguales, ese es el mayoritario.
    Si son distintos, se cuenta cuál aparece más veces en el rango
    completo y ese gana.

Complejidad:
  - Tiempo: O(n log n)
  - Espacio: O(log n) por la pila de recursión

Ejemplo:
  Entrada:  [2, 2, 1, 1, 1, 2, 2]
  Salida:   2   (aparece 4 veces, 4 > 7/2 = 3.5)
"""

import os
import time

PAUSA = 0.08


# ══════════════════════════════════════════════════════════════════
#  LÓGICA PRINCIPAL
# ══════════════════════════════════════════════════════════════════

def contar_en_rango(nums, num, izq, der):
    """Cuenta cuántas veces aparece num en nums[izq..der]."""
    return sum(1 for k in range(izq, der + 1) if nums[k] == num)


def mayoritario_recursivo(nums, izq, der, profundidad, pasos):
    """
    Encuentra el candidato mayoritario en nums[izq..der] usando D&V.

    Parámetros:
        nums        -- arreglo de entrada (no se modifica)
        izq         -- índice izquierdo del subarreglo actual
        der         -- índice derecho del subarreglo actual
        profundidad -- nivel de recursión (0 = llamada inicial)
        pasos       -- lista donde se registran los pasos

    Retorna:
        El elemento candidato mayoritario en el rango [izq..der].
    """
    subarr = nums[izq:der + 1]
    sangria = "  " * profundidad  # Sangría visual por nivel de recursión

    # ── Caso base ──────────────────────────────────────────────
    if izq == der:
        pasos.append({
            'tipo': 'base',
            'izq': izq, 'der': der,
            'profundidad': profundidad,
            'subarreglo': subarr[:],
            'retorna': nums[izq],
            'cand_izq': None, 'cand_der': None,
            'cont_izq': None, 'cont_der': None,
            'desc': (
                f"{sangria}[Prof. {profundidad}] "
                f"Caso base: nums[{izq}] = {nums[izq]}  →  retorna {nums[izq]}"
            )
        })
        return nums[izq]

    # ── Dividir ────────────────────────────────────────────────
    mid = izq + (der - izq) // 2

    pasos.append({
        'tipo': 'dividir',
        'izq': izq, 'der': der, 'mid': mid,
        'profundidad': profundidad,
        'subarreglo': subarr[:],
        'desc': (
            f"{sangria}[Prof. {profundidad}] "
            f"Dividir {subarr}  →  "
            f"izq [{izq}..{mid}] = {nums[izq:mid+1]}  |  "
            f"der [{mid+1}..{der}] = {nums[mid+1:der+1]}"
        )
    })

    # ── Llamadas recursivas ────────────────────────────────────
    cand_izq = mayoritario_recursivo(nums, izq, mid, profundidad + 1, pasos)
    cand_der = mayoritario_recursivo(nums, mid + 1, der, profundidad + 1, pasos)

    # ── Combinar ───────────────────────────────────────────────
    if cand_izq == cand_der:
        pasos.append({
            'tipo': 'iguales',
            'izq': izq, 'der': der, 'mid': mid,
            'profundidad': profundidad,
            'subarreglo': subarr[:],
            'cand_izq': cand_izq, 'cand_der': cand_der,
            'cont_izq': None, 'cont_der': None,
            'retorna': cand_izq,
            'desc': (
                f"{sangria}[Prof. {profundidad}] "
                f"cand_izq={cand_izq} == cand_der={cand_der}  "
                f"→  ambas mitades coinciden, retorna {cand_izq}"
            )
        })
        return cand_izq

    cont_izq = contar_en_rango(nums, cand_izq, izq, der)
    cont_der = contar_en_rango(nums, cand_der, izq, der)
    retorna  = cand_izq if cont_izq > cont_der else cand_der

    pasos.append({
        'tipo': 'contar',
        'izq': izq, 'der': der, 'mid': mid,
        'profundidad': profundidad,
        'subarreglo': subarr[:],
        'cand_izq': cand_izq, 'cand_der': cand_der,
        'cont_izq': cont_izq, 'cont_der': cont_der,
        'retorna': retorna,
        'desc': (
            f"{sangria}[Prof. {profundidad}] "
            f"Contar en {subarr}:  "
            f"{cand_izq} aparece {cont_izq} vez/veces  |  "
            f"{cand_der} aparece {cont_der} vez/veces  "
            f"→  retorna {retorna}"
        )
    })

    return retorna


def elemento_mayoritario(nums):
    """
    Función pública. Recibe un arreglo y devuelve
    (resultado, pasos).
    """
    pasos = []
    pasos.append({
        'tipo': 'inicio',
        'desc': f"Arreglo de entrada: {nums}  |  n = {len(nums)}  |  umbral = n/2 = {len(nums)/2:.1f}"
    })

    resultado = mayoritario_recursivo(nums, 0, len(nums) - 1, 0, pasos)

    frecuencia = nums.count(resultado)
    pasos.append({
        'tipo': 'resultado',
        'resultado': resultado,
        'frecuencia': frecuencia,
        'n': len(nums),
        'desc': (
            f"RESULTADO FINAL: {resultado}  "
            f"(aparece {frecuencia} veces de {len(nums)}  →  "
            f"{frecuencia} > {len(nums)}/2 = {len(nums)/2:.1f})"
        )
    })

    return resultado, pasos


# ══════════════════════════════════════════════════════════════════
#  PRUEBA DE ESCRITORIO EN CONSOLA
# ══════════════════════════════════════════════════════════════════

def separador(char='─', ancho=65):
    print(char * ancho)


def imprimir_arreglo_resaltado(nums, izq=None, der=None, mayoritario=None):
    """
    Imprime el arreglo con el rango activo marcado.
    Si mayoritario está definido, resalta sus ocurrencias.
    """
    linea_vals  = "  Arreglo: [ "
    linea_marks = "           [ "

    for k, val in enumerate(nums):
        campo = f"{val:>3}"
        if mayoritario is not None and val == mayoritario:
            marca = " ★ "
        elif izq is not None and der is not None and izq <= k <= der:
            marca = " · "
        else:
            marca = "   "
        linea_vals  += campo + "  "
        linea_marks += marca + "  "

    print(linea_vals  + "]")
    print(linea_marks + "]  (· = rango activo, ★ = mayoritario)")


def imprimir_arbol_recursion(pasos):
    """Imprime una representación textual del árbol de recursión."""
    print()
    separador('═')
    print("  ÁRBOL DE RECURSIÓN (llamadas y retornos)")
    separador('═')
    print(f"  {'Prof.':>6}  {'izq':>4}  {'der':>4}  {'Subarreglo':<20}  {'Cand.izq':>9}  {'Cand.der':>9}  {'Retorna':>8}")
    separador()

    for paso in pasos:
        tipo = paso['tipo']
        if tipo not in ('base', 'iguales', 'contar'):
            continue
        prof  = paso.get('profundidad', '')
        izq   = paso.get('izq', '')
        der   = paso.get('der', '')
        sub   = str(paso.get('subarreglo', ''))
        ci    = str(paso.get('cand_izq', '—')) if paso.get('cand_izq') is not None else '—'
        cd    = str(paso.get('cand_der', '—')) if paso.get('cand_der') is not None else '—'
        ret   = paso.get('retorna', '')

        print(f"  {prof:>6}  {izq:>4}  {der:>4}  {sub:<20}  {ci:>9}  {cd:>9}  {ret:>8}")

    separador()


def prueba_escritorio(nums, pasos, modo_animado=False):
    """Muestra la prueba de escritorio en consola."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    separador('═')
    print("  PRUEBA DE ESCRITORIO — Elemento mayoritario")
    separador('═')
    print(f"  Arreglo de entrada : {nums}")
    print(f"  Tamaño             : {len(nums)}  |  umbral > {len(nums)/2:.1f}")
    separador()
    print()

    resultado_final = None

    for num, paso in enumerate(pasos, 1):
        tipo = paso['tipo']
        desc = paso.get('desc', '')

        print(f"  Paso {num:>3}  [{tipo.upper():^10}]")
        separador('─', 55)
        print(f"  {desc}")
        print()

        if tipo in ('dividir', 'base'):
            izq = paso.get('izq')
            der = paso.get('der')
            imprimir_arreglo_resaltado(nums, izq, der)
            print()

        if tipo in ('iguales', 'contar'):
            izq = paso.get('izq')
            der = paso.get('der')
            imprimir_arreglo_resaltado(nums, izq, der)
            ci = paso.get('cont_izq')
            cd = paso.get('cont_der')
            if ci is not None:
                print(f"  Conteo: {paso['cand_izq']} → {ci} vez/veces  |  {paso['cand_der']} → {cd} vez/veces")
            print()

        if tipo == 'resultado':
            resultado_final = paso['resultado']
            print()
            imprimir_arreglo_resaltado(nums, mayoritario=resultado_final)
            print()
            separador('═')
            print()
            print("  ╔════════════════════════════════════════════╗")
            print("  ║            RESULTADO FINAL                 ║")
            print("  ╠════════════════════════════════════════════╣")
            print(f"  ║  Elemento mayoritario : {resultado_final:<20}║")
            print(f"  ║  Frecuencia           : {paso['frecuencia']:<20}║")
            print(f"  ║  Umbral (n/2)         : {paso['n']/2:<20.1f}║")
            print(f"  ║  ¿Es mayoritario?     : {'Sí ✓':<20}║")
            print("  ╚════════════════════════════════════════════╝")
            print()

        if modo_animado:
            time.sleep(PAUSA)
        else:
            entrada = input("  [Enter = siguiente paso | 'q' = saltar al final] ").strip().lower()
            if entrada == 'q':
                modo_animado = True
                print()

    # Árbol de recursión al final
    imprimir_arbol_recursion(pasos)

    input("\n  Presiona Enter para volver al menú...")


# ══════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("=" * 60)
    print("  Ejercicio 2 — Elemento mayoritario")
    print("  Estrategia: Divide y Vencerás (recursivo)")
    print("=" * 60)
    print()
    print("  Ingresa el arreglo de enteros separado por comas.")
    print("  NOTA: debe existir un elemento que aparezca más de n/2 veces.")
    print("  Ejemplo: 2, 2, 1, 1, 1, 2, 2")
    print("  (Enter para usar el ejemplo por defecto)")
    print()
    entrada = input("  Arreglo: ").strip()

    if entrada == '':
        nums = [2, 2, 1, 1, 1, 2, 2]
    else:
        try:
            nums = [int(x.strip()) for x in entrada.split(',')]
        except ValueError:
            print("  Error: ingresa solo números enteros separados por comas.")
            input("  Presiona Enter para volver...")
            return

    # Verificar que existe elemento mayoritario
    from collections import Counter
    conteo = Counter(nums)
    mayor_elem, mayor_cnt = conteo.most_common(1)[0]
    if mayor_cnt <= len(nums) // 2:
        print()
        print(f"  ⚠ Advertencia: el elemento más frecuente ({mayor_elem}) "
              f"aparece solo {mayor_cnt} vez/veces.")
        print(f"  Para ser mayoritario necesita aparecer más de {len(nums)/2:.1f} veces.")
        print("  El algoritmo devolverá un candidato, pero puede no ser mayoritario real.")
        print()
        input("  Presiona Enter para continuar de todas formas...")

    print()
    print("  ¿Cómo quieres ver la prueba de escritorio?")
    print("  1. Interactivo (Enter en cada paso)")
    print("  2. Automático  (pausa breve entre pasos)")
    print()
    modo = input("  Modo [1/2]: ").strip()
    animado = (modo == '2')

    print()
    print("  Ejecutando algoritmo...")
    resultado, pasos = elemento_mayoritario(nums)

    prueba_escritorio(nums, pasos, modo_animado=animado)


if __name__ == '__main__':
    main()