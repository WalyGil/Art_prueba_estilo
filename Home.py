import streamlit as st
import database_init  # Esto ya ejecutará init_database()

# Configura la página principal como una página de landing o redirección
st.set_page_config(
    page_title="Artistas De Mar Event Solutions", 
    page_icon="🎉",
    layout="centered"
)

# Aplicar estilos personalizados
st.markdown(
    """
    <style>
    .main {
        background-color: #FFFFFF;
    }
    .sidebar .sidebar-content {
        background-color: #F0F2F6;
    }
    .stButton>button {
        background-color: #F63366;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Bienvenido a Artistas De Mar")
st.write("Por favor, selecciona una opción en el menú lateral.")