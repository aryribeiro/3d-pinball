import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import os
import re

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

# --- Função para converter arquivo para base64 ---
def get_base64_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title=APP_TITLE, layout="centered", initial_sidebar_state="collapsed")

# Diretório dos arquivos do jogo
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

# --- Verificar se arquivo existe ---
path_to_index_html = Path(game_files_directory) / GAME_HTML_ENTRY_POINT

if not path_to_index_html.is_file():
    st.markdown(f"""
    <div class="error-message">
        <h2>ERRO: Arquivo '{GAME_HTML_ENTRY_POINT}' não encontrado</h2>
        <p>Verifique se o arquivo está no diretório correto: {game_files_directory}</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- Interface Principal ---
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
    try:
        # Ler o arquivo HTML principal
        with open(path_to_index_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        game_dir = Path(game_files_directory)
        
        # Função para processar e embdar arquivos
        def embed_files_in_html(html_content, base_dir):
            # Processar arquivos JavaScript
            js_pattern = r'<script[^>]*src="([^"]*\.js)"[^>]*></script>'
            for match in re.finditer(js_pattern, html_content):
                js_file = match.group(1)
                js_path = base_dir / js_file
                if js_path.exists():
                    try:
                        with open(js_path, 'r', encoding='utf-8') as js_f:
                            js_content = js_f.read()
                        html_content = html_content.replace(
                            match.group(0), 
                            f'<script>\n{js_content}\n</script>'
                        )
                    except:
                        pass
            
            # Processar arquivos CSS
            css_pattern = r'<link[^>]*href="([^"]*\.css)"[^>]*>'
            for match in re.finditer(css_pattern, html_content):
                css_file = match.group(1)
                css_path = base_dir / css_file
                if css_path.exists():
                    try:
                        with open(css_path, 'r', encoding='utf-8') as css_f:
                            css_content = css_f.read()
                        html_content = html_content.replace(
                            match.group(0), 
                            f'<style>\n{css_content}\n</style>'
                        )
                    except:
                        pass
            
            # Processar arquivos WASM como base64
            wasm_pattern = r'(["\']?)([^"\']*\.wasm)\1'
            for match in re.finditer(wasm_pattern, html_content):
                wasm_file = match.group(2)
                if not wasm_file.startswith('data:'):
                    wasm_path = base_dir / wasm_file
                    if wasm_path.exists():
                        wasm_base64 = get_base64_file(wasm_path)
                        if wasm_base64:
                            data_url = f'data:application/wasm;base64,{wasm_base64}'
                            html_content = html_content.replace(
                                match.group(0), 
                                f'{match.group(1)}{data_url}{match.group(1)}'
                            )
            
            # Processar outros recursos (imagens, data files)
            resource_pattern = r'(["\']?)([^"\']*\.(png|jpg|jpeg|gif|ico|data|mem))\1'
            for match in re.finditer(resource_pattern, html_content):
                resource_file = match.group(2)
                if not resource_file.startswith('data:') and not resource_file.startswith('http'):
                    resource_path = base_dir / resource_file
                    if resource_path.exists():
                        resource_base64 = get_base64_file(resource_path)
                        if resource_base64:
                            ext = resource_file.split('.')[-1].lower()
                            mime_types = {
                                'png': 'image/png',
                                'jpg': 'image/jpeg', 
                                'jpeg': 'image/jpeg',
                                'gif': 'image/gif',
                                'ico': 'image/x-icon',
                                'data': 'application/octet-stream',
                                'mem': 'application/octet-stream'
                            }
                            mime_type = mime_types.get(ext, 'application/octet-stream')
                            data_url = f'data:{mime_type};base64,{resource_base64}'
                            html_content = html_content.replace(
                                match.group(0),
                                f'{match.group(1)}{data_url}{match.group(1)}'
                            )
            
            return html_content
        
        # Processar o HTML
        processed_html = embed_files_in_html(html_content, game_dir)
        
        # Adicionar CSS para fullscreen
        processed_html = processed_html.replace(
            '<head>',
            f'''<head>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100vw;
                    height: 100vh;
                    overflow: hidden;
                    background-color: {PAGE_BACKGROUND_COLOR};
                }}
                canvas {{
                    display: block;
                    margin: 0 auto;
                }}
            </style>'''
        )
        
        # Renderizar o jogo
        components.html(processed_html, height=680, scrolling=False)
        
    except Exception as e:
        st.error(f"Erro ao carregar o jogo: {str(e)}")
        st.markdown(f"""
        <div class="error-message">
            <h2>Erro ao processar arquivos do jogo</h2>
            <p>Detalhes: {str(e)}</p>
            <p>Verifique se todos os arquivos necessários estão no diretório.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # Mostrar imagem do jogo
    st.markdown(f"""
    <div class="game-content">
        {"<img src='data:image/png;base64," + mesa_base64 + "' class='game-image' alt='Mesa de Pinball'>" if mesa_base64 else "<p style='color: #CCCCCC;'>Imagem mesa.png não encontrada</p>"}
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
  <div style="color: white;">
  💬 Por <strong>Ary Ribeiro</strong>. Obs.: fork da Alula. Código original no GitHub: 
  <a href="https://github.com/alula/SpaceCadetPinball/tree/gh-pages" style="color: white;">AQUI</a><br>
  <em>Obs.: Use o mouse p/ controlar</em>
</div>
""", unsafe_allow_html=True)