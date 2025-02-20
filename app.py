import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

st.set_page_config(layout="wide")

# Contenedor para la gráfica (para evitar el recálculo completo)
placeholder = st.empty()

with st.sidebar:
    st.header("Parámetros de la Nave")

    column_height = st.number_input("Altura de Columnas", min_value=1.0, max_value=15.0, value=4.0, step=0.1)
    rafter_height = st.number_input("Altura de Vigas", min_value=1.0, max_value=15.0, value=2.0, step=0.1)
    frame_spacing = st.number_input("Espaciado de Pórticos", min_value=1.0, max_value=15.0, value=5.0, step=0.1)
    num_frames = st.number_input("Número de Pórticos", min_value=1, max_value=15, value=3, step=1)
    width = st.number_input("Ancho de la Nave", min_value=1.0, max_value=25.0, value=10.0, step=0.1)

@st.cache_resource  # Cache para evitar recalcular gráficos repetitivos
def plot_correct_warehouse(column_height, rafter_height, frame_spacing, num_frames, width):
    fig = plt.figure(figsize=(6, 5))  # Reducir tamaño para mejorar rendimiento
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim([0, (num_frames - 1) * frame_spacing])
    ax.set_ylim([0, width])
    ax.set_zlim([0, column_height + rafter_height])

    # Forzar enteros en el eje X
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    def plot_element(ax, element, color='red'):
        """ Función auxiliar para dibujar líneas en la estructura """
        x, y, z = zip(*element)
        ax.plot(x, y, z, color=color, linewidth=2)

    for i in range(num_frames):
        x_offset = i * frame_spacing
        plot_element(ax, [(x_offset, 0, 0), (x_offset, 0, column_height)])
        plot_element(ax, [(x_offset, width, 0), (x_offset, width, column_height)])
        plot_element(ax, [(x_offset, 0, column_height), (x_offset, width / 2, column_height + rafter_height)])
        plot_element(ax, [(x_offset, width, column_height), (x_offset, width / 2, column_height + rafter_height)])

        if i == 0 or i == num_frames - 1:
            plot_element(ax, [(x_offset, 0, column_height), (x_offset, width, column_height)])

        if i > 0:
            prev_x_offset = (i - 1) * frame_spacing
            plot_element(ax, [(prev_x_offset, 0, column_height), (x_offset, 0, column_height)], color='blue')
            plot_element(ax, [(prev_x_offset, width, column_height), (x_offset, width, column_height)], color='blue')
            plot_element(ax, [(prev_x_offset, width / 2, column_height + rafter_height), (x_offset, width / 2, column_height + rafter_height)], color='blue')

    return fig

# Mostrar la gráfica en el contenedor sin redibujar toda la app
with placeholder:
    fig = plot_correct_warehouse(column_height, rafter_height, frame_spacing, num_frames, width)
    st.pyplot(fig)
