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

---

Instalar requeriments

Y hacer lo siguiente 

```bash
source venv/bin/activate
streamlit run app.py

python -m venv venv
.\venv\Scripts\Activate
```