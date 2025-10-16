import streamlit as st
import pandas as pd
import random
import numpy as np
import folium
from streamlit_folium import st_folium

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
st.write("---")

# --- DATOS SIMULADOS ---
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas",
    "San Juan de Lurigancho", "San Martín de Porres", "Villa El Salvador",
    "Ate", "Santiago de Surco", "Callao", "Los Olivos", "Chorrillos",
    "Surquillo", "Barranco", "Magdalena del Mar", "Pueblo Libre", "Jesús María",
    "Lince", "San Borja", "Breña", "San Miguel"
]

acceso_2024 = [random.randint(10, 85) for _ in distritos]
acceso_2025 = [min(t + random.randint(5, 15), 98) for t in acceso_2024]

df = pd.DataFrame({
    "Distrito": distritos,
    "Población con Acceso Tecnológico 2024 (%)": acceso_2024,
    "Población con Acceso Tecnológico 2025 (%)": acceso_2025
})

df["Incremento Absoluto (%)"] = (
    df["Población con Acceso Tecnológico 2025 (%)"] - df["Población con Acceso Tecnológico 2024 (%)"]
)

df["Incremento Relativo (%)"] = np.where(
    df["Población con Acceso Tecnológico 2024 (%)"] != 0,
    ((df["Incremento Absoluto (%)"] / df["Población con Acceso Tecnológico 2024 (%)"]) * 100).round(1),
    0
)

# --- MÉTRICAS GLOBALES ---
st.header("📊 Resumen General del Acceso Tecnológico")
col1, col2, col3 = st.columns(3)
with col1:
    prom2024 = df['Población con Acceso Tecnológico 2024 (%)'].mean()
    st.metric("Promedio 2024", f"{prom2024:.1f}%")
    st.progress(prom2024 / 100)
with col2:
    prom2025 = df['Población con Acceso Tecnológico 2025 (%)'].mean()
    st.metric("Promedio 2025", f"{prom2025:.1f}%")
    st.progress(prom2025 / 100)
with col3:
    inc_prom = df['Incremento Relativo (%)'].mean()
    st.metric("Incremento Promedio", f"{inc_prom:.1f}%", delta=f"{inc_prom:.1f}%")

st.write("---")

# --- VISUALIZACIÓN DE DATOS ---
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
        st.metric("Población con Acceso 2024", f"{fila['Población con Acceso Tecnológico 2024 (%)']:.1f}%")
    with col_d2:
        st.metric("Población con Acceso 2025", f"{fila['Población con Acceso Tecnológico 2025 (%)']:.1f}%",
                  delta=f"{fila['Incremento Absoluto (%)']:.1f} puntos")
    with col_d3:
        st.metric("Incremento Relativo", f"{fila['Incremento Relativo (%)']:.1f}%",
                  delta=f"{fila['Incremento Relativo (%)']:.1f}%")

    st.subheader(f"Progreso en Acceso Tecnológico en {distrito_sel}")
    st.progress(int(fila['Población con Acceso Tecnológico 2025 (%)']))
    st.caption(f"El porcentaje de población con acceso tecnológico en {distrito_sel} ha alcanzado un {fila['Población con Acceso Tecnológico 2025 (%)']:.1f}% en 2025.")

st.write("---")

# --- MAPA DE CALOR DE ACCESO TECNOLÓGICO ---
st.header("🗺️ Mapa de Calor del Acceso Tecnológico (2025)")

coords = {
    "Lima Cercado": (-12.0464, -77.0428),
    "Miraflores": (-12.1211, -77.0297),
    "San Isidro": (-12.0982, -77.0344),
    "La Molina": (-12.0833, -76.9333),
    "Comas": (-11.9364, -77.0622),
    "San Juan de Lurigancho": (-11.9941, -76.9983),
    "San Martín de Porres": (-11.9911, -77.0603),
    "Villa El Salvador": (-12.1972, -76.9361),
    "Ate": (-12.0293, -76.9348),
    "Santiago de Surco": (-12.1392, -76.9814),
    "Callao": (-12.0566, -77.1181),
    "Los Olivos": (-11.9565, -77.0697),
    "Chorrillos": (-12.1758, -77.0165),
    "Surquillo": (-12.1207, -77.0244),
    "Barranco": (-12.1496, -77.0219),
    "Magdalena del Mar": (-12.0933, -77.0667),
    "Pueblo Libre": (-12.0747, -77.0656),
    "Jesús María": (-12.0736, -77.0438),
    "Lince": (-12.0861, -77.0336),
    "San Borja": (-12.1022, -76.9944),
    "Breña": (-12.0561, -77.0497),
    "San Miguel": (-12.0889, -77.0797)
}

m = folium.Map(location=[-12.0464, -77.0428], zoom_start=11)

for _, row in df.iterrows():
    distrito = row["Distrito"]
    acceso = row["Población con Acceso Tecnológico 2025 (%)"]
    if distrito in coords:
        color = f"#{int(255 - acceso * 2):02x}{int(acceso * 2):02x}40"  # Rojo→Verde
        folium.CircleMarker(
            location=coords[distrito],
            radius=10,
            color=None,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{distrito}: {acceso:.1f}%",
        ).add_to(m)

st_data = st_folium(m, width=900, height=500)
st.caption("El color más verde indica mayor acceso tecnológico en 2025.")
st.write("---")

# --- GRÁFICA DE VARIACIÓN 2022–2025 ---
st.header("📅 Evolución del Acceso Tecnológico (2022–2025)")

df_variacion = pd.DataFrame({
    "Año": [2022, 2023, 2024, 2025],
    "Promedio Acceso (%)": [
        prom2024 - random.uniform(10, 15),
        prom2024 - random.uniform(5, 8),
        prom2024,
        prom2025
    ]
})

st.line_chart(df_variacion.set_index("Año"))
st.caption("Tendencia creciente del acceso tecnológico promedio en Lima Metropolitana (2022–2025).")

st.write("---")

# --- TABLA DE DATOS COMPLETA ---
st.header("📋 Datos Completos")
st.write("Explora la tabla interactiva de todos los distritos.")

sortable_columns_options = [col for col in df.columns if col != "Distrito"]
default_sort_index = sortable_columns_options.index("Incremento Relativo (%)") if "Incremento Relativo (%)" in sortable_columns_options else 0

sort_column = st.selectbox("Ordenar por:", options=sortable_columns_options, index=default_sort_index)
sort_order = st.radio("Orden:", ("Ascendente", "Descendente"))

sorted_df = df.sort_values(by=sort_column, ascending=(sort_order == "Ascendente"))
st.dataframe(sorted_df, use_container_width=True)

st.write("---")
st.markdown("Desarrollado con ❤️ en Python y Streamlit")

