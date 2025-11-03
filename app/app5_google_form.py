import streamlit as st
import requests
from bs4 import BeautifulSoup
import ollama
import re


def main():

    # --- Configuración de página ---
    st.set_page_config(page_title="Analizador de Formularios Google", layout="centered")

    st.title("📘 Analizador de Formularios de Google con Modelos Ollama")
    st.write("Introduce la URL de un formulario de Google Forms. La IA analizará las preguntas y sugerirá las respuestas correctas.")

    # --- SIDEBAR ---
    st.sidebar.title("⚙️ Configuración del modelo")
    st.sidebar.markdown("Selecciona el modelo local de Ollama:")

    # Puedes modificar o ampliar esta lista
    try:
        modelos_disponibles = [m["name"] for m in ollama.list()["models"]]
    except Exception:
        modelos_disponibles = ["tda-llama3", "tda-gpt20b"]

    modelo_seleccionado = st.sidebar.selectbox("Modelo Ollama", modelos_disponibles, index=0)
    temperatura = st.sidebar.slider("Creatividad del modelo (temperatura)", 0.0, 1.0, 0.3, 0.1)

    st.sidebar.markdown("---")
    st.sidebar.info(f"Modelo actual: **{modelo_seleccionado}**")

    # --- CUERPO PRINCIPAL ---
    url = st.text_input("Introduce la URL del formulario de Google Forms:")
    procesar = st.button("Procesar")

    if procesar:
        if not url.strip():
            st.warning("⚠️ Por favor, introduce una URL válida.")
        else:
            st.info("Leyendo el formulario...")

            try:
                # Descargar HTML del formulario
                resp = requests.get(url)
                if resp.status_code != 200:
                    st.error(f"No se pudo acceder al formulario (código {resp.status_code}).")
                else:
                    soup = BeautifulSoup(resp.text, 'html.parser')

                    # Intentar localizar las secciones de preguntas
                    preguntas_html = soup.find_all("div", class_="Qr7Oae")
                    if not preguntas_html:
                        st.warning("No se encontraron preguntas. Verifica que el formulario sea público.")
                    else:
                        st.success(f"✅ Se detectaron {len(preguntas_html)} preguntas en el formulario.")

                        for i, pregunta_html in enumerate(preguntas_html, 1):
                            # Extraer texto de la pregunta (más flexible)
                            pregunta_texto = None
                            posibles_campos = pregunta_html.find_all(["div", "span"])
                            for campo in posibles_campos:
                                texto = campo.get_text(strip=True)
                                if texto and len(texto.split()) > 3 and not texto.lower().startswith("1 punto"):
                                    pregunta_texto = texto
                                    break

                            if not pregunta_texto:
                                pregunta_texto = f"(No se pudo leer el texto de la pregunta {i})"

                            # Limpiar texto de pregunta
                            pregunta_limpia = re.sub(r"\s*\*\s*$", "", pregunta_texto.strip())

                            # Extraer opciones
                            opciones = [op.get_text(strip=True) for op in pregunta_html.find_all("div", class_="Y6Myld")]
                            if not opciones:
                                opciones = [op.get_text(strip=True) for op in pregunta_html.find_all("span", class_="aDTYNe")]

                            if opciones:
                                st.markdown(f"### {i}. {pregunta_limpia}")
                                for letra, opcion in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", opciones):
                                    st.write(f"**{letra})** {opcion}")

                                # Crear prompt para el modelo
                                prompt = f"""
    Eres un experto en cultura general, derecho y finanzas. 
    Selecciona la opción correcta para la siguiente pregunta.

    Pregunta: {pregunta_limpia}
    Opciones:
    {chr(10).join([f"{letra}) {op}" for letra, op in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', opciones)])}

    Indica SOLO la letra de la respuesta correcta (por ejemplo: 'B').
    """

                                try:
                                    respuesta = ollama.chat(
                                        model=modelo_seleccionado,
                                        messages=[{"role": "user", "content": prompt}],
                                        options={"temperature": temperatura},
                                    )
                                    respuesta_texto = respuesta["message"]["content"].strip()
                                    st.success(f"💡 Respuesta sugerida por {modelo_seleccionado}: **{respuesta_texto}**")
                                except Exception as e:
                                    st.error(f"❌ No se pudo obtener respuesta del modelo '{modelo_seleccionado}': {e}")
                            else:
                                st.warning(f"⚠️ No se encontraron opciones para la pregunta {i}.")
            except Exception as e:
                st.error(f"❌ Ocurrió un error: {e}")


if __name__ == "__main__":
    main()
