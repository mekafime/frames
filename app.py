import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Ajustar ancho de la app para que se vea mejor
st.set_page_config(layout="wide")  # Hace que la app use todo el ancho de la pantalla

st.title("Nave Industrial 3D")

# Usar barra lateral para sliders y reducir el espacio en la UI
with st.sidebar:
    st.header("Parámetros de la Nave")

    column_height = st.number_input("Altura de Columnas", min_value=1, max_value=15, value=0, step=1)
    rafter_height = st.number_input("Altura de Vigas", min_value=1, max_value=15, value=0, step=1)
    frame_spacing = st.number_input("Espaciado de Pórticos", min_value=1, max_value=15, value=0, step=1)
    num_frames = st.number_input("Número de Pórticos", min_value=1, max_value=15, value=0, step=1)
    width = st.number_input("Ancho de la Nave", min_value=1, max_value=25, value=0, step=1)

def plot_correct_warehouse(column_height, rafter_height, frame_spacing, num_frames, width):
    fig = plt.figure(figsize=(8, 6))  # Reducir el tamaño del gráfico
    ax = fig.add_subplot(111, projection='3d')

    # Ajustar límites de la gráfica
    ax.set_xlim([0, (num_frames - 1) * frame_spacing])
    ax.set_ylim([0, width])
    ax.set_zlim([0, column_height + rafter_height])

    # Dibujar la estructura
    for i in range(num_frames):
        x_offset = i * frame_spacing

        # Columnas
        column1 = [(x_offset, 0, 0), (x_offset, 0, column_height)]
        column2 = [(x_offset, width, 0), (x_offset, width, column_height)]
        rafter_left = [(x_offset, 0, column_height), (x_offset, width / 2, column_height + rafter_height)]
        rafter_right = [(x_offset, width, column_height), (x_offset, width / 2, column_height + rafter_height)]

        for element in [column1, column2, rafter_left, rafter_right]:
            x, y, z = zip(*element)
            ax.plot(x, y, z, color='red', linewidth=2)

        if i == 0 or i == num_frames - 1:
            horizontal_beam = [(x_offset, 0, column_height), (x_offset, width, column_height)]
            x, y, z = zip(*horizontal_beam)
            ax.plot(x, y, z, color='red', linewidth=2)

        if i > 0:
            prev_x_offset = (i - 1) * frame_spacing
            beam1 = [(prev_x_offset, 0, column_height), (x_offset, 0, column_height)]
            beam2 = [(prev_x_offset, width, column_height), (x_offset, width, column_height)]
            beam3 = [(prev_x_offset, width / 2, column_height + rafter_height), (x_offset, width / 2, column_height + rafter_height)]

            for element in [beam1, beam2, beam3]:
                x, y, z = zip(*element)
                ax.plot(x, y, z, color='blue', linewidth=2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("")

    ax.view_init(elev=20, azim=-60)  # Ajusta la cámara para mejor visibilidad del eje Z
    ax.set_box_aspect([1, 1, 0.8])   # Mantiene proporción uniforme
    ax.grid(True)                     # Activa la cuadrícula

    return fig

# Mostrar la gráfica en la app
fig = plot_correct_warehouse(column_height, rafter_height, frame_spacing, num_frames, width)
st.pyplot(fig)
