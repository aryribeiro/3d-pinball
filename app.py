import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

# --- Configurações Globais ---
GAME_HTML_ENTRY_POINT = "index.html"
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

# --- Função para ler arquivo HTML ---
def read_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except:
        return None

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="collapsed")

# Converter imagem para base64
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
        min-height: calc(100vh - 120px);
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
path_to_index_html = Path(game_files_directory) / GAME_HTML_ENTRY_POINT

# Verificar se arquivo existe
if not path_to_index_html.is_file():
    st.markdown(f"""
    <div class="error-message">
        <h2>ERRO: Arquivo '{GAME_HTML_ENTRY_POINT}' não encontrado</h2>
        <p>Verifique se o arquivo está no diretório correto: {game_files_directory}</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Ler conteúdo do HTML
html_content = read_html_file(path_to_index_html)
if not html_content:
    st.markdown(f"""
    <div class="error-message">
        <h2>ERRO: Não foi possível ler o arquivo '{GAME_HTML_ENTRY_POINT}'</h2>
        <p>Verifique as permissões do arquivo</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Interface principal
# Header fixo com título e botão
st.markdown(f"""
<div class="game-header">
    <h1 class="game-title">{APP_TITLE}</h1>
</div>
""", unsafe_allow_html=True)

# Botão centralizado no header
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 INICIAR JOGO", key="start_game"):
        st.session_state.game_started = True
        st.rerun()

# Conteúdo principal
if st.session_state.game_started:
    # Modificar o HTML para usar caminhos relativos corretos
    modified_html = html_content.replace(
        'src="', 
        f'src="./'
    ).replace(
        'href="',
        f'href="./'
    )
    
    # Embed o jogo diretamente usando components.html
    components.html(
        modified_html,
        height=800,
        scrolling=False
    )
else:
    # Mostrar imagem do jogo
    st.markdown(f"""
    <div class="game-content">
        {"<img src='data:image/png;base64," + mesa_base64 + "' class='game-image' alt='Mesa de Pinball'>" if mesa_base64 else "<p style='color: #CCCCCC;'>Imagem mesa.png não encontrada</p>"}
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 20px;">
  <div style="color: white; font-size: 14px;">
  💬 Por <strong>Ary Ribeiro</strong>. Obs.: fork da Alula. Código original no GitHub: 
  <a href="https://github.com/alula/SpaceCadetPinball/tree/gh-pages" style="color: white;">AQUI</a><br>
  <em>Use o mouse para controlar</em>
  </div>
</div>
""", unsafe_allow_html=True)