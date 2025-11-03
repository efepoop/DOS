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
    page_title="Conversor Ferxxo 💚",
    page_icon="🟢",
    layout="wide",
)

# ======================================
# ESTILO FEID / FERXXO
# ======================================
STYLE = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Chakra+Petch:wght@500;700&family=Urbanist:wght@300;500;700&display=swap');
:root { --neon:#00FF6A; --ink:#061106; --ink-soft:#18582f; }

[data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #b6ffba 0%, #c6ffd3 45%, #e8fff0 100%);
  color: var(--ink);
  font-family: 'Urbanist', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }

/* TÍTULOS */
h1 {
  font-family: 'Bebas Neue', sans-serif;
  text-align: center;
  font-size: clamp(50px, 7vw, 110px);
  color: #000;
  text-shadow: 0 0 25px rgba(0,255,106,.7), 0 0 50px rgba(0,255,106,.35);
}
h2, h3, h4, h5 {
  font-family: 'Chakra Petch', sans-serif;
  color: var(--ink-soft);
  letter-spacing: .8px;
}
.hr {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,255,106,.9), transparent);
  margin: 20px 0;
}

/* IMAGEN CENTRAL */
.stImage>img {
  display:block;
  margin:0 auto;
  border-radius:16px;
  border:4px solid var(--neon);
  box-shadow:0 0 18px rgba(0,255,106,.55), inset 0 0 10px rgba(0,255,106,.4);
}

/* BOTONES ESTILO FEID */
.stButton>button {
  background: transparent !important;
  color: var(--neon) !important;
  border: 2px solid var(--neon) !important;
  border-radius: 12px;
  font-family: 'Chakra Petch', sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  padding: .7rem 1.6rem;
  transition: transform .2s ease, box-shadow .2s ease;
  animation: neonPulse 2.2s ease-in-out infinite;
}
.stButton>button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(0,255,106,.7);
}
@keyframes neonPulse {
  0% { box-shadow: 0 0 6px rgba(0,255,106,.3); }
  50% { box-shadow: 0 0 22px rgba(0,255,106,.7); }
  100% { box-shadow: 0 0 6px rgba(0,255,106,.3); }
}

/* TEXTAREA */
textarea {
  border-radius: 10px !important;
  border: 2px solid rgba(0,255,106,.4) !important;
  background-color: rgba(255,255,255,.7) !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: rgba(230,255,240,.85);
  border-left: 3px solid var(--neon);
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# ======================================
# INTERFAZ PRINCIPAL
# ======================================
st.markdown("<h1>Conversión de Texto a Audio</h1>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

try:
    image = Image.open('gato_raton.png')
    st.image(image, width=350, caption="Fábula del Gato y el Ratón · Kafka")
except Exception:
    st.warning("Sube la imagen 'gato_raton.png' para mostrar la portada.")

with st.sidebar:
    st.header("🎧 Configuración Ferxxo")
    st.write("Escribe o selecciona un texto para escucharlo en voz humana 💚.")

# Crear carpeta temporal
os.makedirs("temp", exist_ok=True)

# ======================================
# TEXTO BASE
# ======================================
st.subheader("Una pequeña Fábula")
st.markdown("""
> “¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño...  
> Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto,  
> y ahí en el rincón está la trampa sobre la cual debo pasar.  
> Todo lo que debes hacer es **cambiar de rumbo** —dijo el gato—... y se lo comió.”  
>  
> *Franz Kafka*
""")

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ======================================
# ENTRADA DE TEXTO
# ======================================
st.markdown("### ¿Quieres escucharlo en modo Ferxxo?")
text = st.text_area("💬 Escribe o pega aquí el texto que quieras escuchar:", "")

tld = 'com'
option_lang = st.selectbox(
    "Selecciona el idioma de voz:",
    ("Español", "English")
)

if option_lang == "Español":
    lg = 'es'
else:
    lg = 'en'

# ======================================
# FUNCIÓN PRINCIPAL
# ======================================
def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[:20].strip().replace(" ", "_")
        if not my_file_name:
            my_file_name = "audio"
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

# ======================================
# BOTÓN DE CONVERSIÓN
# ======================================
if st.button("🎵 Convertir a Audio"):
    if not text.strip():
        st.warning("Por favor, escribe un texto para convertir.")
    else:
        result, output_text = text_to_speech(text, 'com', lg)
        audio_path = f"temp/{result}.mp3"
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()

        st.success("¡Tu audio está listo! 💚")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Descargar archivo
        with open(audio_path, "rb") as f:
            data = f.read()

        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(audio_path)}">⬇️ Descargar Audio</a>'
        st.markdown(href, unsafe_allow_html=True)

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

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.caption("🌿 Ferxxo Translator — Green Neon Edition · Desarrollado con Streamlit y gTTS")
