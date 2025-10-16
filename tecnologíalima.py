import streamlit as st
import pandas as pd
import random
import numpy as np # Importamos numpy para operaciones matemáticas más robustas

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Tecnología en Lima Metropolitana", page_icon="💻", layout="wide")

st.title("💻 Monitoreo del Acceso Tecnológico en Lima Metropolitana")

st.markdown(
    """
    Esta aplicación muestra un **análisis simulado** del **porcentaje de población con acceso a tecnología**
    en los distritos de **Lima Metropolitana**.
    Se compara el acceso entre **2024 y 2025**, mostrando el incremento relativo
    en la adopción de herramientas tecnológicas y acceso a internet.
    """
)
st.write("---") # Separador visual

# --- DATOS SIMULADOS ---
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas",
    "San Juan de Lurigancho", "San Martín de Porres", "Villa El Salvador",
    "Ate", "Santiago de Surco", "Callao", "Los Olivos", "Chorrillos",
    "Surquillo", "Barranco", "Magdalena del Mar", "Pueblo Libre", "Jesús María",
    "Lince", "San Borja", "Breña", "San Miguel"
]
# Aseguramos que los valores sean porcentajes (entre 0 y 100)
# Nivel de acceso inicial en 2024
# Aseguramos que tec_2024 nunca sea cero para evitar la división por cero problemática
acceso_2024 = [random.randint(10, 85) for _ in distritos] # Mínimo 10 para evitar 0
# Nivel de acceso en 2025, con un incremento, sin superar 100
acceso_2025 = [min(t + random.randint(5, 15), 98) for t in acceso_2024] # Incremento más moderado y límite de 98% para realismo

df = pd.DataFrame({
    "Distrito": distritos,
    "Población con Acceso Tecnológico 2024 (%)": acceso_2024,
    "Población con Acceso Tecnológico 2025 (%)": acceso_2025
})

df["Incremento Absoluto (%)"] = df["Población con Acceso Tecnológico 2025 (%)"] - df["Población con Acceso Tecnológico 2024 (%)"]

# --- CORRECCIÓN DE LA DIVISIÓN POR CERO ---
# Calculamos el incremento relativo de forma vectorizada usando np.where para evitar la división por cero
# Si el denominador es 0, el resultado es 0; de lo contrario, se realiza la división
df["Incremento Relativo (%)"] = np.where(
    df["Población con Acceso Tecnológico 2024 (%)"] != 0,
    ((df["Incremento Absoluto (%)"] / df["Población con Acceso Tecnológico 2024 (%)"]) * 100).round(1),
    0 # Si el denominador es 0, el incremento relativo es 0
)


# --- MÉTRICAS GLOBALES ---
st.header("📊 Resumen General del Acceso Tecnológico")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Promedio 2024", f"{df['Población con Acceso Tecnológico 2024 (%)'].mean():.1f}%")
    st.progress(df['Población con Acceso Tecnológico 2024 (%)'].mean() / 100)
with col2:
    st.metric("Promedio 2025", f"{df['Población con Acceso Tecnológico 2025 (%)'].mean():.1f}%")
    st.progress(df['Población con Acceso Tecnológico 2025 (%)'].mean() / 100)
with col3:
    st.metric("Incremento Promedio", f"{df['Incremento Relativo (%)'].mean():.1f}%",
              delta=f"{df['Incremento Relativo (%)'].mean():.1f}%")

st.write("---")

# --- VISUALIZACIÓN DE DATOS con st.bar_chart ---
st.header("📈 Comparativa del Porcentaje de Población con Acceso Tecnológico por Distrito")

df_chart = df.set_index("Distrito").sort_values(by="Población con Acceso Tecnológico 2025 (%)", ascending=False)

st.bar_chart(df_chart[["Población con Acceso Tecnológico 2024 (%)", "Población con Acceso Tecnológico 2025 (%)"]], use_container_width=True)

st.write("---")

# --- ANÁLISIS POR DISTRITO ---
st.header("🔍 Análisis Detallado por Distrito")
distrito_sel = st.selectbox("Selecciona un distrito para ver su evolución:", df["Distrito"])

if distrito_sel:
    fila = df[df["Distrito"] == distrito_sel].iloc[0]

    st.subheader(f"Datos para {distrito_sel}")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.metric(
            label="Población con Acceso 2024",
            value=f"{fila['Población con Acceso Tecnológico 2024 (%)']:.1f}%"
        )
    with col_d2:
        st.metric(
            label="Población con Acceso 2025",
            value=f"{fila['Población con Acceso Tecnológico 2025 (%)']:.1f}%",
            delta=f"{fila['Incremento Absoluto (%)']:.1f} puntos"
        )
    with col_d3:
        st.metric(
            label="Incremento Relativo",
            value=f"{fila['Incremento Relativo (%)']:.1f}%",
            delta=f"{fila['Incremento Relativo (%)']:.1f}%"
        )

    # Gráfico de progreso para el distrito seleccionado
    st.subheader(f"Progreso en Acceso Tecnológico en {distrito_sel}")
    st.progress(int(fila['Población con Acceso Tecnológico 2025 (%)']))
    st.caption(f"El porcentaje de población con acceso tecnológico en {distrito_sel} ha alcanzado un {fila['Población con Acceso Tecnológico 2025 (%)']:.1f}% en 2025.")

st.write("---")

# --- TABLA DE DATOS COMPLETA ---
st.header("📋 Datos Completos")
st.write("Explora la tabla interactiva de todos los distritos.")

# Columnas disponibles para ordenar (excluyendo "Distrito")
sortable_columns_options = [col for col in df.columns if col != "Distrito"]

# Determinar el índice predeterminado.
try:
    default_sort_index = sortable_columns_options.index("Incremento Relativo (%)")
except ValueError:
    default_sort_index = 0

sort_column = st.selectbox(
    "Ordenar por:",
    options=sortable_columns_options,
    index=default_sort_index
)
sort_order = st.radio("Orden:", ("Ascendente", "Descendente"))

sorted_df = df.sort_values(by=sort_column, ascending=(sort_order == "Ascendente"))

st.dataframe(sorted_df, use_container_width=True)

# Puedes añadir un pie de página
st.write("---")
st.markdown("Desarrollado con ❤️ en Python y Streamlit")
