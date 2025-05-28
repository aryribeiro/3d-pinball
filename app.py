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

# Detectar ambiente e configurar URL apropriada
is_local = is_local_environment()

# Interface principal
if st.session_state.python_server_init_error_final_ux:
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
        # Ler conteúdo do HTML
        with open(path_to_index_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Modificar o HTML para funcionar no Streamlit
        modified_html = html_content.replace(
            'src=SpaceCadetPinball.js',
            f'src="./static/SpaceCadetPinball.js"'
        )
        
        # Servir diretamente o HTML modificado
        production_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                :root{{
                    --ActiveBorder:rgb(212, 208, 200);
                    --ActiveTitle:rgb(10, 36, 106);
                    --AppWorkspace:rgb(128, 128, 128);
                    --Background:rgb(58, 110, 165);
                    --ButtonAlternateFace:rgb(192, 192, 192);
                    --ButtonDkShadow:rgb(64, 64, 64);
                    --ButtonFace:rgb(212, 208, 200);
                    --ButtonHilight:rgb(255, 255, 255);
                    --ButtonLight:rgb(212, 208, 200);
                    --ButtonShadow:rgb(128, 128, 128);
                    --ButtonText:rgb(0, 0, 0);
                    --GradientActiveTitle:rgb(166, 202, 240);
                    --GradientInactiveTitle:rgb(192, 192, 192);
                    --GrayText:rgb(128, 128, 128);
                    --Hilight:rgb(10, 36, 106);
                    --HilightText:rgb(255, 255, 255);
                    --HotTrackingColor:rgb(0, 0, 128);
                    --InactiveBorder:rgb(212, 208, 200);
                    --InactiveTitle:rgb(128, 128, 128);
                    --InactiveTitleText:rgb(212, 208, 200);
                    --InfoText:rgb(0, 0, 0);
                    --InfoWindow:rgb(255, 255, 225);
                    --Menu:rgb(212, 208, 200);
                    --MenuBar:rgb(192, 192, 192);
                    --MenuHilight:rgb(0, 0, 128);
                    --MenuText:rgb(0, 0, 0);
                    --Scrollbar:rgb(212, 208, 200);
                    --TitleText:rgb(255, 255, 255);
                    --Window:rgb(255, 255, 255);
                    --WindowFrame:rgb(0, 0, 0);
                    --WindowText:rgb(0, 0, 0);
                }}
                body {{
                    font-family: Tahoma, Geneva, Verdana, sans-serif;
                    background-color: var(--Background);
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                }}
                canvas.emscripten {{
                    border: 0 none;
                    background-color: #000;
                    width: 100% !important;
                    height: 100% !important;
                }}
                .window {{
                    font-size: 8pt;
                    color: var(--WindowText);
                    background-color: var(--ButtonFace);
                    border: 1px solid var(--ActiveBorder);
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }}
                #status {{
                    margin: 20px;
                    color: white;
                }}
                #progress {{
                    margin: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="active window">
                <div id="status">Carregando...</div>
                <div><progress hidden id="progress" max="100" value="0"></progress></div>
                <canvas class="emscripten" id="canvas" oncontextmenu="event.preventDefault()" tabindex="-1"></canvas>
            </div>
            
            <script>
                var statusElement = document.getElementById('status');
                var progressElement = document.getElementById('progress');
                var Module = {{
                    preRun: [],
                    postRun: [],
                    print: function(text) {{
                        console.log(text);
                    }},
                    printErr: function(text) {{
                        console.error(text);
                    }},
                    canvas: document.getElementById('canvas'),
                    setStatus: function(text) {{
                        if (!Module.setStatus.last) Module.setStatus.last = {{ time: Date.now(), text: '' }};
                        if (text === Module.setStatus.last.text) return;
                        var m = text.match(/([^(]+)\\((\\d+(\\.\\d+)?)\\/(\\d+)\\)/);
                        var now = Date.now();
                        if (m && now - Module.setStatus.last.time < 30) return;
                        Module.setStatus.last.time = now;
                        Module.setStatus.last.text = text;
                        if (m) {{
                            text = m[1];
                            progressElement.value = parseInt(m[2]) * 100;
                            progressElement.max = parseInt(m[4]) * 100;
                            progressElement.hidden = false;
                        }} else {{
                            progressElement.value = null;
                            progressElement.max = null;
                            progressElement.hidden = true;
                            document.getElementById('canvas').style.display = '';
                        }}
                        statusElement.innerHTML = text;
                        if (text === '') {{
                            statusElement.style.display = 'none';
                            progressElement.style.display = 'none';
                        }} else {{
                            statusElement.style.display = '';
                            progressElement.style.display = '';
                        }}
                    }},
                    totalDependencies: 0,
                    monitorRunDependencies: function(left) {{
                        this.totalDependencies = Math.max(this.totalDependencies, left);
                        Module.setStatus(left ? 'Preparando... (' + (this.totalDependencies - left) + '/' + this.totalDependencies + ')' : 'Todos os downloads concluídos.');
                    }}
                }};
                Module.setStatus('Baixando...');
                window.onerror = function() {{
                    Module.setStatus('Exceção lançada, verifique o console JavaScript');
                    Module.setStatus = function(text) {{
                        if (text) Module.printErr('[post-exception status] ' + text);
                    }};
                }};
            </script>
            <script async src="./static/SpaceCadetPinball.js"></script>
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