import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ======================================
# CONFIGURACIÓN BÁSICA
# ======================================
st.set_page_config(
    page_title="Ferxxo Vibrascafes ☕💚",
    page_icon="🟢",
    layout="wide",
)

# ======================================
# ESTILO FEID VIBRACOOL (VERDE + CAFÉ)
# ======================================
STYLE = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Chakra+Petch:wght@500;700&family=Urbanist:wght@300;500;700&display=swap');
:root { 
  --neon:#00FF6A; 
  --cafe:#5a3e2b; 
  --beige:#f4ede1; 
  --ink-soft:#2a6a44; 
}

/* FONDO Y FUENTE BASE */
[data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #e8fdee 0%, #f8f3ea 50%, #f6e8d4 100%);
  color: var(--cafe);
  font-family: 'Urbanist', sans-serif;
  padding-bottom: 60px;
}

[data-testid="stHeader"] {
  background: transparent;
}

/* TITULOS PRINCIPALES */
h1 {
  font-family: 'Bebas Neue', sans-serif;
  text-align: center;
  font-size: clamp(54px, 7vw, 115px);
  color: var(--cafe);
  text-shadow: 0 0 20px rgba(0,255,106,.6);
  letter-spacing: 1px;
}
h2, h3 {
  font-family: 'Chakra Petch', sans-serif;
  color: var(--ink-soft);
  letter-spacing: .8px;
}

.hr {
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--neon), transparent);
  margin: 20px 0;
}

/* IMAGEN CENTRAL */
.stImage>img {
  display:block;
  margin:0 auto;
  border-radius:22px;
  border:3px solid var(--neon);
  box-shadow:0 0 18px rgba(0,255,106,.5), 0 0 18px rgba(90,62,43,.3);
  max-height:440px;
  transition: transform .3s ease;
  object-fit:cover;
}
.stImage>img:hover {
  transform: scale(1.03);
}

/* TARJETAS CAFÉ */
.card {
  background: linear-gradient(180deg, #ffffffcc, #fff9f0dd);
  border: 1px solid rgba(0,255,106,.25);
  border-left: 6px solid var(--neon);
  border-radius: 14px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 8px 18px rgba(90,62,43,.1);
  margin-bottom: 1rem;
}

/* BOTÓN ESTILO FERXXO CAFÉ */
.stButton>button {
  background: linear-gradient(90deg, var(--cafe) 0%, #775740 100%) !important;
  color: var(--beige) !important;
  border: 2px solid var(--neon) !important;
  border-radius: 10px;
  font-family: 'Chakra Petch', sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  padding: .8rem 1.8rem;
  transition: transform .25s ease, box-shadow .25s ease;
}
.stButton>button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 25px rgba(0,255,106,.6);
}

/* TEXTAREA */
textarea {
  border-radius: 10px !important;
  border: 2px solid rgba(0,255,106,.4) !important;
  background-color: rgba(255,255,255,.9) !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: rgba(250,245,235,.92);
  border-left: 3px solid var(--neon);
  color: var(--cafe);
}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
  color: var(--cafe);
}

/* DESCARGA LINK */
a {
  font-family: 'Chakra Petch', sans-serif;
  color: var(--neon) !important;
  text-decoration: none;
}
a:hover {
  text-shadow: 0 0 10px rgba(0,255,106,.6);
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# ======================================
# INTERFAZ PRINCIPAL
# ======================================
st.markdown("<h1>Ferxxo Vibrascafes ☕💚</h1>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# IMAGEN DE PORTADA
try:
    image = Image.open('ferquini2.jpg')
    st.image(image, caption="Ferxxo Vibrascafes · Neon & Café Mood 🌿☕", use_container_width=True)
except Exception:
    st.warning("Sube la imagen 'ferquini2.jpg' para mostrar la portada.")

# ======================================
# SIDEBAR
# ======================================
with st.sidebar:
    st.header("🎧 Configuración Ferxxo")
    st.write("Escribe o selecciona un texto para escucharlo en voz humana con **vibras verdes y aroma a café** 💚☕.")

# Crear carpeta temporal
os.makedirs("temp", exist_ok=True)

# ======================================
# TEXTO BASE
# ======================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Una pequeña fábula")
st.markdown("""
> “¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño...  
> Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto,  
> y ahí en el rincón está la trampa sobre la cual debo pasar.  
> Todo lo que debes hacer es **cambiar de rumbo** —dijo el gato—... y se lo comió.”  
>  
> *Franz Kafka*
""")
st.markdown("</div>", unsafe_allow_html=True)

# ======================================
# ENTRADA DE TEXTO
# ======================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🎙️ Convierte tu texto en audio")
text = st.text_area("💬 Escribe o pega aquí el texto que quieras escuchar:", "")

option_lang = st.selectbox(
    "Selecciona el idioma de voz:",
    ("Español", "English")
)
lg = 'es' if option_lang == "Español" else 'en'
st.markdown("</div>", unsafe_allow_html=True)

# ======================================
# FUNCIÓN PRINCIPAL
# ======================================
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    file_name = text[:20].strip().replace(" ", "_") or "audio"
    path = f"temp/{file_name}.mp3"
    tts.save(path)
    return path

# ======================================
# BOTÓN DE CONVERSIÓN
# ======================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
if st.button("🎵 Convertir a Audio"):
    if not text.strip():
        st.warning("Por favor, escribe un texto para convertir.")
    else:
        audio_path = text_to_speech(text, lg)
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        st.success("💚 ¡Tu audio está listo!")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        bin_str = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(audio_path)}">⬇️ Descargar Audio</a>'
        st.markdown(href, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ======================================
# LIMPIEZA AUTOMÁTICA
# ======================================
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
remove_files(7)

# ======================================
# FOOTER
# ======================================
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.caption("☕ Ferxxo Vibrascafes — Café & Green Neon Edition · Desarrollado con Streamlit y gTTS")
