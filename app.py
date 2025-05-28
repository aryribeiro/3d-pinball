import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import os

# --- Configurações Globais ---
APP_TITLE = "🪩 3D Pinball | Space Cadet"
# URL para o jogo hospedado publicamente (GitHub Pages da Alula para SpaceCadetPinball)
HOSTED_GAME_URL = "https://alula.github.io/SpaceCadetPinball/"

# Fundo azul escuro do game original
PAGE_BACKGROUND_COLOR = "#3A6EA5"

# --- Estado da Sessão ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# --- Função para converter imagem para base64 ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        print(f"Aviso: Arquivo de imagem não encontrado em {image_path}")
        return None
    except Exception as e:
        print(f"Erro ao carregar imagem {image_path}: {e}")
        return None

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title=APP_TITLE, layout="centered", initial_sidebar_state="collapsed")

# Converter imagem para base64
# __file__ é o caminho para o script atual. .parent pega o diretório.
game_files_directory = str(Path(__file__).resolve().parent)
mesa_image_path = Path(game_files_directory) / "mesa.png"
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
        padding: 0 !important;
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
        position: sticky;
        top: 0;
        z-index: 1000;
    }}
    
    .game-title {{
        font-size: 48px;
        margin-bottom: 30px;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-top: 0;
    }}
    
    .game-content {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: calc(100vh - 120px); /* Altura para conteúdo antes do jogo iniciar */
        background-color: {PAGE_BACKGROUND_COLOR};
        padding: 20px;
    }}
    
    .game-image {{
        max-width: 90vw;
        max-height: 70vh;
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
        width: auto !important;
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
    }}
    
    /* .game-iframe classe original, mantida caso seja usada em outro contexto.
       O iframe do jogo é estilizado diretamente no HTML do components.html. */
    .game-iframe {{
        width: 100vw !important;
        height: calc(100vh - 120px) !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
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
</style>
""", unsafe_allow_html=True)

# --- Lógica Principal ---

# Header fixo com título
st.markdown(f"""
<div class="game-header">
    <h1 class="game-title">{APP_TITLE}</h1>
</div>
""", unsafe_allow_html=True)

# Botão centralizado abaixo do header
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 INICIAR JOGO", key="start_game"):
        st.session_state.game_started = True
        st.rerun() # Rerun para atualizar a interface e mostrar o jogo

# Conteúdo principal (imagem de preview ou o jogo)
if st.session_state.game_started:
    # Mostrar game usando components.html
    game_url = HOSTED_GAME_URL
    
    # Altura fixa para o iframe do componente que contém o jogo.
    # O valor 680px foi usado no código original com components.html.
    game_container_height_px = 680 

    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body, html {{ /* Estilos para o documento DENTRO do iframe de components.html */
                margin: 0;
                padding: 0;
                width: 100%; /* Preenche a largura do iframe de components.html */
                height: 100%; /* Preenche a altura do iframe de components.html */
                overflow: hidden;
                background-color: {PAGE_BACKGROUND_COLOR}; /* Cor de fundo opcional */
            }}
            iframe {{ /* Estilos para o iframe DO JOGO, dentro do documento acima */
                width: 100%;
                height: 100%;
                border: none;
                margin: 0;
                padding: 0;
                display: block; /* Para evitar espaços extras abaixo do iframe */
            }}
        </style>
    </head>
    <body>
        <iframe src="{game_url}" allowfullscreen></iframe>
    </body>
    </html>
    """, height=game_container_height_px, scrolling=False)
else:
    # Mostrar imagem do jogo antes de iniciar
    st.markdown(f"""
    <div class="game-content">
        {"<img src='data:image/png;base64," + mesa_base64 + "' class='game-image' alt='Mesa de Pinball'>" if mesa_base64 else "<p style='color: #CCCCCC;'>Imagem da mesa (mesa.png) não encontrada.</p>"}
    </div>
    """, unsafe_allow_html=True)

# Rodapé com créditos
st.markdown("""
<div style="text-align: center; padding-top: 20px; padding-bottom: 20px;">
  <div style="color: white; font-size: 14px;">
  💬 Por <strong>Ary Ribeiro</strong>. Obs.: fork da Alula. Código original no GitHub: 
  <a href="https://github.com/alula/SpaceCadetPinball/tree/gh-pages" target="_blank" style="color: white; text-decoration: underline;">AQUI</a><br>
  <em>Obs.: Use o mouse para controlar os flippers e lançar a bola.</em>
</div>
""", unsafe_allow_html=True)