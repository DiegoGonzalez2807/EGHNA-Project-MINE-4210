import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000/predict"

st.title("Predicción de fibrosis hepática (EGHNA)")
st.write("Sube una imagen y el sistema te devolverá el estadio F0–F4.")

uploaded_file = st.file_uploader(
    "Sube la imagen (por ejemplo, elastografía, US, etc.)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Imagen cargada", use_column_width=True)

    if st.button("Analizar fibrosis"):
        try:
            img_bytes = uploaded_file.getvalue()

            files = {
                "image": (
                    uploaded_file.name,
                    img_bytes,
                    uploaded_file.type
                )
            }

            with st.spinner("Analizando imagen..."):
                resp = requests.post(BACKEND_URL, files=files)

            if resp.status_code == 200:
                data = resp.json()
                fibrosis_stage = data.get("fibrosis_stage", "N/A")
                st.success(f"Estadio de fibrosis predicho: **{fibrosis_stage}**")
            else:
                st.error(f"Error desde el backend: {resp.status_code}")
                st.write(resp.text)

        except Exception as e:
            st.error("Error al enviar la imagen al backend.")
            st.exception(e)
