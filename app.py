import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from pathlib import Path

APP_TITLE = "🪩 3D Pinball | Space Cadet"
PAGE_BG = "#3A6EA5"

if 'game_started' not in st.session_state:
    st.session_state.game_started = False

def get_base64_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

def get_file_content(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def encode_file_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="collapsed")

base_dir = Path(__file__).resolve().parent
mesa_img = get_base64_image(base_dir / "mesa.png")

st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"], .main {{
    background-color: {PAGE_BG} !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}}
.block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}
header[data-testid="stHeader"], .stDeployButton, footer, .stDecoration {{
    display: none !important;
}}
.game-header {{
    text-align: center;
    color: white;
    padding: 20px 0;
    background: {PAGE_BG};
}}
.game-title {{
    font-size: 48px;
    margin: 0 0 20px 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}}
.stButton > button {{
    padding: 15px 30px !important;
    font-size: 20px !important;
    font-weight: bold !important;
    color: white !important;
    background: linear-gradient(45deg, #0066CC, #0099FF) !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 15px rgba(0,100,200,0.3) !important;
}}
.game-content {{
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 200px);
    padding: 20px;
}}
.game-image {{
    max-width: 90vw;
    max-height: 70vh;
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="game-header"><h1 class="game-title">{APP_TITLE}</h1></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 INICIAR JOGO"):
        st.session_state.game_started = True
        st.rerun()

if st.session_state.game_started:
    html_file = base_dir / "index.html"
    
    if html_file.exists():
        html_content = get_file_content(html_file)
        
        if html_content:
            # Encontrar e incorporar todos os arquivos necessários
            js_files = []
            wasm_files = []
            
            # Procurar por arquivos JS e WASM no diretório
            for file_path in base_dir.glob("*.js"):
                js_content = get_file_content(file_path)
                if js_content:
                    js_files.append(js_content)
            
            for file_path in base_dir.glob("*.wasm"):
                wasm_b64 = encode_file_base64(file_path)
                if wasm_b64:
                    wasm_files.append((file_path.name, wasm_b64))
            
            # Criar HTML completo incorporando todos os recursos
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body, html {{
                        margin: 0;
                        padding: 0;
                        width: 100vw;
                        height: 100vh;
                        background: {PAGE_BG};
                        overflow: hidden;
                    }}
                    canvas {{
                        display: block;
                        margin: 0 auto;
                        max-width: 100%;
                        max-height: 100%;
                    }}
                </style>
            </head>
            <body>
                {html_content.split('<body>')[1].split('</body>')[0] if '<body>' in html_content else html_content}
                
                <script>
                // Função para carregar WASM a partir de base64
                function base64ToArrayBuffer(base64) {{
                    const binaryString = window.atob(base64);
                    const len = binaryString.length;
                    const bytes = new Uint8Array(len);
                    for (let i = 0; i < len; i++) {{
                        bytes[i] = binaryString.charCodeAt(i);
                    }}
                    return bytes.buffer;
                }}
                
                // Incorporar arquivos WASM
                {chr(10).join([f'window["{name}"] = base64ToArrayBuffer("{content}");' for name, content in wasm_files])}
                
                // Incorporar arquivos JS
                {chr(10).join(js_files)}
                </script>
            </body>
            </html>
            """
            
            components.html(full_html, height=750, scrolling=False)
        else:
            st.error("Erro ao ler index.html")
    else:
        st.error("Arquivo index.html não encontrado")
else:
    st.markdown(f"""
    <div class="game-content">
        {"<img src='data:image/png;base64," + mesa_img + "' class='game-image'>" if mesa_img else "<p style='color: white;'>Imagem não encontrada</p>"}
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: white; padding: 20px;">
💬 Por <strong>Ary Ribeiro</strong> | Fork da Alula | 
<a href="https://github.com/alula/SpaceCadetPinball/tree/gh-pages" style="color: white;">GitHub</a><br>
<em>Use o mouse para controlar</em>
</div>
""", unsafe_allow_html=True)