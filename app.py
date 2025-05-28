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
game_files_directory = Path(__file__).resolve().parent

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

# Verificar se arquivos necessários existem
index_html_path = game_files_directory / "index.html"
js_file_path = game_files_directory / "SpaceCadetPinball.js"
wasm_file_path = game_files_directory / "SpaceCadetPinball.wasm"
data_file_path = game_files_directory / "SpaceCadetPinball.data"
mesa_image_path = game_files_directory / "mesa.png"

missing_files = []
if not index_html_path.exists():
    missing_files.append("index.html")
if not js_file_path.exists():
    missing_files.append("SpaceCadetPinball.js")

if missing_files:
    st.markdown(f"""
    <div class="error-message">
        <h2>ERRO: Arquivos não encontrados</h2>
        <p>Os seguintes arquivos estão faltando: {', '.join(missing_files)}</p>
        <p>Diretório: {game_files_directory}</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

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
    # Ler arquivo HTML original
    with open(index_html_path, 'r', encoding='utf-8') as f:
        original_html = f.read()
    
    # Ler arquivo JavaScript
    js_content = ""
    if js_file_path.exists():
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
    
    # Converter arquivos binários para base64
    wasm_base64 = get_base64_file(wasm_file_path) if wasm_file_path.exists() else None
    data_base64 = get_base64_file(data_file_path) if data_file_path.exists() else None
    
    # Criar HTML completo com todos os recursos inline
    game_html = f"""
    <!DOCTYPE html>
    <html lang="en-us">
    <head>
        <meta charset="utf-8">
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
        <title>3D Pinball for Windows - Space Cadet</title>
        <style>
        :root{{--ActiveBorder:rgb(212, 208, 200);--ActiveTitle:rgb(10, 36, 106);--AppWorkspace:rgb(128, 128, 128);--Background:rgb(58, 110, 165);--ButtonAlternateFace:rgb(192, 192, 192);--ButtonDkShadow:rgb(64, 64, 64);--ButtonFace:rgb(212, 208, 200);--ButtonHilight:rgb(255, 255, 255);--ButtonLight:rgb(212, 208, 200);--ButtonShadow:rgb(128, 128, 128);--ButtonText:rgb(0, 0, 0);--GradientActiveTitle:rgb(166, 202, 240);--GradientInactiveTitle:rgb(192, 192, 192);--GrayText:rgb(128, 128, 128);--Hilight:rgb(10, 36, 106);--HilightText:rgb(255, 255, 255);--HotTrackingColor:rgb(0, 0, 128);--InactiveBorder:rgb(212, 208, 200);--InactiveTitle:rgb(128, 128, 128);--InactiveTitleText:rgb(212, 208, 200);--InfoText:rgb(0, 0, 0);--InfoWindow:rgb(255, 255, 225);--Menu:rgb(212, 208, 200);--MenuBar:rgb(192, 192, 192);--MenuHilight:rgb(0, 0, 128);--MenuText:rgb(0, 0, 0);--Scrollbar:rgb(212, 208, 200);--TitleText:rgb(255, 255, 255);--Window:rgb(255, 255, 255);--WindowFrame:rgb(0, 0, 0);--WindowText:rgb(0, 0, 0)}}
        body{{font-family:Tahoma,Geneva,Verdana,sans-serif;background-color:var(--Background);text-align:center;margin:0;padding:0;height:100vh;}}
        textarea.emscripten{{font-family:monospace;width:80%}}
        canvas.emscripten{{border:0 none;background-color:#000}}
        .titlebar{{text-align:start;margin:0;padding:1px;position:relative;overflow:hidden;display:flex;user-select:none}}
        .titlebar .titlebar-icon{{width:16px;height:16px;padding:1px}}
        .titlebar .titlebar-title{{display:flex;padding:0 2px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;flex-grow:1;font-weight:700;align-items:center}}
        .titlebar .titlebar-wincontrols{{display:inline-block;margin:0;padding:1px;min-width:fit-content}}
        .titlebar-wincontrols .buttons-wrapper{{display:inline-block;width:auto;margin:0;padding:1px}}
        .titlebar-wincontrols .spacer{{display:inline-block;margin:0;padding:0;width:2px}}
        .titlebar-wincontrols .button{{display:inline-block;min-width:12px;min-height:10px;width:12px;height:10px;text-align:center;vertical-align:middle;line-height:10px}}
        .window{{font-size:8pt;color:var(--WindowText);background-color:var(--ButtonFace);border:1px solid var(--ActiveBorder);box-shadow:-.5px -.5px 0 .5px var(--ButtonHilight),0 0 0 1px var(--ButtonShadow),-.5px -.5px 0 1.5px var(--ButtonLight),0 0 0 2px var(--ButtonDkShadow);padding-right:0;margin-left:auto;margin-right:auto;display:inline-block}}
        .window.active{{border:1px solid var(--ActiveBorder)}}
        .window.active .titlebar .titlebar-icon{{background-color:var(--ActiveTitle);color:var(--TitleText)}}
        .window.active .titlebar .titlebar-title{{background-color:var(--ActiveTitle);background-image:linear-gradient(to right,var(--ActiveTitle),var(--GradientActiveTitle));color:var(--TitleText)}}
        .window.active .titlebar .titlebar-wincontrols,.window.active .titlebar .titlebar-wincontrols .buttons-wrapper{{background-color:var(--GradientActiveTitle);font-size:8pt;font-weight:700}}
        .button{{margin:2px}}
        .button span.button-content{{display:inline-block}}
        .button:active .button-content{{transform:translate(1px,1px)}}
        .button{{background-color:var(--ButtonFace);color:var(--ButtonText);box-shadow:-.5px -.5px 0 .5px var(--ButtonLight),0 0 0 1px var(--ButtonShadow),-.5px -.5px 0 1.5px var(--ButtonHilight),0 0 0 2px var(--ButtonDkShadow)}}
        .button:active{{box-shadow:-.5px -.5px 0 .5px var(--ButtonShadow),0 0 0 1px var(--ButtonShadow),-.5px -.5px 0 1.5px var(--WindowFrame),0 0 0 2px var(--WindowFrame)}}
        .button svg path{{fill:var(--ButtonText)}}
        .titlebar .button:active{{box-shadow:-.5px -.5px 0 .5px var(--ButtonShadow),0 0 0 1px var(--ButtonLight),-.5px -.5px 0 1.5px var(--ButtonDkShadow),0 0 0 2px var(--ButtonHilight)}}
        #status{{margin:40px 32px}}
        </style>
    </head>
    <body>
        <div class="active window">
            <div class="titlebar">
                <span class="titlebar-title">3D Pinball for Windows - Space Cadet</span>
                <div class="titlebar-wincontrols">
                    <ul class="buttons-wrapper">
                        <li class="button minimize">
                            <svg class="button-content replaced-svg" height="0.104181in" width="0.125017in" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 10">
                                <path d="M 2.00,7.00 C 2.00,7.00 8.00,7.00 8.00,7.00 8.00,7.00 8.00,9.00 8.00,9.00 8.00,9.00 2.00,9.00 2.00,9.00 2.00,9.00 2.00,7.00 2.00,7.00 Z" fill="black" id="Minimize" stroke-width="0" stroke="black"></path>
                            </svg>
                        </li>
                        <li class="button maximize">
                            <svg class="button-content replaced-svg" height="0.104181in" width="0.125017in" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 10">
                                <path d="M 2.00,2.00 C 2.00,2.00 9.00,2.00 9.00,2.00 9.00,2.00 9.00,8.00 9.00,8.00 9.00,8.00 2.00,8.00 2.00,8.00 2.00,8.00 2.00,2.00 2.00,2.00 Z M 1.00,0.00 C 1.00,0.00 1.00,9.00 1.00,9.00 1.00,9.00 10.00,9.00 10.00,9.00 10.00,9.00 10.00,0.00 10.00,0.00 10.00,0.00 1.00,0.00 1.00,0.00 Z" fill="black" id="Maximize" stroke-width="0" stroke="black"></path>
                            </svg>
                        </li>
                        <li class="spacer"></li>
                        <li class="button close">
                            <svg class="button-content replaced-svg" height="10" width="12" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:svg="http://www.w3.org/2000/svg">
                                <g id="layer1" transform="translate(0,-1042.3622)">
                                    <path d="m 2.0025485,1043.3853 2.0198115,0 0,1.0185 0.984011,0 0,0.984 1.985286,0 0,-0.984 1.001274,0 0,-1.0185 2.002548,0 0,1.0013 0,0 0,0 -1.001274,0 0,1.0012 -1.001274,0 0,0.9841 -1.001274,0 0,1.0012 1.001274,0 0,1.0013 1.001274,0 0,1.0013 1.001274,0 0,1.0013 -2.002548,0 0,-1.0013 -1.001274,0 0,-0.984 -1.985286,0 0,0.984 -1.001274,0 0,1.0013 -2.0025485,0 0,-1.0013 1.0012745,0 0,-1.0013 1.001274,0 0,-1.0013 1.001274,0 0,-1.0012 -1.001274,0 0,-0.9841 -1.001274,0 0,-1.0012 -1.0012745,0 0,-1.0186 z" fill="black" id="Close" stroke-width="0"></path>
                                </g>
                            </svg>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="emscripten" id="status">Carregando...</div>
            <div class="emscripten">
                <progress hidden id="progress" max="100" value="0"></progress>
            </div>
            <canvas class="emscripten" id="canvas" oncontextmenu="event.preventDefault()" style="display:none" tabindex="-1"></canvas>
        </div>
        
        <script>
        var statusElement = document.getElementById('status');
        var progressElement = document.getElementById('progress');
        
        // Dados binários embutidos
        var wasmBinary = '{wasm_base64 or ""}';
        var dataBinary = '{data_base64 or ""}';
        
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
            canvas: function() {{
                var canvas = document.getElementById('canvas');
                canvas.addEventListener("webglcontextlost", function(e) {{
                    alert('WebGL context lost. You will need to reload the page.');
                    e.preventDefault();
                }}, false);
                return canvas;
            }}(),
            setStatus: function(text) {{
                if (!Module.setStatus.last) Module.setStatus.last = {{ time: Date.now(), text: '' }};
                if (text === Module.setStatus.last.text) return;
                var m = text.match(/([^(]+)\((\d+(\.\d+)?)\/(\d+)\)/);
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
                Module.setStatus(left ? 'Preparando... (' + (this.totalDependencies-left) + '/' + this.totalDependencies + ')' : 'Todos os downloads completos.');
            }},
            locateFile: function(path, prefix) {{
                if (path.endsWith('.wasm') && wasmBinary) {{
                    return 'data:application/wasm;base64,' + wasmBinary;
                }}
                if (path.endsWith('.data') && dataBinary) {{
                    return 'data:application/octet-stream;base64,' + dataBinary;
                }}
                return prefix + path;
            }}
        }};
        
        Module.setStatus('Carregando...');
        
        window.onerror = function() {{
            Module.setStatus('Exceção lançada, veja o console JavaScript');
            Module.setStatus = function(text) {{
                if (text) Module.printErr('[post-exception status] ' + text);
            }};
        }};
        </script>
        
        <script>
        {js_content}
        </script>
    </body>
    </html>
    """
    
    # Renderizar o jogo
    components.html(game_html, height=700, scrolling=False)
    
else:
    # Mostrar imagem do jogo
    mesa_base64 = get_base64_file(mesa_image_path)
    st.markdown(f"""
    <div class="game-content">
        {"<img src='data:image/png;base64," + mesa_base64 + "' class='game-image' alt='Mesa de Pinball'>" if mesa_base64 else "<p style='color: #CCCCCC;'>Imagem mesa.png não encontrada</p>"}
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 20px;">
  <div style="color: white;">
  💬 Por <strong>Ary Ribeiro</strong>. Obs.: fork da Alula. Código original no GitHub: 
  <a href="https://github.com/alula/SpaceCadetPinball/tree/gh-pages" style="color: white;">AQUI</a><br>
  <em>Obs.: Use o mouse p/ controlar</em>
  </div>
</div>
""", unsafe_allow_html=True)