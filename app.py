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
import mimetypes

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

# --- Função do Servidor HTTP com MIME types corretos ---
def start_http_server_thread(directory_to_serve: str, port: int):
   class MIMEFixedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
       def log_message(self, format, *args):
           pass
       
       def guess_type(self, path):
           mimetype, encoding = super().guess_type(path)
           
           # Fix MIME types para WebAssembly e JavaScript
           if path.endswith('.wasm'):
               return 'application/wasm', encoding
           elif path.endswith('.js'):
               return 'application/javascript', encoding
           elif path.endswith('.html'):
               return 'text/html', encoding
           elif path.endswith('.css'):
               return 'text/css', encoding
           elif path.endswith('.png'):
               return 'image/png', encoding
           elif path.endswith('.jpg') or path.endswith('.jpeg'):
               return 'image/jpeg', encoding
           elif path.endswith('.gif'):
               return 'image/gif', encoding
           elif path.endswith('.svg'):
               return 'image/svg+xml', encoding
           elif path.endswith('.json'):
               return 'application/json', encoding
           
           return mimetype, encoding
       
       def end_headers(self):
           # Adicionar headers CORS para produção
           self.send_header('Access-Control-Allow-Origin', '*')
           self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
           self.send_header('Access-Control-Allow-Headers', 'Content-Type')
           self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
           self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
           super().end_headers()

   handler = partial(MIMEFixedHTTPRequestHandler, directory=directory_to_serve)
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

# Iniciar servidor se necessário
if not st.session_state.python_server_thread_launched_final_ux:
   st.session_state.python_server_thread_launched_final_ux = True
   st.session_state.python_server_init_error_final_ux = None
   
   server_thread = threading.Thread(
       target=start_http_server_thread,
       args=(game_files_directory, LOCAL_GAME_SERVER_PORT),
       daemon=True
   )
   server_thread.start()
   time.sleep(2)
   st.rerun()

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
       # Detectar se está em produção ou local
       try:
           import socket
           hostname = socket.getfqdn()
           is_local = 'localhost' in hostname or '127.0.0.1' in hostname
       except:
           is_local = False
       
       # Determinar URL base
       if is_local:
           base_url = f"http://localhost:{LOCAL_GAME_SERVER_PORT}"
       else:
           # Em produção no Streamlit Cloud, usar URL relativa
           base_url = f"/_stcore/static/{LOCAL_GAME_SERVER_PORT}"
       
       game_url = f"{base_url}/{GAME_HTML_ENTRY_POINT}"
       
       # Embed do jogo com configurações de segurança para WASM
       components.html(f"""
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
               .loading {{
                   display: flex;
                   justify-content: center;
                   align-items: center;
                   height: 100vh;
                   color: white;
                   font-family: Arial, sans-serif;
                   font-size: 18px;
               }}
           </style>
       </head>
       <body>
           <div id="loading" class="loading">
               🎮 Carregando Space Cadet Pinball...
           </div>
           <iframe 
               id="gameFrame"
               src="{game_url}" 
               allowfullscreen
               allow="cross-origin-isolated"
               sandbox="allow-scripts allow-same-origin allow-forms"
               style="display: none;"
               onload="document.getElementById('loading').style.display='none'; this.style.display='block';"
               onerror="document.getElementById('loading').innerHTML='⚠️ Erro ao carregar o jogo. Recarregue a página.'"
           ></iframe>
           
           <script>
               // Fallback para timeout de carregamento
               setTimeout(function() {{
                   const loading = document.getElementById('loading');
                   const frame = document.getElementById('gameFrame');
                   if (loading.style.display !== 'none') {{
                       loading.innerHTML = '⚠️ Timeout no carregamento. <br><button onclick="location.reload()">Tentar Novamente</button>';
                   }}
               }}, 15000);
           </script>
       </body>
       </html>
       """, height=680, scrolling=False)
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