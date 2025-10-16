import streamlit as st
import pandas as pd
import random
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Población en Lima Metropolitana", page_icon="👥", layout="wide")

st.title("👥 Monitoreo de la Población en Lima Metropolitana")

st.markdown(
    """
    Esta aplicación muestra un **análisis simulado** de la **población estimada**
    en los distritos de **Lima Metropolitana**.
    Se comparan los valores entre **2024 y 2025**, mostrando el crecimiento relativo
    de la población.
    """
)
st.write("---")

# --- DATOS SIMULADOS ---
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas",
    "San Juan de Lurigancho", "San Martín de Porres", "Villa El Salvador",
    "Ate", "Santiago de Surco", "Callao", "Los Olivos", "Chorrillos",
    "Surquillo", "Barranco", "Magdalena del Mar", "Pueblo Libre", "Jesús María",
    "Lince", "San Borja", "Breña", "San Miguel"
]

# Población simulada en miles de habitantes
poblacion_2024 = [random.randint(50, 1200) for _ in distritos]  # en miles
poblacion_2025 = [int(t * random.uniform(1.01, 1.05)) for t in poblacion_2024]  # crecimiento 1% a 5%

df = pd.DataFrame({
    "Distrito": distritos,
    "Población 2024 (miles)": poblacion_2024,
    "Población 2025 (miles)": poblacion_2025
})

df["Crecimiento Absoluto (miles)"] = df["Población 2025 (miles)"] - df["Población 2024 (miles)"]

df["Crecimiento Relativo (%)"] = np.where(
    df["Población 2024 (miles)"] != 0,
    ((df["Crecimiento Absoluto (miles)"] / df["Población 2024 (miles)"]) * 100).round(2),
    0
)

# --- MÉTRICAS GLOBALES ---
st.header("📊 Resumen General de la Población")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Promedio 2024", f"{df['Población 2024 (miles)'].mean():.0f} mil")
with col2:
    st.metric("Promedio 2025", f"{df['Población 2025 (miles)'].mean():.0f} mil")
with col3:
    st.metric("Crecimiento Promedio", f"{df['Crecimiento Relativo (%)'].mean():.2f}%",
              delta=f"{df['Crecimiento Relativo (%)'].mean():.2f}%")

st.write("---")

# --- VISUALIZACIÓN DE DATOS ---
st.header("📈 Comparativa de Población por Distrito")

df_chart = df.set_index("Distrito").sort_values(by="Población 2025 (miles)", ascending=False)

st.bar_chart(df_chart[["Población 2024 (miles)", "Población 2025 (miles)"]], use_container_width=True)

st.write("---")

# --- ANÁLISIS POR DISTRITO ---
st.header("🔍 Análisis Detallado por Distrito")
distrito_sel = st.selectbox("Selecciona un distrito para ver su evolución:", df["Distrito"])

if distrito_sel:
    fila = df[df["Distrito"] == distrito_sel].iloc[0]

    st.subheader(f"Datos para {distrito_sel}")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.metric("Población 2024", f"{fila['Población 2024 (miles)']} mil")
    with col_d2:
        st.metric("Población 2025", f"{fila['Población 2025 (miles)']} mil",
                  delta=f"{fila['Crecimiento Absoluto (miles)']} mil")
    with col_d3:
        st.metric("Crecimiento Relativo", f"{fila['Crecimiento Relativo (%)']}%",
                  delta=f"{fila['Crecimiento Relativo (%)']}%")

    st.subheader(f"Evolución en {distrito_sel}")
    st.progress(min(int((fila['Población 2025 (miles)'] / df['Población 2025 (miles)'].max()) * 100), 100))
    st.caption(f"La población estimada en {distrito_sel} alcanzó {fila['Población 2025 (miles)']} mil habitantes en 2025.")

st.write("---")

# --- TABLA DE DATOS COMPLETA ---
st.header("📋 Datos Completos")
st.write("Explora la tabla interactiva de todos los distritos.")

sortable_columns_options = [col for col in df.columns if col != "Distrito"]

sort_column = st.selectbox("Ordenar por:", options=sortable_columns_options, index=2)
sort_order = st.radio("Orden:", ("Ascendente", "Descendente"))

sorted_df = df.sort_values(by=sort_column, ascending=(sort_order == "Ascendente"))

st.dataframe(sorted_df, use_container_width=True)

st.write("---")
st.markdown("Desarrollado con ❤️ en Python y Streamlit")


