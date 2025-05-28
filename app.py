import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

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

# --- Função para ler arquivo como base64 ---
def get_base64_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="collapsed")

# Obter diretório dos arquivos do jogo
game_files_directory = Path(__file__).resolve().parent
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
        overflow: hidden !important;
    }}
    
    .block-container {{
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100vw !important;
        height: 100vh !important;
    }}
    
    header[data-testid="stHeader"], 
    .stDeployButton,
    footer,
    .stDecoration {{
        display: none !important;
    }}
    
    .game-header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        align-items: center;
        background: linear-gradient(180deg, {PAGE_BACKGROUND_COLOR} 0%, rgba(58, 110, 165, 0.95) 100%);
        color: #FFFFFF;
        text-align: center;
        padding: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}
    
    .game-title {{
        font-size: 32px;
        margin: 0 0 15px 0;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        font-weight: bold;
    }}
    
    .game-content {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: {PAGE_BACKGROUND_COLOR};
        z-index: 1;
    }}
    
    .game-image {{
        max-width: 80vw;
        max-height: 70vh;
        width: auto;
        height: auto;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }}
    
    .game-image:hover {{
        transform: scale(1.02);
    }}
    
    .stButton > button {{
        padding: 12px 25px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
        background: linear-gradient(45deg, #0066CC, #0099FF) !important;
        border: none !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(0, 100, 200, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(45deg, #0055AA, #0088EE) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 100, 200, 0.5) !important;
    }}
    
    .stButton {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}
    
    .game-container {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 2000;
        background-color: #000000;
    }}
    
    .credits {{
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        color: white;
        font-size: 12px;
        text-align: center;
        z-index: 1001;
        background: rgba(0,0,0,0.5);
        padding: 5px 15px;
        border-radius: 15px;
        backdrop-filter: blur(5px);
    }}
    
    .credits a {{
        color: #87CEEB;
        text-decoration: none;
    }}
    
    .credits a:hover {{
        color: #FFFFFF;
        text-decoration: underline;
    }}
</style>
""", unsafe_allow_html=True)

# --- Função para criar HTML do jogo embedado ---
def create_embedded_game_html():
    # Ler arquivos necessários
    index_html_path = game_files_directory / "index.html"
    js_file_path = game_files_directory / "SpaceCadetPinball.js"
    wasm_file_path = game_files_directory / "SpaceCadetPinball.wasm"
    data_file_path = game_files_directory / "SpaceCadetPinball.data"
    
    # Verificar se arquivos existem
    if not index_html_path.exists():
        return None
        
    # Ler conteúdo do HTML
    with open(index_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Converter arquivos binários para base64
    js_base64 = get_base64_file(js_file_path) if js_file_path.exists() else None
    wasm_base64 = get_base64_file(wasm_file_path) if wasm_file_path.exists() else None
    data_base64 = get_base64_file(data_file_path) if data_file_path.exists() else None
    
    # Criar HTML modificado para funcionar embedado
    embedded_html = f"""
    <!DOCTYPE html>
    <html lang="en-us">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>3D Pinball for Windows - Space Cadet</title>
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
            html, body {{
                margin: 0;
                padding: 0;
                width: 100vw;
                height: 100vh;
                overflow: hidden;
                font-family: Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--Background);
            }}
            .window {{
                width: 100vw;
                height: 100vh;
                border: none;
                box-shadow: none;
                background-color: var(--ButtonFace);
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
            }}
            .titlebar {{
                display: none;
            }}
            canvas.emscripten {{
                border: 0 none;
                background-color: #000;
                width: 100% !important;
                height: 100% !important;
                display: block !important;
            }}
            #status {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-size: 16px;
                z-index: 1000;
            }}
            #progress {{
                position: absolute;
                top: 60%;
                left: 50%;
                transform: translateX(-50%);
                width: 300px;
                z-index: 1000;
            }}
        </style>
    </head>
    <body>
        <div class="active window">
            <div id="status">Carregando...</div>
            <div class="emscripten">
                <progress hidden id="progress" value="0" max="100"></progress>
            </div>
            <canvas class="emscripten" id="canvas" oncontextmenu="event.preventDefault()" tabindex="-1"></canvas>
        </div>
        
        <script>
            var statusElement = document.getElementById('status');
            var progressElement = document.getElementById('progress');
            
            var Module = {{
                preRun: [],
                postRun: [],
                print: function() {{
                    var element = document.getElementById('output');
                    if (element) element.value = '';
                    return function(text) {{
                        if (arguments.length > 1) text = Array.prototype.slice.call(arguments).join(' ');
                        console.log(text);
                    }};
                }}(),
                printErr: function(text) {{
                    if (arguments.length > 1) text = Array.prototype.slice.call(arguments).join(' ');
                    console.error(text);
                }},
                canvas: (function() {{
                    var canvas = document.getElementById('canvas');
                    canvas.addEventListener("webglcontextlost", function(e) {{
                        console.error('WebGL context lost. You will need to reload the page.');
                        e.preventDefault();
                    }}, false);
                    return canvas;
                }})(),
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
                        progressElement.value = parseInt(m[2])*100;
                        progressElement.max = parseInt(m[4])*100;
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
                    Module.setStatus(left ? 'Preparando... (' + (this.totalDependencies-left) + '/' + this.totalDependencies + ')' : 'Download completo.');
                }},
                locateFile: function(path, prefix) {{
                    if (path.endsWith('.wasm')) {{
                        return 'data:application/wasm;base64,{wasm_base64 or ""}';
                    }}
                    if (path.endsWith('.data')) {{
                        return 'data:application/octet-stream;base64,{data_base64 or ""}';
                    }}
                    return prefix + path;
                }}
            }};
            
            Module.setStatus('Baixando...');
            window.onerror = function() {{
                Module.setStatus('Exceção capturada, verifique o console JavaScript');
                Module.setStatus = function(text) {{
                    if (text) Module.printErr('[post-exception status] ' + text);
                }};
            }};
        </script>
        
        {f'<script>{{atob("{js_base64}").split("").map(c => String.fromCharCode(c.charCodeAt(0))).join("")}}</script>' if js_base64 else '<script src="SpaceCadetPinball.js"></script>'}
    </body>
    </html>
    """
    
    return embedded_html

# --- Interface Principal ---
if not st.session_state.game_started:
    # Header com título e botão
    st.markdown(f"""
    <div class="game-header">
        <h1 class="game-title">{APP_TITLE}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão centralizado
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 INICIAR JOGO", key="start_game"):
            st.session_state.game_started = True
            st.rerun()
    
    # Mostrar imagem do jogo como preview
    if mesa_base64:
        st.markdown(f"""
        <div class="game-content">
            <img src='data:image/png;base64,{mesa_base64}' class='game-image' alt='Mesa de Pinball'>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="game-content">
            <p style='color: #CCCCCC; font-size: 18px;'>Preparando o jogo...</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Mostrar o jogo
    game_html = create_embedded_game_html()
    
    if game_html:
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        components.html(game_html, height=800, scrolling=False)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="game-content">
            <div style="color: #FF6B6B; text-align: center;">
                <h2>Erro: Arquivos do jogo não encontrados</h2>
                <p>Verifique se todos os arquivos estão no diretório correto.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Créditos fixos
st.markdown("""
<div class="credits">
    💬 Por <strong>Ary Ribeiro</strong> | Fork da <a href="https://github.com/alula/SpaceCadetPinball/tree/gh-pages" target="_blank">Alula</a><br>
    <em>Use o mouse para controlar os flippers</em>
</div>
""", unsafe_allow_html=True)