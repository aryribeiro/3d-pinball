import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import os

# --- Configurações Globais ---
APP_TITLE = "🪩 3D Pinball | Space Cadet"
PAGE_BACKGROUND_COLOR = "#3A6EA5"

# --- Estado da Sessão ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# --- Função para converter imagem para base64 ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# --- Função para ler arquivo como texto ---
def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

# --- Função para ler arquivo binário como base64 ---
def read_binary_as_base64(file_path):
    try:
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="collapsed")

# Diretório dos arquivos do jogo
game_files_directory = Path(__file__).resolve().parent

# Converter imagem para base64
mesa_image_path = game_files_directory / "mesa.png"
mesa_base64 = get_base64_image(mesa_image_path)

# CSS para fundo azul e layout
st.markdown(f"""
<style>
    html, body, [data-testid="stAppViewContainer"], .main {{
        background-color: {PAGE_BACKGROUND_COLOR} !important;
        height: 100vh !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
    }}
    
    .block-container {{
        padding: 10px !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100vw !important;
    }}
    
    header[data-testid="stHeader"], 
    .stDeployButton,
    footer,
    .stDecoration {{
        display: none !important;
    }}
    
    .game-header {{
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: {PAGE_BACKGROUND_COLOR};
        color: #FFFFFF;
        text-align: center;
        padding: 20px 0 10px 0;
        margin-bottom: 20px;
    }}
    
    .game-title {{
        font-size: 32px;
        margin-bottom: 20px;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-top: 0;
    }}
    
    .game-content {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 60vh;
        background-color: {PAGE_BACKGROUND_COLOR};
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    .game-image {{
        max-width: 80vw;
        max-height: 60vh;
        width: auto;
        height: auto;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }}
    
    .stButton > button {{
        padding: 15px 30px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
        background: linear-gradient(45deg, #0066CC, #0099FF) !important;
        border: none !important;
        border-radius: 10px !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(0, 100, 200, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        height: auto !important;
        margin-bottom: 15px !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(45deg, #0055AA, #0088EE) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 100, 200, 0.4) !important;
    }}
    
    .stButton {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }}
    
    .error-message {{
        color: #FF6B6B;
        background: rgba(255, 107, 107, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #FF6B6B;
        margin: 20px;
        text-align: center;
    }}
    
    .game-container {{
        width: 100%;
        height: 80vh;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background-color: #000;
    }}
</style>
""", unsafe_allow_html=True)

# Verificar se arquivo HTML existe
index_html_path = game_files_directory / "index.html"
if not index_html_path.is_file():
    st.markdown(f"""
    <div class="error-message">
        <h2>ERRO: Arquivo 'index.html' não encontrado</h2>
        <p>Verifique se o arquivo está no diretório: {game_files_directory}</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Header fixo com título
st.markdown(f"""
<div class="game-header">
    <h1 class="game-title">{APP_TITLE}</h1>
</div>
""", unsafe_allow_html=True)

# Criar layout com colunas para o botão
if not st.session_state.game_started:
    # Mostrar imagem e botão quando jogo não iniciou
    st.markdown(f"""
    <div class="game-content">
        {"<img src='data:image/png;base64," + mesa_base64 + "' class='game-image' alt='Mesa de Pinball'>" if mesa_base64 else "<p style='color: #CCCCCC;'>Imagem mesa.png não encontrada</p>"}
    </div>
    """, unsafe_allow_html=True)
    
    # Botão centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 INICIAR JOGO", key="start_game", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()

else:
    # Mostrar o jogo quando iniciado
    # Ler conteúdo do HTML
    html_content = read_file_content(index_html_path)
    
    if html_content:
        # Ler arquivos JavaScript necessários
        js_file_path = game_files_directory / "SpaceCadetPinball.js"
        js_content = ""
        
        if js_file_path.exists():
            js_base64 = read_binary_as_base64(js_file_path)
            if js_base64:
                js_content = f'<script src="data:application/javascript;base64,{js_base64}"></script>'
        
        # Ler arquivos WASM se existirem
        wasm_files = list(game_files_directory.glob("*.wasm"))
        data_files = list(game_files_directory.glob("*.data"))
        
        # Modificar HTML para funcionar inline
        modified_html = html_content.replace(
            '<script async src=SpaceCadetPinball.js></script>',
            js_content
        )
        
        # HTML completo para o jogo
        game_html = f"""
        <!DOCTYPE html>
        <html style="margin: 0; padding: 0; height: 100%; background-color: #000;">
        <head>
            <meta charset="utf-8">
            <title>3D Pinball Space Cadet</title>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    background-color: #3A6EA5;
                    overflow: hidden;
                }}
                .window {{
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }}
                canvas {{
                    display: block;
                    margin: 0 auto;
                    background-color: #000;
                }}
                #status {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: white;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            {modified_html.replace('<!doctypehtml><html lang=en-us><head>', '').replace('</body></html>', '')}
        </body>
        </html>
        """
        
        # Renderizar o jogo
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        components.html(game_html, height=600, scrolling=False)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botão para voltar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔙 VOLTAR AO MENU", key="back_to_menu", use_container_width=True):
                st.session_state.game_started = False
                st.rerun()
    else:
        st.markdown("""
        <div class="error-message">
            <h2>Erro ao carregar o jogo</h2>
            <p>Não foi possível ler o arquivo HTML do jogo.</p>
        </div>
        """, unsafe_allow_html=True)

# Rodapé
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #3A6EA5;">
  <div style="color: white; font-size: 14px;">
  💬 Por <strong>Ary Ribeiro</strong>. Obs.: fork da Alula. Código original no GitHub: 
  <a href="https://github.com/alula/SpaceCadetPinball/tree/gh-pages" style="color: white;">AQUI</a><br>
  <em>Obs.: Use o mouse para controlar os flippers e lançar a bola</em>
</div>
""", unsafe_allow_html=True)