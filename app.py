import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_correct_warehouse(column_height, rafter_height, frame_spacing, num_frames, width):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Ajustar límites de la gráfica
    ax.set_xlim([0, (num_frames - 1) * frame_spacing])
    ax.set_ylim([0, width])
    ax.set_zlim([0, column_height + rafter_height])

    # Dibujar los pórticos individuales
    for i in range(num_frames):
        x_offset = i * frame_spacing

        # Columnas
        column1 = [(x_offset, 0, 0), (x_offset, 0, column_height)]
        column2 = [(x_offset, width, 0), (x_offset, width, column_height)]

        # Vigas inclinadas (techo a dos aguas)
        rafter_left = [(x_offset, 0, column_height), (x_offset, width / 2, column_height + rafter_height)]
        rafter_right = [(x_offset, width, column_height), (x_offset, width / 2, column_height + rafter_height)]

        # Dibujar elementos
        for element in [column1, column2, rafter_left, rafter_right]:
            x, y, z = zip(*element)
            ax.plot(x, y, z, color='red', linewidth=2)

        # Agregar vigas horizontales
        if i == 0 or i == num_frames - 1:
            horizontal_beam = [(x_offset, 0, column_height), (x_offset, width, column_height)]
            x, y, z = zip(*horizontal_beam)
            ax.plot(x, y, z, color='red', linewidth=2)

        # Conectar pórticos con vigas horizontales en la parte superior
        if i > 0:
            prev_x_offset = (i - 1) * frame_spacing
            beam1 = [(prev_x_offset, 0, column_height), (x_offset, 0, column_height)]
            beam2 = [(prev_x_offset, width, column_height), (x_offset, width, column_height)]
            beam3 = [(prev_x_offset, width / 2, column_height + rafter_height), (x_offset, width / 2, column_height + rafter_height)]

            for element in [beam1, beam2, beam3]:
                x, y, z = zip(*element)
                ax.plot(x, y, z, color='blue', linewidth=2)

    # Configurar etiquetas
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("Nave Industrial 3D")

    return fig

# Configuración de la interfaz en Streamlit
st.title("Simulación de una Nave Industrial 3D")

# Controles deslizantes
column_height = st.slider('Altura de Columnas', min_value=2, max_value=10, value=10, step=1)
rafter_height = st.slider('Altura de Vigas', min_value=1, max_value=5, value=5, step=1)
frame_spacing = st.slider('Espaciado de Pórticos', min_value=1, max_value=10, value=5, step=1)
num_frames = st.slider('Número de Pórticos', min_value=1, max_value=7, value=3, step=1)
width = st.slider('Ancho de la Nave', min_value=4, max_value=20, value=10, step=1)

# Generar y mostrar la gráfica
fig = plot_correct_warehouse(column_height, rafter_height, frame_spacing, num_frames, width)
st.pyplot(fig)
