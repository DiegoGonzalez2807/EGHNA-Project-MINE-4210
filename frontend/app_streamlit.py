import streamlit as st
import streamlit.components.v1 as components
import requests
import time
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="EGHNA - Diagnóstico de Fibrosis Hepática",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

BACKEND_URL = "http://localhost:5000/predict"

# Colores por estadio
STAGE_COLORS = {
    "F0": "#10B981",
    "F1": "#06B6D4",
    "F2": "#F59E0B",
    "F3": "#F97316",
    "F4": "#EF4444"
}

STAGE_NAMES = {
    "F0": "Sin Fibrosis",
    "F1": "Fibrosis Leve",
    "F2": "Fibrosis Moderada",
    "F3": "Fibrosis Avanzada",
    "F4": "Cirrosis"
}

SEVERITY_POSITIONS = {
    "F0": 0,
    "F1": 25,
    "F2": 50,
    "F3": 75,
    "F4": 100
}

# CSS minimalista y profesional
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-primary: #0a0a0b;
        --bg-secondary: #111113;
        --bg-card: #18181b;
        --border: #27272a;
        --text-primary: #fafafa;
        --text-secondary: #a1a1aa;
        --accent: #6366f1;
        --accent-hover: #818cf8;
    }

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: var(--bg-primary);
    }

    #MainMenu, footer, header, .stDeployButton {
        display: none !important;
    }

    /* Header */
    .app-header {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
    }

    .app-logo {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.05em;
        margin: 0;
    }

    .app-logo span {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .app-description {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }

    /* Cards */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .card-title {
        color: var(--text-primary);
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .card-title i {
        color: var(--accent);
        font-size: 0.875rem;
    }

    /* Upload zone */
    .upload-zone {
        border: 2px dashed var(--border);
        border-radius: 8px;
        padding: 2rem 1rem;
        text-align: center;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .upload-zone:hover {
        border-color: var(--accent);
        background: rgba(99, 102, 241, 0.05);
    }

    .upload-icon {
        font-size: 2rem;
        color: var(--text-secondary);
        margin-bottom: 0.75rem;
    }

    .upload-text {
        color: var(--text-primary);
        font-size: 0.875rem;
        margin-bottom: 0.25rem;
    }

    .upload-hint {
        color: var(--text-secondary);
        font-size: 0.75rem;
    }

    /* Image preview */
    .image-container {
        background: var(--bg-secondary);
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }

    .stImage > img {
        border-radius: 6px !important;
        max-height: 200px !important;
        object-fit: contain !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: var(--accent-hover) !important;
        transform: translateY(-1px);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* File uploader styling */
    .stFileUploader {
        padding: 0 !important;
    }

    .stFileUploader > div {
        padding: 0 !important;
    }

    .stFileUploader label {
        display: none !important;
    }

    .stFileUploader section {
        padding: 0 !important;
    }

    .stFileUploader section > div {
        padding: 0 !important;
    }

    [data-testid="stFileUploader"] section {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    [data-testid="stFileUploadDropzone"] {
        background: transparent !important;
        border: 2px dashed var(--border) !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--accent) !important;
        background: rgba(99, 102, 241, 0.05) !important;
    }

    [data-testid="stFileUploadDropzone"] span {
        color: var(--text-secondary) !important;
    }

    [data-testid="stFileUploadDropzone"] button {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
    }

    /* Progress */
    .stProgress > div > div {
        background: var(--accent) !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-color: var(--accent) !important;
    }

    /* Result card styles */
    .result-container {
        text-align: center;
        padding: 1rem 0;
    }

    .result-stage {
        font-size: 4rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .result-name {
        font-size: 1.125rem;
        color: var(--text-primary);
        font-weight: 500;
        margin-bottom: 1.5rem;
    }

    .severity-track {
        width: 100%;
        height: 8px;
        background: linear-gradient(to right, #10B981, #06B6D4, #F59E0B, #F97316, #EF4444);
        border-radius: 4px;
        position: relative;
        margin-bottom: 1rem;
    }

    .severity-marker {
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 16px;
        height: 16px;
        background: white;
        border-radius: 50%;
        border: 3px solid var(--bg-primary);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .result-time {
        color: var(--text-secondary);
        font-size: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 1.5rem 0;
        color: var(--text-secondary);
        font-size: 0.75rem;
        border-top: 1px solid var(--border);
        margin-top: 2rem;
    }

    /* Alerts */
    .stAlert {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="app-header">
    <h1 class="app-logo"><span>EGHNA</span></h1>
    <p class="app-description">Sistema de Diagnóstico de Fibrosis Hepática</p>
</div>
""", unsafe_allow_html=True)

# Estado para controlar la vista
if 'result' not in st.session_state:
    st.session_state['result'] = None

# Vista de resultados
if st.session_state['result'] is not None:
    result = st.session_state['result']
    stage = result['stage']
    color = STAGE_COLORS.get(stage, "#6366f1")
    name = STAGE_NAMES.get(stage, "Desconocido")
    position = SEVERITY_POSITIONS.get(stage, 50)
    timestamp = result['timestamp']

    st.markdown(f"""
    <div class="card">
        <div class="card-title">
            <i class="fas fa-chart-pie"></i>
            Resultado del Análisis
        </div>
        <div class="result-container">
            <div class="result-stage" style="color: {color};">{stage}</div>
            <div class="result-name">{name}</div>
            <div class="severity-track">
                <div class="severity-marker" style="left: {position}%;"></div>
            </div>
            <div class="result-time">
                <i class="far fa-clock"></i>
                {timestamp}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Nuevo Análisis", use_container_width=True):
        st.session_state['result'] = None
        st.rerun()

# Vista de carga
else:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <i class="fas fa-microscope"></i>
            Análisis de Imagen
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Cargar imagen",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        # Contenedor para la imagen
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(uploaded_file, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Botón de análisis
        if st.button("Analizar Imagen", use_container_width=True):
            with st.spinner("Procesando..."):
                try:
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.006)
                        progress.progress(i + 1)
                    progress.empty()

                    img_bytes = uploaded_file.getvalue()
                    files = {"image": (uploaded_file.name, img_bytes, uploaded_file.type)}
                    resp = requests.post(BACKEND_URL, files=files)

                    if resp.status_code == 200:
                        data = resp.json()
                        fibrosis_stage = data.get("fibrosis_stage", "N/A")

                        st.session_state['result'] = {
                            'stage': fibrosis_stage,
                            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        }
                        st.rerun()
                    else:
                        st.error(f"Error del servidor: {resp.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("No se pudo conectar con el servidor")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Footer
st.markdown("""
<div class="app-footer">
    <i class="fas fa-info-circle"></i>
    Herramienta de apoyo diagnóstico. Consulte siempre con un profesional médico.
</div>
""", unsafe_allow_html=True)
