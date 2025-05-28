import streamlit as st
import streamlit.components.v1 as components
import http.server
import socketserver
import threading
from pathlib import Path
from functools import partial
import time
import os
import base64

# --- Configurações Globais ---
GAME_HTML_ENTRY_POINT = "index.html"
LOCAL_GAME_SERVER_PORT = 8001
APP_TITLE = "🪩 3D Pinball | Space Cadet"

# Fundo azul escuro do game original
PAGE_BACKGROUND_COLOR = "#3A6EA5"

# --- Estado da Sessão ---
if 'python_server_thread_launched_final_ux' not in st.session_state:
    st.session_state.python_server_thread_launched_final_ux = False
if 'python_server_init_error_final_ux' not in st.session_state:
    st.session_state.python_server_init_error_final_ux = None
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# --- Função para converter imagem para base64 ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# --- Função do Servidor HTTP (Thread Separada) ---
def start_http_server_thread(directory_to_serve: str, port: int):
    class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

    handler = partial(QuietHTTPRequestHandler, directory=directory_to_serve)
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"SUCCESS: Local HTTP server started on port {port}")
            httpd.serve_forever()
    except Exception as e:
        error_msg = f"PYTHON_SERVER_ERROR: Failed to start HTTP server on port {port}: {e}"
        print(error_msg)
        st.session_state.python_server_init_error_final_ux = error_msg

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title=APP_TITLE, layout="centered", initial_sidebar_state="collapsed")

# Converter imagem para base64
game_files_directory = str(Path(__file__).resolve().parent / "static")
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

# --- Função para detectar ambiente ---
def is_local_environment():
    """Detecta se está rodando localmente ou em produção"""
    # Verifica variáveis de ambiente do Streamlit Cloud
    return not any([
        os.getenv('STREAMLIT_SHARING_MODE'),
        os.getenv('STREAMLIT_SERVER_PORT'),
        'streamlit.app' in os.getenv('HOSTNAME', '').lower(),
        'streamlit' in os.getenv('RAILWAY_ENVIRONMENT_NAME', '').lower()
    ])

# --- Lógica Principal ---
# Debug: listar arquivos disponíveis
current_dir = Path(__file__).resolve().parent
static_dir = current_dir / "static"

st.write("DEBUG - Diretório atual:", str(current_dir))
st.write("DEBUG - Diretório static:", str(static_dir))
st.write("DEBUG - Arquivos no diretório atual:", list(current_dir.glob("*")))
if static_dir.exists():
    st.write("DEBUG - Arquivos no diretório static:", list(static_dir.glob("*")))

path_to_index_html = Path(game_files_directory) / GAME_HTML_ENTRY_POINT

# Verificar se arquivo existe
if not path_to_index_html.is_file():
    # Tentar encontrar o arquivo em outros locais
    possible_paths = [
        current_dir / GAME_HTML_ENTRY_POINT,
        static_dir / GAME_HTML_ENTRY_POINT,
        current_dir / "static" / GAME_HTML_ENTRY_POINT
    ]
    
    found_path = None
    for path in possible_paths:
        if path.is_file():
            found_path = path
            game_files_directory = str(path.parent)
            path_to_index_html = path
            break
    
    if not found_path:
        st.markdown(f"""
        <div class="error-message">
            <h2>ERRO: Arquivo '{GAME_HTML_ENTRY_POINT}' não encontrado</h2>
            <p>Procurado em: {game_files_directory}</p>
            <p>Caminhos testados:</p>
            <ul>
                {"".join([f"<li>{path}</li>" for path in possible_paths])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# Detectar ambiente e configurar URL apropriada
is_local = is_local_environment()

if is_local:
    # Ambiente local - usar servidor HTTP local
    if not st.session_state.python_server_thread_launched_final_ux:
        st.session_state.python_server_thread_launched_final_ux = True
        st.session_state.python_server_init_error_final_ux = None
        
        server_thread = threading.Thread(
            target=start_http_server_thread,
            args=(game_files_directory, LOCAL_GAME_SERVER_PORT),
            daemon=True
        )
        server_thread.start()
        time.sleep(1)
        st.rerun()
    
    game_url = f"http://localhost:{LOCAL_GAME_SERVER_PORT}/{GAME_HTML_ENTRY_POINT}"
else:
    # Ambiente de produção - usar arquivos estáticos diretamente
    # Ler conteúdo do HTML e servir inline
    with open(path_to_index_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Ler arquivos JavaScript e outros recursos necessários
    js_files = list(Path(game_files_directory).glob("*.js"))
    wasm_files = list(Path(game_files_directory).glob("*.wasm"))
    data_files = list(Path(game_files_directory).glob("*.data"))
    
    # Converter arquivos para base64 para servir inline
    resources = {}
    for file_path in js_files + wasm_files + data_files:
        with open(file_path, 'rb') as f:
            resources[file_path.name] = base64.b64encode(f.read()).decode()

# Interface principal
if is_local and st.session_state.python_server_init_error_final_ux:
    st.markdown(f"""
    <div class="error-message">
        <h2>Erro ao iniciar servidor</h2>
        <p>{st.session_state.python_server_init_error_final_ux}</p>
        <button onclick="location.reload()" class="start-button">Tentar Novamente</button>
    </div>
    """, unsafe_allow_html=True)
else:
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
        if is_local:
            # Ambiente local - usar iframe com servidor HTTP
            components.html(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body, html {{
                        margin: 0;
                        padding: 0;
                        width: 100vw;
                        height: calc(100vh - 120px);
                        overflow: hidden;
                        background-color: {PAGE_BACKGROUND_COLOR};
                    }}
                    iframe {{
                        width: 100vw;
                        height: 100%;
                        border: none;
                        margin: 0;
                        padding: 0;
                    }}
                </style>
            </head>
            <body>
                <iframe src="{game_url}" allowfullscreen></iframe>
            </body>
            </html>
            """, height=680, scrolling=False)
        else:
            # Ambiente de produção - servir HTML inline com recursos embutidos
            production_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body, html {{
                        margin: 0;
                        padding: 0;
                        width: 100vw;
                        height: calc(100vh - 120px);
                        overflow: hidden;
                        background-color: {PAGE_BACKGROUND_COLOR};
                    }}
                </style>
            </head>
            <body>
                {html_content}
                <script>
                    // Configurar URLs para recursos em produção
                    Module.locateFile = function(path) {{
                        if (path.endsWith('.wasm') || path.endsWith('.data')) {{
                            return 'data:application/octet-stream;base64,' + resources[path];
                        }}
                        return path;
                    }};
                </script>
            </body>
            </html>
            """
            
            components.html(production_html, height=680, scrolling=False)
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