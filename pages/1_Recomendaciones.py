import streamlit as st
import sqlite3
import pandas as pd
import database_init  # Esto ya ejecutará init_database()

# Configuración específica para página de recomendaciones
st.set_page_config(
    page_title="Encuentra tu Proveedor Perfecto", 
    page_icon="🔍",
    layout="wide"
)

# Eliminar menú de Streamlit y otros elementos por defecto
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def obtener_recomendaciones(tipo_evento, num_invitados, presupuesto, estilo, ubicacion):
    conn = sqlite3.connect('proveedores.db')
    df = pd.read_sql_query("SELECT * FROM proveedores", conn)
    conn.close()
    
    # Filtrar por presupuesto
    df = df[df['precio_promedio'] <= presupuesto * 0.3]
    
    # Calcular score
    df['score'] = (
        df['puntuacion'] * 0.6 +
        (1 - (df['precio_promedio'] / (presupuesto * 0.3))) * 0.4
    )
    
    return df.nlargest(3, 'score')

def main():
    st.title("Encuentra los Mejores Proveedores para tu Evento")
    
    with st.form("recommendation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_evento = st.selectbox(
                "Tipo de Evento:",
                ["Boda", "Cumpleaños", "Evento Corporativo", "Fiesta"]
            )
            num_invitados = st.number_input("Número de Invitados:", min_value=1)
            presupuesto = st.number_input("Presupuesto Total (ARS):", min_value=0.0)
            
        with col2:
            estilo = st.selectbox(
                "Estilo del Evento:",
                ["Moderno", "Clásico", "Infantil", "Elegante"]
            )
            ubicacion = st.text_input("Ubicación:")
        
        submitted = st.form_submit_button("Obtener Recomendaciones")
        
        if submitted:
            recomendaciones = obtener_recomendaciones(
                tipo_evento, num_invitados, presupuesto, estilo, ubicacion
            )
            
            st.subheader("Proveedores Recomendados")
            for _, proveedor in recomendaciones.iterrows():
                with st.container():
                    st.markdown(f"""
                    ### {proveedor['nombre']}
                    - **Tipo:** {proveedor['tipo']}
                    - **Estilo:** {proveedor['estilo']}
                    - **Precio promedio:** ARS {proveedor['precio_promedio']}
                    - **Puntuación:** {proveedor['puntuacion']}/5
                    - **Ubicación:** {proveedor['ubicacion']}
                    - **Score de compatibilidad:** {proveedor['score']*100:.2f}%
                    """)
                    st.divider()

if __name__ == "__main__":
    main()