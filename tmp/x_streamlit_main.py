import streamlit as st
import app_00
import app_01
import app_02
import app_03

def main():
    st.set_page_config(page_title="App de Pestañas", layout="wide")
    
    # Crear pestañas
    tab0, tab1, tab2, tab3 = st.tabs(["Main", "Lector PDF", "Transcribir", "Chat IA"])
    
    with tab0:
        st.header("Menú principal")
        app_00.mostrar()

    with tab1:
        st.header("Lector de Facturas IA")
        app_01.mostrar()
        
    with tab2:
        st.header("Transcripción de reuniones IA")
        app_02.mostrar()
        
    with tab3:
        st.header("CHAT con IA (TdA)")
        app_03.mostrar()

if __name__ == "__main__":
    main()
