import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(layout="wide", page_title="Dashboard de Temperaturas", initial_sidebar_state="expanded")
st.title("📊 Dashboard Interactivo de Temperaturas por Estación de Bombeo del 01-01-25 al 06-01-25")
st.markdown("<h3 style='text-align: center;'>Elaborado por Departamento de Confiabilidad de Cecuamaq, C.A.</h3>", unsafe_allow_html=True)
# Clasifica archivos según su nombre
def clasificar_archivos(archivos):
    estaciones = {"Estación 2": [], "Estación 5": [], "Estación 6": []}
    for archivo in archivos:
        nombre = archivo.name.upper()
        if "E2" in nombre:
            estaciones["Estación 2"].append(archivo)
        elif "E5" in nombre:
            estaciones["Estación 5"].append(archivo)
        elif "E6" in nombre:
            estaciones["Estación 6"].append(archivo)
    return estaciones

# Lee cada CSV
def leer_csv(archivo):
    df = pd.read_csv(archivo, delimiter=';')
    df.columns = ['DateTime', 'Temperatura']
    df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
    df['Temperatura'] = df['Temperatura'].astype(str).str.replace(',', '.').astype(float)
    return df

# Crea gráfico con líneas de alerta y leyenda debajo del eje X
def crear_grafico_interactivo(estacion, archivos):
    fig = go.Figure()

    for archivo in archivos:
        df = leer_csv(archivo)
        etiqueta = archivo.name.replace(".csv", "")
        fig.add_trace(go.Scatter(
            x=df["DateTime"],
            y=df["Temperatura"],
            mode='lines',
            name=etiqueta
        ))

    # Líneas de alerta
    fig.add_hline(
        y=60, line_dash="dash", line_color="yellow", line_width=3,
        annotation_text="A1: 60 °C", annotation_position="top left",
        annotation_font_color="yellow", annotation_bgcolor="black"
    )
    fig.add_hline(
        y=70, line_dash="dash", line_color="red", line_width=3,
        annotation_text="A2: 70 °C", annotation_position="top left",
        annotation_font_color="red", annotation_bgcolor="black"
    )

    # Configuración del layout con leyenda debajo del eje X
    fig.update_layout(
        title=f"{estacion} - Temperaturas",
        xaxis_title="Fecha",
        yaxis_title="Temperatura (°C)",
        yaxis=dict(range=[0, 90]),
        height=420,
        margin=dict(l=20, r=20, t=50, b=60),
        legend=dict(
            orientation="h",         # Horizontal
            yanchor="top", y=-0.35,  # Debajo del gráfico
            xanchor="center", x=0.5, # Centrada
            bgcolor="rgba(0,0,0,0)"  # Fondo transparente
        )
    )
    return fig

# Zona de carga con opción para ocultar
with st.expander("📂 Cargar archivos CSV"):
    archivos = st.file_uploader("Selecciona uno o más archivos", type=["csv"], accept_multiple_files=True)

# Mostrar gráficos si hay archivos
if archivos:
    estaciones = clasificar_archivos(archivos)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    for idx, nombre_estacion in enumerate(["Estación 2", "Estación 5", "Estación 6"]):
        archivos_estacion = estaciones[nombre_estacion]
        if archivos_estacion:
            fig = crear_grafico_interactivo(nombre_estacion, archivos_estacion)
            if idx == 0:
                with col1: st.plotly_chart(fig, use_container_width=True)
            elif idx == 1:
                with col2: st.plotly_chart(fig, use_container_width=True)
            else:
                with col3: st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Carga archivos CSV para visualizar los gráficos.")






