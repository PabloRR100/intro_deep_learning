import streamlit as st
import os
import sys

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'script'))
sys.path.append(script_path)
from similarity_template import PokemonSimilarity
from PIL import Image
import requests
from io import BytesIO

# Título de la app
st.title("🔍 Encuentra el Pokémon más parecido")

# Inicializa el motor de similitud
@st.cache_resource
def get_engine():
    return PokemonSimilarity()

similarity_engine = get_engine()

# Subida de imagen o entrada de URL
option = st.radio("¿Cómo quieres subir la imagen?", ("Subir imagen", "Introducir URL"))

img = None

if option == "Subir imagen":
    uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Cargar la imagen desde el archivo subido
        bytes_data = uploaded_file.getvalue()
        try:
            img = Image.open(BytesIO(bytes_data)).convert("RGB")
        except Exception as e:
            st.error(f"Error al cargar la imagen: {e}")

    st.image(img, caption="Imagen cargada", use_container_width=True)
elif option == "Introducir URL":
    image_url = st.text_input("Introduce la URL de la imagen")
    img = image_url

 

# Mostrar la imagen y lanzar búsqueda
if img:
    

    if st.button("Buscar Pokémon más parecido"):
        with st.spinner("Buscando..."):
            result = similarity_engine.find_closest_pokemon(image_url if option == "Introducir URL" else uploaded_file)

            st.success(f"¡El Pokémon más parecido es: **{result}**!")
