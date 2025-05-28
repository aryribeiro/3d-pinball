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
    except FileNotFoundError:
        print(f"Warning: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None

# --- Função do Servidor HTTP (Thread Separada) ---
def start_http_server_thread(directory_to_serve: str, port: int):
    # QuietHTTPRequestHandler silences all server logging output to the console
    class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory_to_serve, **kwargs)

        def log_message(self, format, *args):
            # Override to keep the console clean
            pass

    # Use partial to set the directory for the handler
    handler = partial(QuietHTTPRequestHandler, directory=directory_to_serve)
    
    try:
        # Allow address reuse, crucial for quick restarts (common in Streamlit dev)
        socketserver.TCPServer.allow_reuse_address = True
        # Bind to all available interfaces (0.0.0.0) on the specified port
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"SUCCESS: Local HTTP server started on port {port}, serving from '{directory_to_serve}'")
            httpd.serve_forever()
    except Exception as e:
        error_msg = f"PYTHON_SERVER_ERROR: Failed to start HTTP server on port {port}: {e}"
        print(error_msg)
        # Use Streamlit's session state to communicate the error to the main thread
        st.session_state.python_server_init_error_final_ux = error_msg

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title=APP_TITLE, layout="centered", initial_sidebar_state="collapsed")

# Determine game files directory relative to the script file
game_files_directory = str(Path(__file__).resolve().parent)
mesa_image_path = Path(game_files_directory) / "mesa.png"
mesa_base64 = get_base64_image(mesa_image_path)

# CSS para fundo azul, layout e ocultar elementos indesejados do Streamlit
st.markdown(f"""
<style>
    /* Core layout and background */
    html, body, [data-testid="stAppViewContainer"], .main {{
        background-color: {PAGE_BACKGROUND_COLOR} !important;
        height: 100vh !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important; /* Changed from overflow-x: hidden */
    }}
    
    .block-container {{ /* Ensure content can fill screen */
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100vw !important;
        height: 100vh !important; 
    }}
    
    /* Hide Streamlit's default header, footer, and hamburger menu */
    header[data-testid="stHeader"], 
    .stDeployButton,
    footer,
    #MainMenu {{ /* Target hamburger menu more reliably */
        display: none !important;
    }}
    
    /* Styling for the custom game header */
    .game-header {{
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: {PAGE_BACKGROUND_COLOR}; /* Ensure header bg matches page */
        color: #FFFFFF;
        text-align: center;
        padding: 15px 0 5px 0; /* Reduced padding */
        position: sticky;
        top: 0;
        z-index: 1000;
        width: 100%;
    }}
    
    .game-title {{
        font-size: 36px; /* Slightly reduced */
        margin-bottom: 10px; /* Reduced margin */
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-top: 0;
    }}

    /* Container for start button, placed within columns for centering */
    .button-container {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 10px; /* Space below button before image/game */
    }}
    
    /* Styling for the main game content area (image or iframe) */
    .game-content-area {{
        display: flex;
        justify-content: center;
        align-items: center;
        /* Calculate height: viewport height - header height (approx) */
        /* Adjust 80px based on actual header height */
        min-height: calc(100vh - 80px); 
        background-color: {PAGE_BACKGROUND_COLOR};
        padding: 0; /* No padding for the content area itself */
        width: 100%;
    }}
    
    .game-image {{
        max-width: 90vw;
        max-height: calc(100vh - 100px); /* Ensure image respects header */
        width: auto;
        height: auto;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }}
    
    /* Streamlit button styling */
    .stButton > button {{
        padding: 12px 25px !important; /* Slightly smaller padding */
        font-size: 18px !important; /* Slightly smaller font */
        font-weight: bold !important;
        color: #FFFFFF !important;
        background: linear-gradient(45deg, #0066CC, #0099FF) !important;
        border: none !important;
        border-radius: 10px !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(0, 100, 200, 0.3) !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(45deg, #0055AA, #0088EE) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 100, 200, 0.4) !important;
    }}
        
    /* Iframe styling for the game */
    .game-iframe-container {{ /* New container for iframe sizing */
        width: 100vw;
        height: calc(100vh - 80px); /* Adjust 80px based on actual header height */
        margin: 0;
        padding: 0;
        overflow: hidden; /* Ensure no scrollbars on container */
    }}

    iframe#game_iframe {{ /* Target iframe by ID */
        width: 100%;
        height: 100%;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        display: block; /* Remove extra space below iframe */
    }}
    
    /* Error message styling */
    .error-message {{
        color: #FF6B6B;
        background: rgba(255, 107, 107, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #FF6B6B;
        margin: 20px;
        text-align: center;
    }}

    .error-message button.start-button {{ /* Make sure retry button is visible */
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #007bff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }}
    .error-message button.start-button:hover {{
        background-color: #0056b3;
    }}
    .footer-credits {{
        position: fixed;
        bottom: 5px;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
        font-size: 0.8em;
        color: #FFFFFF; /* White text for footer */
        width: 100%;
        z-index: 1001; /* Above game content but below modals if any */
    }}
    .footer-credits a {{
        color: #ADD8E6; /* Light blue for links, for better contrast */
        text-decoration: none;
    }}
    .footer-credits a:hover {{
        text-decoration: underline;
    }}
</style>
""", unsafe_allow_html=True)

# --- Lógica Principal ---
path_to_index_html = Path(game_files_directory) / GAME_HTML_ENTRY_POINT

# Verificar se o arquivo HTML principal do jogo existe
if not path_to_index_html.is_file():
    st.markdown(f"""
    <div class="error-message">
        <h2>ERRO CRÍTICO: Arquivo '{GAME_HTML_ENTRY_POINT}' não encontrado!</h2>
        <p>Verifique se o arquivo está no diretório correto: '{game_files_directory}'. O aplicativo não pode continuar.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop() # Parar a execução se o arquivo do jogo não for encontrado

# Iniciar servidor HTTP local em uma thread separada, se ainda não foi iniciado
if not st.session_state.python_server_thread_launched_final_ux:
    st.session_state.python_server_thread_launched_final_ux = True
    st.session_state.python_server_init_error_final_ux = None # Limpar erro anterior
    
    server_thread = threading.Thread(
        target=start_http_server_thread,
        args=(game_files_directory, LOCAL_GAME_SERVER_PORT),
        daemon=True # Thread daemon morrerá quando o programa principal sair
    )
    server_thread.start()
    time.sleep(0.5) # Dar um breve momento para o servidor iniciar
    st.rerun() # Rerun para verificar o status do servidor

# Interface principal
if st.session_state.python_server_init_error_final_ux:
    # Mostrar mensagem de erro se o servidor falhar ao iniciar
    st.markdown(f"""
    <div class="error-message">
        <h2>Erro Crítico ao Iniciar Servidor Interno</h2>
        <p>{st.session_state.python_server_init_error_final_ux}</p>
        <p>Este aplicativo requer um servidor local para funcionar. Por favor, verifique se a porta {LOCAL_GAME_SERVER_PORT} não está em uso por outro aplicativo.</p>
        <button onclick="window.location.reload()" class="start-button">Tentar Novamente</button>
    </div>
    """, unsafe_allow_html=True)
else:
    # Header fixo com título
    st.markdown(f"""
    <div class="game-header">
        <h1 class="game-title">{APP_TITLE}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Colocar o botão de iniciar jogo em uma coluna centralizada abaixo do título
    # Usando st.columns para centralizar o botão de forma mais robusta
    _, col_button, _ = st.columns([1, 0.5, 1]) # Ajustar proporções conforme necessário
    with col_button:
        # Envolver o botão em um div para aplicar CSS de centralização se necessário
        st.markdown("""<div class="button-container">""", unsafe_allow_html=True)
        if st.button("🚀 INICIAR JOGO", key="start_game_button"):
            st.session_state.game_started = True
            st.rerun() # Rerun para mostrar o jogo
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Conteúdo principal: imagem do jogo ou o próprio jogo
    st.markdown("""<div class="game-content-area">""", unsafe_allow_html=True)
    if st.session_state.game_started:
        # Mostrar o jogo usando components.html com iframe
        # O src do iframe será definido dinamicamente por JavaScript
        # para lidar corretamente com localhost (desenvolvimento) e URLs de produção.
        
        # A altura do iframe é calculada dinamicamente com JS para preencher o espaço.
        # O `calc(100vh - 80px)` é uma aproximação, o JS pode ser mais preciso.
        components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Game Loader</title>
            <style>
                body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background-color: {PAGE_BACKGROUND_COLOR}; }}
                iframe {{ display: block; width: 100%; height: 100%; border: none; }}
            </style>
        </head>
        <body>
            <iframe id="game_iframe" allowfullscreen title="Game Content"></iframe>
            <script>
                const gamePort = {LOCAL_GAME_SERVER_PORT};
                const gameEntry = "{GAME_HTML_ENTRY_POINT}";
                let iframeSrc;

                // Lógica para determinar o URL base do jogo
                // Em desenvolvimento (localhost), usa http://localhost:gamePort
                // Em produção, tenta usar window.location.origin/:gamePort/ (requer que a plataforma de hospedagem encaminhe/proxie esta porta)
                if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {{
                    iframeSrc = `http://localhost:${{gamePort}}/${{gameEntry}}`;
                }} else {{
                    // Para produção (ex: Streamlit Cloud)
                    // Esta sintaxe assume que a plataforma pode rotear para um serviço interno na porta especificada
                    // usando o formato 'https://[hostname]/:[port]/[path]'.
                    // Esta é uma suposição crítica e pode não funcionar em todas as plataformas.
                    // Se não funcionar, o jogo precisará ser hospedado externamente ou
                    // a plataforma precisa de uma configuração de proxy específica.
                    iframeSrc = `${{window.location.origin}}/:${{gamePort}}/${{gameEntry}}`;
                }}
                
                const iframeElement = document.getElementById('game_iframe');
                iframeElement.src = iframeSrc;
                
                // Ajustar altura do contêiner do iframe dinamicamente
                // O contêiner do iframe já tem `height: calc(100vh - approx_header_height)` via CSS.
                // Não é necessário JS adicional para esta parte se o CSS for suficiente.
            </script>
        </body>
        </html>
        """, height=700, scrolling=False) # A altura aqui é para o contêiner do Streamlit component
    else:
        # Mostrar imagem de placeholder do jogo antes de iniciar
        if mesa_base64:
            st.markdown(f"<img src='data:image/png;base64,{mesa_base64}' class='game-image' alt='Mesa de Pinball'>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #CCCCCC; text-align: center;'>Imagem da mesa de pinball (mesa.png) não encontrada.</p>", unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)

# Rodapé com créditos
st.markdown("""
<div class="footer-credits">
  <span>💬 Por <strong>Ary Ribeiro</strong>. Fork de 
  <a href="https://github.com/alula/SpaceCadetPinball" target="_blank">Alula's SpaceCadetPinball GH-Pages</a>.
  <em>(Use o mouse para controlar os flippers)</em></span>
</div>
""", unsafe_allow_html=True)