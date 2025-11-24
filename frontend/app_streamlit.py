import streamlit as st
import requests
import time
from datetime import datetime
import base64

# Configuración de la página
st.set_page_config(
    page_title="EGHNA AI - Diagnóstico Inteligente",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BACKEND_URL = "http://localhost:5000/predict"

# Información de los estadios de fibrosis
FIBROSIS_INFO = {
    "F0": {
        "nombre": "Sin Fibrosis",
        "color": "#00E676",
        "gradient": "linear-gradient(135deg, #00E676 0%, #76FF03 100%)",
        "icono": "✅",
        "emoji": "😊",
        "descripcion": "No hay evidencia de fibrosis hepática. El hígado se encuentra en estado saludable.",
        "severidad": 0,
        "nivel": "Excelente",
        "recomendacion": "Mantener hábitos saludables y realizar controles periódicos preventivos.",
        "color_texto": "#FFFFFF"
    },
    "F1": {
        "nombre": "Fibrosis Leve",
        "color": "#00BCD4",
        "gradient": "linear-gradient(135deg, #00BCD4 0%, #26C6DA 100%)",
        "icono": "ℹ️",
        "emoji": "🙂",
        "descripcion": "Fibrosis portal leve. Se observan cambios iniciales en el tejido hepático.",
        "severidad": 25,
        "nivel": "Leve",
        "recomendacion": "Control médico regular y adopción de hábitos de vida saludables.",
        "color_texto": "#FFFFFF"
    },
    "F2": {
        "nombre": "Fibrosis Moderada",
        "color": "#FFC107",
        "gradient": "linear-gradient(135deg, #FFC107 0%, #FFD54F 100%)",
        "icono": "⚠️",
        "emoji": "😐",
        "descripcion": "Fibrosis portal moderada con septos. Se observa progresión del daño hepático.",
        "severidad": 50,
        "nivel": "Moderado",
        "recomendacion": "Tratamiento médico y seguimiento especializado necesario.",
        "color_texto": "#FFFFFF"
    },
    "F3": {
        "nombre": "Fibrosis Avanzada",
        "color": "#FF6F00",
        "gradient": "linear-gradient(135deg, #FF6F00 0%, #FF8A65 100%)",
        "icono": "⚠️",
        "emoji": "😟",
        "descripcion": "Fibrosis avanzada con puentes. Se detecta daño significativo del tejido.",
        "severidad": 75,
        "nivel": "Avanzado",
        "recomendacion": "Tratamiento urgente y seguimiento médico estricto requerido.",
        "color_texto": "#FFFFFF"
    },
    "F4": {
        "nombre": "Cirrosis",
        "color": "#D32F2F",
        "gradient": "linear-gradient(135deg, #D32F2F 0%, #F44336 100%)",
        "icono": "🚨",
        "emoji": "😰",
        "descripcion": "Cirrosis establecida. Estadio más avanzado de fibrosis hepática.",
        "severidad": 100,
        "nivel": "Crítico",
        "recomendacion": "Atención médica especializada inmediata y tratamiento intensivo requerido.",
        "color_texto": "#FFFFFF"
    }
}

# CSS Ultra Moderno y Espectacular
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');

    /* Variables CSS */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --accent: #f093fb;
        --bg-dark: #0a0e27;
        --text-light: #ffffff;
    }

    /* Reset y estilos base */
    * {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        background-attachment: fixed;
    }

    /* Fondo animado con partículas */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(240, 147, 251, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(118, 75, 162, 0.15) 0%, transparent 50%);
        animation: backgroundShift 20s ease infinite;
        pointer-events: none;
        z-index: 0;
    }

    @keyframes backgroundShift {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.1) rotate(5deg); }
    }

    /* Header espectacular con glassmorphism */
    .hero-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 4rem 2rem;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow:
            0 20px 60px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        animation: heroFadeIn 1s ease-out;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: heroRotate 15s linear infinite;
    }

    @keyframes heroRotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    @keyframes heroFadeIn {
        from {
            opacity: 0;
            transform: translateY(-50px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .hero-header h1 {
        color: white;
        font-size: 4rem;
        font-weight: 900;
        margin: 0;
        text-shadow:
            0 0 20px rgba(255,255,255,0.5),
            0 5px 15px rgba(0,0,0,0.3);
        letter-spacing: -2px;
        position: relative;
        z-index: 1;
        animation: titlePulse 3s ease-in-out infinite;
    }

    @keyframes titlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    .hero-header .subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.4rem;
        margin-top: 1rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
        letter-spacing: 1px;
    }

    .hero-header .tagline {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        margin-top: 1rem;
        font-size: 0.9rem;
        color: white;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        z-index: 1;
    }

    /* Cards con glassmorphism y efectos 3D */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s;
    }

    .glass-card:hover::before {
        opacity: 1;
        animation: cardShine 2s linear infinite;
    }

    @keyframes cardShine {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow:
            0 25px 50px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
    }

    /* Upload zone espectacular */
    .upload-zone {
        background: rgba(102, 126, 234, 0.05);
        border: 3px dashed rgba(102, 126, 234, 0.5);
        border-radius: 25px;
        padding: 4rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }

    .upload-zone::before {
        content: '📤';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 8rem;
        opacity: 0.05;
        animation: uploadFloat 3s ease-in-out infinite;
    }

    @keyframes uploadFloat {
        0%, 100% { transform: translate(-50%, -50%) translateY(0); }
        50% { transform: translate(-50%, -50%) translateY(-20px); }
    }

    .upload-zone:hover {
        background: rgba(102, 126, 234, 0.15);
        border-color: rgba(240, 147, 251, 0.8);
        transform: scale(1.03);
        box-shadow:
            0 20px 40px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    /* Resultado card con animación espectacular */
    .result-mega-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(30px);
        border-radius: 30px;
        padding: 3rem;
        border: 2px solid;
        box-shadow:
            0 25px 60px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        animation: resultAppear 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }

    @keyframes resultAppear {
        from {
            opacity: 0;
            transform: scale(0.8) rotateY(-20deg);
        }
        to {
            opacity: 1;
            transform: scale(1) rotateY(0deg);
        }
    }

    .result-mega-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: resultSweep 3s ease-in-out infinite;
    }

    @keyframes resultSweep {
        0%, 100% { left: -100%; }
        50% { left: 100%; }
    }

    /* Medidor de severidad ultra moderno */
    .severity-container {
        margin: 2rem 0;
        position: relative;
    }

    .severity-meter {
        width: 100%;
        height: 40px;
        background: linear-gradient(to right,
            #00E676 0%,
            #00BCD4 25%,
            #FFC107 50%,
            #FF6F00 75%,
            #D32F2F 100%);
        border-radius: 50px;
        position: relative;
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.3),
            inset 0 2px 5px rgba(0, 0, 0, 0.2);
        overflow: hidden;
    }

    .severity-meter::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: meterShine 2s linear infinite;
    }

    @keyframes meterShine {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .severity-indicator {
        position: absolute;
        top: -15px;
        width: 6px;
        height: 70px;
        background: white;
        border: 3px solid #0a0e27;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
        transition: left 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        animation: indicatorPulse 2s ease-in-out infinite;
    }

    @keyframes indicatorPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }

    /* Stats boxes con efectos 3D */
    .stat-mega-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }

    .stat-mega-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
        opacity: 0;
        transition: opacity 0.4s;
    }

    .stat-mega-box:hover {
        transform: translateY(-15px) rotateX(5deg);
        box-shadow:
            0 30px 60px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }

    .stat-mega-box:hover::before {
        opacity: 1;
    }

    .stat-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: inline-block;
        animation: iconFloat 3s ease-in-out infinite;
    }

    @keyframes iconFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 1rem 0;
    }

    .stat-value {
        color: white;
        font-size: 0.95rem;
        font-weight: 300;
        line-height: 1.6;
    }

    /* Botón ultra moderno */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        padding: 1.5rem 2rem;
        font-size: 1.3rem;
        font-weight: 700;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow:
            0 10px 30px rgba(102, 126, 234, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow:
            0 20px 50px rgba(240, 147, 251, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    /* Badge ultra moderno */
    .ultra-badge {
        display: inline-block;
        padding: 0.8rem 1.8rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow:
            0 10px 25px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        animation: badgePulse 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }

    @keyframes badgePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Info card mejorada */
    .info-mega-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        color: white !important;
    }

    .info-mega-card:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }

    .info-mega-card h4 {
        color: white !important;
        margin-top: 0;
        font-size: 1.3rem;
        font-weight: 700;
    }

    .info-mega-card p {
        color: rgba(255, 255, 255, 0.95) !important;
        margin-bottom: 0;
        font-size: 1.1rem;
        line-height: 1.8;
    }

    /* Títulos */
    h1, h2, h3, h4, h5 {
        color: white !important;
    }

    /* Progress bar personalizado */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 100%;
        animation: progressGradient 2s ease infinite;
    }

    @keyframes progressGradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Footer moderno */
    .footer-mega {
        text-align: center;
        padding: 3rem 2rem;
        margin-top: 4rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .footer-mega p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0;
        font-size: 1rem;
    }

    .footer-mega strong {
        color: white;
        font-size: 1.2rem;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}

    /* File uploader personalizado */
    .stFileUploader {
        background: transparent !important;
    }

    /* Spinner personalizado */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* Success/Error/Info messages */
    .stSuccess, .stError, .stInfo {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Timestamp */
    .timestamp {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin-top: 2rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Header ultra espectacular
st.markdown("""
    <div class="hero-header">
        <h1>🏥 EGHNA AI</h1>
        <div class="subtitle">Diagnóstico Inteligente de Fibrosis Hepática</div>
        <div class="tagline">✨ Powered by Deep Learning & ResNet50 ✨</div>
    </div>
""", unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([1.3, 1], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📤 Cargar Imagen Médica")

    uploaded_file = st.file_uploader(
        "Arrastra o selecciona una imagen",
        type=["png", "jpg", "jpeg"],
        help="Formatos: PNG, JPG, JPEG | Tamaño recomendado: 224x224 o superior",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        st.markdown("#### 🖼️ Imagen Cargada")
        st.image(uploaded_file, use_container_width=True, caption=f"📁 {uploaded_file.name}")

        if st.button("🔬 ANALIZAR FIBROSIS", use_container_width=True):
            with st.spinner("🧠 Procesando con Inteligencia Artificial..."):
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # Animación de progreso con mensajes
                    messages = [
                        "Cargando modelo ResNet50...",
                        "Preprocesando imagen...",
                        "Analizando tejido hepático...",
                        "Calculando nivel de fibrosis...",
                        "Generando diagnóstico..."
                    ]

                    for i in range(100):
                        time.sleep(0.015)
                        progress_bar.progress(i + 1)
                        if i % 20 == 0:
                            status_text.text(messages[i // 20])

                    status_text.empty()

                    # Realizar predicción
                    img_bytes = uploaded_file.getvalue()
                    files = {
                        "image": (uploaded_file.name, img_bytes, uploaded_file.type)
                    }

                    resp = requests.post(BACKEND_URL, files=files)

                    if resp.status_code == 200:
                        data = resp.json()
                        fibrosis_stage = data.get("fibrosis_stage", "N/A")

                        if fibrosis_stage in FIBROSIS_INFO:
                            info = FIBROSIS_INFO[fibrosis_stage]
                            st.session_state['last_result'] = {
                                'stage': fibrosis_stage,
                                'info': info,
                                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            }
                            st.success("✅ Análisis completado con éxito")
                            st.balloons()
                            time.sleep(0.5)
                            st.rerun()
                    else:
                        st.error(f"❌ Error del servidor: {resp.status_code}")

                except Exception as e:
                    st.error("❌ Error al procesar la imagen")
                    st.exception(e)
    else:
        st.markdown("""
            <div class="upload-zone">
                <h2 style="color: rgba(255,255,255,0.9); font-size: 2rem; margin-bottom: 1rem;">
                    📁 Selecciona una Imagen
                </h2>
                <p style="color: rgba(255,255,255,0.7); font-size: 1.2rem; line-height: 1.8;">
                    Arrastra y suelta tu imagen médica aquí<br>
                    o haz clic para buscar en tu equipo
                </p>
                <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin-top: 1rem;">
                    Formatos soportados: PNG, JPG, JPEG
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Resultados del Análisis")

    if 'last_result' in st.session_state:
        result = st.session_state['last_result']
        stage = result['stage']
        info = result['info']

        # Card de resultado mega espectacular
        st.markdown(f"""
            <div class="result-mega-card" style="border-color: {info['color']};">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem;">
                    <div>
                        <div style="font-size: 5rem; margin-bottom: 0.5rem;">
                            {info['icono']} {info['emoji']}
                        </div>
                        <h2 style="color: {info['color']}; margin: 0; font-size: 3rem; font-weight: 900;">
                            {stage}
                        </h2>
                        <h3 style="color: white; margin: 0.5rem 0; font-size: 1.8rem; font-weight: 600;">
                            {info['nombre']}
                        </h3>
                    </div>
                    <div class="ultra-badge" style="background: {info['gradient']}; color: {info['color_texto']};">
                        {info['nivel']}
                    </div>
                </div>
                <p style="color: rgba(255,255,255,0.95); font-size: 1.15rem; line-height: 1.8; margin: 1.5rem 0;">
                    {info['descripcion']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Medidor de severidad ultra moderno
        st.markdown("#### 📈 Nivel de Severidad")
        st.markdown(f"""
            <div class="severity-container">
                <div class="severity-meter">
                    <div class="severity-indicator" style="left: {info['severidad']}%;"></div>
                </div>
                <div style="text-align: center; margin-top: 1rem;">
                    <span style="color: white; font-size: 2rem; font-weight: 700;">
                        {info['severidad']}%
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Recomendación con mejor contraste
        st.markdown(f"""
            <div class="info-mega-card" style="border-left-color: {info['color']}; background: {info['gradient']};">
                <h4 style="color: {info['color_texto']};">💡 Recomendación Médica</h4>
                <p style="color: {info['color_texto']} !important;">
                    {info['recomendacion']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Timestamp
        st.markdown(f"""
            <div class="timestamp">
                🕐 Análisis realizado el {result['timestamp']}
            </div>
        """, unsafe_allow_html=True)

    else:
        st.info("👈 Carga una imagen médica para comenzar el análisis")

        # Información de los estadios
        st.markdown("#### 📚 Clasificación de Fibrosis")
        for stage_key in ["F0", "F1", "F2", "F3", "F4"]:
            stage_info = FIBROSIS_INFO[stage_key]
            st.markdown(f"""
                <div class="info-mega-card" style="border-left-color: {stage_info['color']};">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 2rem;">{stage_info['icono']}</span>
                        <div>
                            <strong style="color: {stage_info['color']}; font-size: 1.3rem;">{stage_key}</strong>
                            <span style="color: rgba(255,255,255,0.8); font-size: 1.1rem;"> - {stage_info['nombre']}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Sección de características
st.markdown("---")
st.markdown('<div style="margin: 3rem 0;">', unsafe_allow_html=True)

col_feat1, col_feat2, col_feat3 = st.columns(3)

with col_feat1:
    st.markdown("""
        <div class="stat-mega-box">
            <div class="stat-icon">🎯</div>
            <div class="stat-label">Alta Precisión</div>
            <div class="stat-value">
                Modelo ResNet50 pre-entrenado<br>
                con arquitectura de Deep Learning<br>
                optimizada para imágenes médicas
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_feat2:
    st.markdown("""
        <div class="stat-mega-box">
            <div class="stat-icon">⚡</div>
            <div class="stat-label">Ultra Rápido</div>
            <div class="stat-value">
                Resultados en segundos<br>
                Procesamiento optimizado<br>
                con TensorFlow 2.20
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_feat3:
    st.markdown("""
        <div class="stat-mega-box">
            <div class="stat-icon">🔒</div>
            <div class="stat-label">100% Seguro</div>
            <div class="stat-value">
                Procesamiento local<br>
                Sin almacenamiento en nube<br>
                Privacidad garantizada
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer espectacular
st.markdown("""
    <div class="footer-mega">
        <p><strong>EGHNA AI - Sistema de Diagnóstico Inteligente</strong></p>
        <p>Powered by TensorFlow 2.20 & ResNet50 Deep Learning Architecture</p>
        <p style="margin-top: 1.5rem; font-size: 0.85rem; color: rgba(255,255,255,0.6);">
            ⚠️ Este sistema es una herramienta de apoyo diagnóstico basada en IA.
            <br>Los resultados deben ser siempre validados por un profesional médico certificado.
        </p>
        <p style="margin-top: 1rem; font-size: 0.9rem;">
            Desarrollado con ❤️ para la comunidad médica | © 2025
        </p>
    </div>
""", unsafe_allow_html=True)
