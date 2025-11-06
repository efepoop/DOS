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
    page_title="Ferxxo Vibrascafes 💚",
    page_icon="🟢",
    layout="wide",
)

# ======================================
# ESTILO FEID / VIBRANT GREEN
# ======================================
STYLE = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Chakra+Petch:wght@500;700&family=Urbanist:wght@300;500;700&display=swap');
:root { --neon:#00FF6A; --ink:#051306; --ink-soft:#1b5c32; }

[data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #b6ffba 0%, #c8ffd6 40%, #eafff0 100%);
  color: var(--ink);
  font-family: 'Urbanist', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }

/* TÍTULOS */
h1 {
  font-family: 'Bebas Neue', sans-serif;
  text-align: center;
  font-size: clamp(54px, 7vw, 115px);
  color: #000;
  text-shadow: 0 0 25px rgba(0,255,106,.7), 0 0 55px rgba(0,255,106,.35);
}
h2, h3 {
  font-family: 'Chakra Petch', sans-serif;
  color: var(--ink-soft);
  letter-spacing: .8px;
}
.hr {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,255,106,.9), transparent);
  margin: 25px 0;
}

/* IMAGEN CENTRAL */
.stImage>img {
  display:block;
  margin:0 auto;
  border-radius:20px;
  border:4px solid var(--neon);
  box-shadow:0 0 18px rgba(0,255,106,.55), inset 0 0 10px rgba(0,255,106,.4);
  max-height:460px;
  object-fit:cover;
  transition: transform .3s ease;
}
.stImage>img:hover {
  transform: scale(1.02);
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
  padding: .8rem 1.6rem;
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
  background-color: rgba(255,255,255,.75) !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: rgba(230,255,240,.88);
  border-left: 3px solid var(--neon);
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# ======================================
# INTERFAZ PRINCIPAL
# ======================================
st.markdown("<h1>Ferxxo Vibrascafes 🔊</h1>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# Imagen portada
try:
    image = Image.open('ferquini2.jpg')  # 💚 Imagen actualizada
    st.image(image, width=400, caption="Ferxxo Vibrascafes · Green Mode 🌿")
except Exception:
    st.warning("Sube la imagen 'ferquini2.jpg' para mostrar la portada.")

with st.sidebar:
    st.header("🎧 Configuración Ferxxo")
    st.write("Escribe o selecciona un texto para escucharlo en **modo vibrascafé** 💚.")

# Crear carpeta temporal
os.makedirs("temp", exist_ok=True)

# ======================================
# TEXTO BASE
# ======================================
st.subheader("Una pequeña Fábula con Vibras 💫")
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
st.markdown("### ¿Quieres escucharlo en voz Ferxxo?")
text = st.text_area("💬 Escribe o pega aquí el texto que quieras escuchar:", "")

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
def text_to_speech(text, lg):
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
        result, output_text = text_to_speech(text, lg)
        audio_path = f"temp/{result}.mp3"
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()

        st.success("💚 ¡Tu audio Ferxxo está listo!")
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
st.caption("🌿 Ferxxo Vibrascafes — Green Neon Edition · Desarrollado con Streamlit y gTTS")
