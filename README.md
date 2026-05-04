# Taller — Estrategias de Programación

Implementación en Python de los ejercicios del taller de estrategias algorítmicas.
Cada ejercicio incluye el algoritmo documentado y su **prueba de escritorio interactiva** en consola.

---

## Estructura del repositorio

```
taller_estrategias/
│
├── menu_principal.py                        ← Punto de entrada principal
│
├── divide_y_venceras/
│   ├── __init__.py
│   ├── menu_dv.py
│   ├── ejercicio1_elementos_menores.py      ← Conteo de elementos menores
│   └── ejercicio2_elemento_mayoritario.py   ← Elemento mayoritario
│
├── algoritmos_voraces/
│   └── __init__.py                          ← (próximamente)
│
└── programacion_dinamica/
    └── __init__.py                          ← (próximamente)
```

---

## Cómo ejecutar

### Menú principal (recomendado)
```bash
python menu_principal.py
```

### Ejecutar un ejercicio directamente
```bash
python divide_y_venceras/ejercicio1_elementos_menores.py
python divide_y_venceras/ejercicio2_elemento_mayoritario.py
```

> Requiere **Python 3.7+**. No tiene dependencias externas.

---

## Sección 1 — Divide y Vencerás

### Ejercicio 1 — Conteo de elementos menores

**Problema:** Para cada posición `i`, contar cuántos elementos a la derecha de `arr[i]` son estrictamente menores.

**Estrategia:** MergeSort modificado en orden descendente. Durante la combinación, cuando `v[i] > v[j]`, todos los elementos desde `j` hasta `h` son menores que `v[i]`, por lo que se suman de una sola vez.

| Complejidad | Valor |
|-------------|-------|
| Tiempo      | O(n log n) |
| Espacio     | O(n)  |

**Ejemplo:**
```
Entrada : [5, 2, 6, 1, 3]
Salida  : [3, 1, 2, 0, 0]
```

---

### Ejercicio 2 — Elemento mayoritario

**Problema:** Encontrar el elemento que aparece más de `n/2` veces en el arreglo.

**Estrategia:** Divide el arreglo en dos mitades recursivamente. El mayoritario global debe serlo en al menos una mitad. Al combinar, si los candidatos difieren, se cuenta cuál aparece más en el rango completo.

| Complejidad | Valor |
|-------------|-------|
| Tiempo      | O(n log n) |
| Espacio     | O(log n) — pila de recursión |

**Ejemplo:**
```
Entrada : [2, 2, 1, 1, 1, 2, 2]
Salida  : 2   (aparece 4 veces > 7/2 = 3.5)
```

---

Instalar requeriments

Y hacer lo siguiente 

```bash
source venv/bin/activate
streamlit run app.py

python -m venv venv
.\venv\Scripts\Activate
```