import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

# --- Configurações Globais ---
APP_TITLE = "🕹️3D Pinball | Space Cadet"
PAGE_BACKGROUND_COLOR = "#3A6EA5"

# --- Estado da Sessão ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# --- Função para converter arquivo para base64 ---
def file_to_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# --- Configuração da Página ---
st.set_page_config(page_title=APP_TITLE, layout="centered", initial_sidebar_state="collapsed")

# Diretório dos arquivos
game_files_directory = Path(__file__).resolve().parent
mesa_image_path = game_files_directory / "mesa.png"
mesa_base64 = file_to_base64(mesa_image_path)

# Preparar recursos do jogo
js_file = game_files_directory / "SpaceCadetPinball.js"
wasm_file = game_files_directory / "SpaceCadetPinball.wasm"
data_file = game_files_directory / "SpaceCadetPinball.data"

js_base64 = file_to_base64(js_file) if js_file.exists() else None
wasm_base64 = file_to_base64(wasm_file) if wasm_file.exists() else None
data_base64 = file_to_base64(data_file) if data_file.exists() else None

# CSS
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

# Verificar arquivos necessários
missing_files = []
if not js_base64:
    missing_files.append("SpaceCadetPinball.js")
if not wasm_base64:
    missing_files.append("SpaceCadetPinball.wasm")
if not data_base64:
    missing_files.append("SpaceCadetPinball.data")

if missing_files:
    st.markdown(f"""
    <div class="error-message">
        <h2>ERRO: Arquivos do jogo não encontrados</h2>
        <p>Arquivos necessários: {', '.join(missing_files)}</p>
        <p>Diretório: {game_files_directory}</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Interface principal
st.markdown(f"""
<div class="game-header">
    <h1 class="game-title">{APP_TITLE}</h1>
</div>
""", unsafe_allow_html=True)

# Botão centralizado
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("▶️ INICIAR JOGO", key="start_game"):
        st.session_state.game_started = True
        st.rerun()

# Conteúdo
if st.session_state.game_started:
    # HTML do jogo otimizado para Streamlit
    game_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title></title>
        <style>
            :root {{
                --ActiveBorder: rgb(212, 208, 200);
                --ActiveTitle: rgb(10, 36, 106);
                --AppWorkspace: rgb(128, 128, 128);
                --Background: rgb(58, 110, 165);
                --ButtonAlternateFace: rgb(192, 192, 192);
                --ButtonDkShadow: rgb(64, 64, 64);
                --ButtonFace: rgb(212, 208, 200);
                --ButtonHilight: rgb(255, 255, 255);
                --ButtonLight: rgb(212, 208, 200);
                --ButtonShadow: rgb(128, 128, 128);
                --ButtonText: rgb(0, 0, 0);
                --GradientActiveTitle: rgb(166, 202, 240);
                --GradientInactiveTitle: rgb(192, 192, 192);
                --GrayText: rgb(128, 128, 128);
                --Hilight: rgb(10, 36, 106);
                --HilightText: rgb(255, 255, 255);
                --HotTrackingColor: rgb(0, 0, 128);
                --InactiveBorder: rgb(212, 208, 200);
                --InactiveTitle: rgb(128, 128, 128);
                --InactiveTitleText: rgb(212, 208, 200);
                --InfoText: rgb(0, 0, 0);
                --InfoWindow: rgb(255, 255, 225);
                --Menu: rgb(212, 208, 200);
                --MenuBar: rgb(192, 192, 192);
                --MenuHilight: rgb(0, 0, 128);
                --MenuText: rgb(0, 0, 0);
                --Scrollbar: rgb(212, 208, 200);
                --TitleText: rgb(255, 255, 255);
                --Window: rgb(255, 255, 255);
                --WindowFrame: rgb(0, 0, 0);
                --WindowText: rgb(0, 0, 0);
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
                width: 100%;
                height: 100%;
                max-width: 100vw;
                max-height: 100vh;
            }}
            
            .window {{
                font-size: 8pt;
                color: var(--WindowText);
                background-color: var(--ButtonFace);
                border: 1px solid var(--ActiveBorder);
                box-shadow: -0.5px -0.5px 0 0.5px var(--ButtonHilight), 0 0 0 1px var(--ButtonShadow), -0.5px -0.5px 0 1.5px var(--ButtonLight), 0 0 0 2px var(--ButtonDkShadow);
                padding-right: 0;
                margin: 0;
                display: auto;
                width: 90%;
                height: 90vh;
            }}
            
            .titlebar {{
                text-align: start;
                margin: 0;
                padding: 1px;
                position: relative;
                overflow: hidden;
                display: flex;
                user-select: none;
                background-color: var(--ActiveTitle);
                background-image: linear-gradient(to right, var(--ActiveTitle), var(--GradientActiveTitle));
                color: var(--TitleText);
            }}
            
            .titlebar-title {{
                display: flex;
                padding: 2px 5px;
                overflow: hidden;
                white-space: nowrap;
                text-overflow: ellipsis;
                flex-grow: 1;
                font-weight: 700;
                align-items: center;
            }}
            
            #status {{
                margin: 20px;
                color: white;
                font-size: 12px;
            }}
            
            #progress {{
                margin: 20px;
                width: 80%;
            }}
        </style>
    </head>
    <body>
        <div class="window active">
            <div class="titlebar">
                <span class="titlebar-title"></span>
            </div>
            <div id="status">Carregando...</div>
            <div>
                <progress id="progress" value="0" max="100" style="display: none;"></progress>
            </div>
            <canvas class="emscripten" id="canvas" oncontextmenu="event.preventDefault()" tabindex="-1"></canvas>
        </div>
        
        <script>
            // Criar blobs dos recursos
            function base64ToBlob(base64, mimeType) {{
                const byteCharacters = atob(base64);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {{
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }}
                const byteArray = new Uint8Array(byteNumbers);
                return new Blob([byteArray], {{type: mimeType}});
            }}
            
            // URLs dos recursos
            const wasmBlob = base64ToBlob('{wasm_base64}', 'application/wasm');
            const dataBlob = base64ToBlob('{data_base64}', 'application/octet-stream');
            const wasmUrl = URL.createObjectURL(wasmBlob);
            const dataUrl = URL.createObjectURL(dataBlob);
            
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
                    }}
                    statusElement.innerHTML = text;
                    if (text === '') {{
                        statusElement.style.display = 'none';
                        progressElement.style.display = 'none';
                    }}
                }},
                totalDependencies: 0,
                monitorRunDependencies: function(left) {{
                    this.totalDependencies = Math.max(this.totalDependencies, left);
                    Module.setStatus(left ? 'Preparando... (' + (this.totalDependencies - left) + '/' + this.totalDependencies + ')' : 'Pronto!');
                }},
                locateFile: function(path, scriptDirectory) {{
                    if (path === 'SpaceCadetPinball.wasm') {{
                        return wasmUrl;
                    }}
                    if (path === 'SpaceCadetPinball.data') {{
                        return dataUrl;
                    }}
                    return scriptDirectory + path;
                }}
            }};
            
            Module.setStatus('Baixando...');
            
            window.onerror = function() {{
                Module.setStatus('Erro - verifique o console');
            }};
            
            // Carregar o JS do jogo
            const jsBlob = base64ToBlob('{js_base64}', 'application/javascript');
            const jsUrl = URL.createObjectURL(jsBlob);
            const script = document.createElement('script');
            script.src = jsUrl;
            script.async = true;
            document.body.appendChild(script);
        </script>
    </body>
    </html>
    """
    
    components.html(game_html, height=600, scrolling=False)
else:
    # Mostrar imagem
    st.markdown(f"""
    <div class="game-content">
        {"<img src='data:image/png;base64," + mesa_base64 + "' class='game-image' alt='Mesa de Pinball'>" if mesa_base64 else "<p style='color: #CCCCCC;'>Imagem mesa.png não encontrada</p>"}
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 20px;">
    <div style="color: white;">
        💬 Por <strong>Ary Ribeiro</strong>. Obs.: fork da Alula. Código original no GitHub: 
        <a href="https://github.com/alula/SpaceCadetPinball/tree/gh-pages" style="color: white;">AQUI</a><br>
        <em>Obs.: Use o mouse p/ controlar</em>
    </div>
</div>
""", unsafe_allow_html=True)