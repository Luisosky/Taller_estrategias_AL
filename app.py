import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import numpy as np
import random

# Importar funciones de Divide y Vencerás
from divide_y_venceras.ejercicio1_elementos_menores import construir_arreglo_menores
from divide_y_venceras.ejercicio2_elemento_mayoritario import elemento_mayoritario

# Importar funciones de Algoritmos Voraces
from algoritmos_voraces.ejercicio3_convex_hull import graham_scan
from algoritmos_voraces.ejercicio4_devuelta_billetes import devuelta_greedy
from algoritmos_voraces.ejercicio5_mochila_fraccion import mochila_fraccionaria
from algoritmos_voraces.ejercicio6_kruskal_municipios import kruskal_mst

# Importar funciones de Programación Dinámica
from programacion_dinamica.ejercicio7_shortest_path import min_cost_path
from programacion_dinamica.ejercicio8_knapsack import knapsack

st.set_page_config(page_title="Algoritmos Interactivos", layout="wide", page_icon="🚀")

def set_custom_style():
    st.markdown("""
        <style>
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        h1, h2, h3 {
            color: #4CAF50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            border: None;
            padding: 10px 24px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

def parse_array(arr_str):
    try:
        return [int(x.strip()) for x in arr_str.split(",")]
    except ValueError:
        st.error("Formato inválido. Por favor, ingresa números enteros separados por comas.")
        return []

def render_home():
    st.title("Taller — Estrategias de Programación 💻")
    st.markdown("""
        Bienvenido a la aplicación interactiva para visualizar los algoritmos implementados.
        Usa el menú lateral para navegar por las diferentes estrategias y ejecutar los algoritmos con tus propios datos.
        
        ### Estrategias Disponibles:
        - **Divide y Vencerás**: Elementos menores a la derecha, Elemento Mayoritario.
        - **Algoritmos Voraces (Greedy)**: Convex Hull (Graham Scan), Devuelta de Billetes, Mochila Fraccional, MST Kruskal.
        - **Programación Dinámica**: Ruta de Costo Mínimo (Grid), Mochila 0/1.
    """)

def render_dv():
    st.header("Divide y Vencerás")
    ejercicio = st.selectbox("Selecciona un ejercicio", ["1. Elementos Menores a la Derecha", "2. Elemento Mayoritario"])
    
    if "Elementos Menores" in ejercicio:
        st.subheader("Conteo de Elementos Menores a la Derecha")
        st.write("Para cada posición, cuenta cuántos elementos a su derecha son estrictamente menores.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            arr_input = st.text_input("Arreglo (separado por comas):", "5, 2, 6, 1, 3")
        
        if st.button("Calcular Conteo"):
            arr = parse_array(arr_input)
            if arr:
                ans, pasos = construir_arreglo_menores(arr)
                st.success(f"Resultado: {ans}")
                
                # Visualización interactiva
                fig = go.Figure()
                fig.add_trace(go.Bar(x=[str(i) for i in arr], y=ans, name="Menores a la derecha", marker_color='#4CAF50'))
                fig.update_layout(title="Elementos vs. Cantidad de Menores", xaxis_title="Elemento", yaxis_title="Cantidad")
                st.plotly_chart(fig, use_container_width=True)

    elif "Elemento Mayoritario" in ejercicio:
        st.subheader("Búsqueda del Elemento Mayoritario")
        st.write("Encuentra el elemento que aparece más de N/2 veces en el arreglo.")
        
        arr_input = st.text_input("Arreglo (separado por comas):", "2, 2, 1, 1, 1, 2, 2")
        if st.button("Buscar Mayoritario"):
            arr = parse_array(arr_input)
            if arr:
                mayoritario, pasos = elemento_mayoritario(arr)
                if mayoritario is not None:
                    st.success(f"El elemento mayoritario es: {mayoritario}")
                else:
                    st.warning("No hay elemento mayoritario en el arreglo.")
                
                # Gráfico de frecuencias
                from collections import Counter
                counts = Counter(arr)
                fig = go.Figure([go.Bar(x=[str(k) for k in counts.keys()], y=list(counts.values()), marker_color='#2196F3')])
                fig.add_hline(y=len(arr)/2, line_dash="dash", line_color="red", annotation_text="N/2")
                fig.update_layout(title="Frecuencia de Elementos", xaxis_title="Elemento", yaxis_title="Frecuencia")
                st.plotly_chart(fig, use_container_width=True)

def render_voraces():
    st.header("Algoritmos Voraces (Greedy)")
    ejercicio = st.selectbox("Selecciona un ejercicio", ["3. Convex Hull", "4. Devuelta Billetes", "5. Mochila Fraccional", "6. Kruskal Municipios"])
    
    if "Convex Hull" in ejercicio:
        st.subheader("Convex Hull (Graham Scan)")
        st.write("Encuentra el polígono convexo más pequeño que contiene todos los puntos.")
        num_puntos = st.slider("Número de puntos aleatorios", 5, 50, 15)
        
        if st.button("Generar y Calcular"):
            # Generar puntos aleatorios
            puntos = [[random.randint(-20, 20), random.randint(-20, 20)] for _ in range(num_puntos)]
            pasos = []
            hull = graham_scan(puntos, pasos)
            
            if hull != [[-1]]:
                # Extraer coordenadas
                px = [p[0] for p in puntos]
                py = [p[1] for p in puntos]
                hx = [p[0] for p in hull] + [hull[0][0]]
                hy = [p[1] for p in hull] + [hull[0][1]]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=px, y=py, mode='markers', name='Puntos', marker=dict(color='blue', size=8)))
                fig.add_trace(go.Scatter(x=hx, y=hy, mode='lines+markers', name='Envolvente', line=dict(color='red', width=2)))
                fig.update_layout(title="Convex Hull Resultante", xaxis_title="X", yaxis_title="Y")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("No se pudo calcular la envolvente.")

    elif "Devuelta Billetes" in ejercicio:
        st.subheader("Problema de la Devuelta de Billetes")
        monto = st.number_input("Monto a entregar", min_value=1000, value=230000, step=1000)
        denominaciones = st.text_input("Denominaciones (separadas por coma)", "100000, 50000, 20000, 10000")
        disponibilidad = st.text_input("Disponibilidad por denominación", "5, 1, 2, 3")
        
        if st.button("Calcular Devuelta"):
            denoms = parse_array(denominaciones)
            disps = parse_array(disponibilidad)
            
            if len(denoms) == len(disps):
                pasos = []
                resultado, posible = devuelta_greedy(monto, denoms, disps, pasos)
                if posible:
                    st.success("Devuelta calculada correctamente.")
                    df = pd.DataFrame([
                        {"Denominación": d, "Cantidad": c, "Subtotal": d*c}
                        for d, c in resultado if c > 0
                    ])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("No hay suficientes billetes para dar la devuelta exacta.")
            else:
                st.error("El número de denominaciones no coincide con las disponibilidades.")

    elif "Mochila Fraccional" in ejercicio:
        st.subheader("Problema de la Mochila Fraccional")
        capacidad = st.number_input("Capacidad de la mochila", min_value=1.0, value=50.0)
        
        st.write("Ingresa los elementos como: peso,valor separados por punto y coma (ej. 10,60; 20,100; 30,120)")
        elementos_str = st.text_input("Elementos", "10,60; 20,100; 30,120")
        
        if st.button("Llenar Mochila"):
            try:
                # Parsear entrada
                elementos = []
                for i, p_v in enumerate(elementos_str.split(";")):
                    p, v = p_v.split(",")
                    elementos.append((f"Item {i+1}", 1, float(p.strip()), float(v.strip())))
                
                # Ejecutar algoritmo
                pasos = []
                valor_total, seleccion = mochila_fraccionaria(elementos, capacidad, 'ratio', pasos)
                st.success(f"Valor máximo obtenido: {valor_total:.2f}")
                
                df = pd.DataFrame([{
                    "Elemento": s[0],
                    "Fracción Usada": f"{s[1]*100:.1f}%",
                    "Peso Tomado": s[2],
                    "Valor Aportado": s[3]
                } for s in seleccion])
                
                st.dataframe(df, use_container_width=True)
                
                # Gráfico
                fig = go.Figure(data=[go.Pie(labels=[s[0] for s in seleccion], 
                                             values=[s[3] for s in seleccion], 
                                             hole=.3)])
                fig.update_layout(title="Distribución del Valor en la Mochila")
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"Error al procesar los datos: {e}")

    elif "Kruskal Municipios" in ejercicio:
        st.subheader("Árbol de Expansión Mínima (Kruskal)")
        st.write("Genera un grafo aleatorio y encuentra el MST.")
        num_nodos = st.slider("Número de Municipios (Nodos)", 3, 10, 5)
        
        if st.button("Generar MST"):
            # Crear nodos aleatorios
            nodos = [f"Mun_{i}" for i in range(num_nodos)]
            aristas = []
            # Crear aristas completas
            for i in range(num_nodos):
                for j in range(i+1, num_nodos):
                    # Distancia Aleatoria
                    dist = random.randint(5, 50)
                    aristas.append((i, j, dist))
            
            pasos = []
            costo_total, aristas_mst = kruskal_mst(nodos, aristas, pasos)
            
            # Dibujar con NetworkX y Plotly
            G = nx.Graph()
            posiciones = {i: (random.randint(0, 100), random.randint(0, 100)) for i in range(num_nodos)}
            for i, nombre in enumerate(nodos):
                G.add_node(nombre, pos=posiciones[i])
            
            for a in aristas:
                G.add_edge(nodos[a[0]], nodos[a[1]], weight=a[2])
                
            pos = nx.get_node_attributes(G, 'pos')
            
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                
            mst_edge_x = []
            mst_edge_y = []
            for a in aristas_mst:
                x0, y0 = pos[a[0]]
                x1, y1 = pos[a[1]]
                mst_edge_x.extend([x0, x1, None])
                mst_edge_y.extend([y0, y1, None])

            node_x = [pos[n][0] for n in G.nodes()]
            node_y = [pos[n][1] for n in G.nodes()]
            
            fig = go.Figure()
            # Aristas normales en gris
            fig.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines', name='Todas las rutas', hoverinfo='none'))
            # Aristas MST en rojo
            fig.add_trace(go.Scatter(x=mst_edge_x, y=mst_edge_y, line=dict(width=3, color='red'), mode='lines', name='MST (Kruskal)'))
            # Nodos
            fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=nodos, textposition="top center", marker=dict(size=10, color='blue'), name='Municipios'))
            
            fig.update_layout(title=f"Red de Municipios (Costo Total: {costo_total}M)", showlegend=True, xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            st.plotly_chart(fig, use_container_width=True)

def render_pd():
    st.header("Programación Dinámica")
    ejercicio = st.selectbox("Selecciona un ejercicio", ["7. Ruta de Costo Mínimo", "8. Mochila 0/1"])
    
    if "Ruta de Costo" in ejercicio:
        st.subheader("Ruta de Costo Mínimo (Grid)")
        st.write("Encuentra el costo mínimo para ir de la esquina superior izquierda a la inferior derecha.")
        
        grid_str = st.text_area("Grid de costos (filas separadas por nueva línea, columnas por coma)", "1, 2, 3\n4, 8, 2\n1, 5, 3")
        
        if st.button("Calcular Costo"):
            try:
                grid = []
                for row in grid_str.strip().split('\n'):
                    grid.append([int(x.strip()) for x in row.split(',')])
                
                costo, path, dp = min_cost_path(grid)
                st.success(f"El costo mínimo es: **{costo}**")
                
                m, n = len(grid), len(grid[0])
                path_set = set(path)
                
                # Construir matrices de color: celda en ruta = 1, el resto = 0
                z_highlight = [[0]*n for _ in range(m)]
                for (r, c) in path:
                    z_highlight[r][c] = 1
                
                # Texto de cada celda: costo original + costo acumulado dp
                cell_text = [[f"{grid[r][c]}<br><sub>dp={dp[r][c]}</sub>" for c in range(n)] for r in range(m)]
                
                # Colorscale: gris para celdas normales, verde para celdas en la ruta
                colorscale = [[0, '#2d2d3d'], [1, '#00c853']]
                
                fig = go.Figure()
                
                # Heatmap base con colores de ruta
                fig.add_trace(go.Heatmap(
                    z=z_highlight,
                    text=cell_text,
                    texttemplate="%{text}",
                    colorscale=colorscale,
                    showscale=False,
                    hovertemplate="Fila: %{y}<br>Columna: %{x}<br>Costo: %{customdata}<extra></extra>",
                    customdata=grid,
                    textfont=dict(size=14, color='white'),
                ))
                
                # Dibujar flechas de la ruta óptima
                path_x = [c for (r, c) in path]
                path_y = [r for (r, c) in path]
                
                fig.add_trace(go.Scatter(
                    x=path_x,
                    y=path_y,
                    mode='lines+markers',
                    line=dict(color='#ffeb3b', width=3, dash='solid'),
                    marker=dict(size=12, color='#ffeb3b', symbol='circle',
                                line=dict(width=2, color='#f57f17')),
                    name='Ruta Óptima',
                    hoverinfo='skip',
                ))
                
                # Marcar inicio y fin
                fig.add_trace(go.Scatter(
                    x=[path_x[0]], y=[path_y[0]],
                    mode='markers+text',
                    marker=dict(size=18, color='#00e676', symbol='star',
                                line=dict(width=2, color='white')),
                    text=['INICIO'], textposition='top center',
                    textfont=dict(color='#00e676', size=12),
                    name='Inicio',
                    hoverinfo='skip',
                ))
                fig.add_trace(go.Scatter(
                    x=[path_x[-1]], y=[path_y[-1]],
                    mode='markers+text',
                    marker=dict(size=18, color='#ff5252', symbol='star',
                                line=dict(width=2, color='white')),
                    text=['FIN'], textposition='bottom center',
                    textfont=dict(color='#ff5252', size=12),
                    name='Fin',
                    hoverinfo='skip',
                ))
                
                # Añadir anotaciones de flechas entre celdas consecutivas de la ruta
                for k in range(len(path) - 1):
                    r0, c0 = path[k]
                    r1, c1 = path[k+1]
                    fig.add_annotation(
                        x=c1, y=r1, ax=c0, ay=r0,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True,
                        arrowhead=3, arrowsize=1.5, arrowwidth=2,
                        arrowcolor='#ffeb3b',
                    )
                
                fig.update_layout(
                    title=f"Ruta de Costo Mínimo = {costo}",
                    xaxis=dict(
                        title="Columna", dtick=1, showgrid=False,
                        zeroline=False, constrain='domain',
                    ),
                    yaxis=dict(
                        title="Fila", dtick=1, showgrid=False,
                        zeroline=False, autorange='reversed', scaleanchor='x',
                    ),
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#0E1117',
                    font=dict(color='white'),
                    showlegend=True,
                    legend=dict(
                        orientation='h', yanchor='bottom', y=-0.2,
                        xanchor='center', x=0.5,
                    ),
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar los pasos de la ruta como texto
                st.markdown("#### 🛤️ Pasos de la Ruta Óptima")
                for idx, (r, c) in enumerate(path):
                    if idx == 0:
                        st.markdown(f"**{idx+1}.** Inicio en `({r},{c})` → Costo: `{grid[r][c]}`")
                    else:
                        prev_r, prev_c = path[idx-1]
                        if r > prev_r and c > prev_c:
                            mov = "↘️ Diagonal"
                        elif r > prev_r:
                            mov = "⬇️ Abajo"
                        else:
                            mov = "➡️ Derecha"
                        st.markdown(f"**{idx+1}.** {mov} hasta `({r},{c})` → Costo acumulado: `{dp[prev_r][prev_c]}` + `{grid[r][c]}` = `{dp[r][c]}`")
                
            except Exception as e:
                st.error(f"Error en el formato del grid: {e}")
                
    elif "Mochila 0/1" in ejercicio:
        st.subheader("Problema de la Mochila 0/1")
        capacidad = st.number_input("Capacidad W", min_value=1, value=8)
        pesos_str = st.text_input("Pesos (separados por coma)", "1, 3, 4, 5, 7")
        valores_str = st.text_input("Valores (separados por coma)", "2, 5, 10, 14, 15")
        
        if st.button("Calcular DP"):
            pesos = parse_array(pesos_str)
            valores = parse_array(valores_str)
            
            if len(pesos) == len(valores):
                ganancia = knapsack(capacidad, pesos, valores, len(valores))
                st.success(f"La ganancia máxima es: {ganancia}")
            else:
                st.error("La cantidad de pesos y valores debe ser igual.")

def main():
    set_custom_style()
    st.sidebar.title("Navegación 🧭")
    estrategia = st.sidebar.radio("Estrategia", ["Inicio", "Divide y Vencerás", "Algoritmos Voraces", "Programación Dinámica"])
    
    if estrategia == "Inicio":
        render_home()
    elif estrategia == "Divide y Vencerás":
        render_dv()
    elif estrategia == "Algoritmos Voraces":
        render_voraces()
    elif estrategia == "Programación Dinámica":
        render_pd()

if __name__ == "__main__":
    main()
