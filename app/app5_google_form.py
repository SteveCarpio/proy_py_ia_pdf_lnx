import streamlit as st
import requests
from bs4 import BeautifulSoup
import ollama
import re
import urllib3
import pandas as pd

# 1 https://docs.google.com/forms/d/e/1FAIpQLSfKg4aOQDVqwPjuUkVm0XGhwHzRVFvgRcXHt1RS3Uxoz9OjRw/viewform

# 2 https://docs.google.com/forms/d/e/1FAIpQLSc7XsTh2z1SDekC17NmUuLZAcUMdJLNqwSFIgPPiPRV0v6GCQ/viewform

# 3 https://docs.google.com/forms/d/e/1FAIpQLSfcJHILLJciJAANJj4aiV2BoPZ1G7lnmKRtCFG40xZDhqGgRA/viewform

# 4 https://docs.google.com/forms/d/e/1FAIpQLSdtvuLq8sI6_HiVVCl8xmK96WhC36PiGobzVsFUy72N9OW2AQ/viewform

# 5 https://docs.google.com/forms/d/e/1FAIpQLSdh5fC64K_C14Ff-uUKStv0ChnAxrruUCjnpShrF6qh2VSXkA/viewform

# 6 https://docs.google.com/forms/d/e/1FAIpQLSfMvfzrvw9fHNpMn0ApZzdGi4nKoxFCFcRAD528W0yLnpJ1cA/viewform

# 7 https://docs.google.com/forms/d/e/1FAIpQLSeXer3wwpWP5HEvKXJxTQEyMvMWjoyQbY2YH1tn5J43R36txw/viewform

# 8 https://docs.google.com/forms/d/e/1FAIpQLSedtVjzdkbnD0PBLktBYrOfnZBsaM0Rt6GJyzzv6CpbsqDBuw/viewform



def main():

    # --- Configuración de página ---
    #st.set_page_config(page_title="Analizador de Formularios Google", layout="centered")

    st.title("📘 Analizador ")

    # --- SIDEBAR ---
    st.sidebar.title("⚙️ Selecciona un modelo")
    
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
    url = st.text_input("Introduce la URL :")
    procesar = st.button("Procesar")

    if procesar:
        if not url.strip():
            st.warning("⚠️ Por favor, introduce una URL válida.")
        else:
            st.info("Leyendo el formulario...")
            datos = []
            try:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                # Descargar HTML del formulario
                #resp = requests.get(url)
                resp = requests.get(url, verify=False, timeout=20)


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
                                #st.markdown(f"### {i}. {pregunta_limpia}")
                                #st.caption(f"{i}. {pregunta_limpia}")
                                st.caption(f"{pregunta_limpia}")
                                for letra, opcion in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", opciones):
                                    #st.write(f"**{letra})** {opcion}")
                                    st.write(f"{opcion}")

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

                                    datos.append((i, respuesta_texto)) 

                                    

                                except Exception as e:
                                    st.error(f"❌ No se pudo obtener respuesta del modelo '{modelo_seleccionado}': {e}")
                            else:
                                st.warning(f"⚠️ No se encontraron opciones para la pregunta {i}.")
            except Exception as e:
                st.error(f"❌ Ocurrió un error: {e}")


            # Mostrar resultado de todas las respuestas:
            st.write("---")
            st.write(" ")
            df = pd.DataFrame(datos, columns=['Índice', 'Respuesta'])
            st.write(df)



if __name__ == "__main__":
    main()
