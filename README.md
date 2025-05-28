# 3D Pinball - Space Cadet, em Python e Streamlit

## 📌 Descrição

Uma aplicação web desenvolvida em Streamlit que hospeda o clássico jogo **3D Pinball - Space Cadet**. A aplicação cria um servidor para servir os arquivos do jogo e apresenta uma interface web.

## 🎮 Características

- **Interface moderna**: Design inspirado no jogo original
- **Servidor HTTP integrado**: Servidor local automático para hospedar os arquivos do jogo
- **Experiência imersiva**: Jogo em navegador web
- **Layout otimizado**: Botão de iniciar centralizado e controle do game no mouse
- **Gerenciamento de estado**: Controle inteligente do estado da aplicação via Streamlit

## 🚀 Como Usar

### Pré-requisitos

- Python 3.7+
- Streamlit
- Arquivos do jogo 3D Pinball

### Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Certifique-se de que os seguintes arquivos estão na raiz do projeto:
   - `index.html` (arquivo principal do jogo)
   - `mesa.png` (imagem de preview da mesa)
   - Todos os outros arquivos necessários do jogo

### Execução

```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
space-cadet-pinball/
├── app.py              # Aplicação principal Streamlit
├── index.html          # Arquivo principal do jogo
├── mesa.png           # Imagem de preview da mesa
├── README.md          # Este arquivo
├── requirements.txt   # Dependências Python
└── [outros arquivos do jogo]
```

## ⚙️ Configurações

### Variáveis Configuráveis (app.py)

- `GAME_HTML_ENTRY_POINT`: Nome do arquivo HTML principal (padrão: "index.html")
- `LOCAL_GAME_SERVER_PORT`: Porta do servidor local (padrão: 8001)
- `APP_TITLE`: Título da aplicação (padrão: "Space Cadet Pinball")
- `PAGE_BACKGROUND_COLOR`: Cor de fundo (padrão: "#3A6EA5")

## 🔧 Funcionalidades Técnicas

### Servidor HTTP Local
- Servidor HTTP silencioso executado em thread separada
- Reutilização automática de endereço para evitar conflitos
- Tratamento de erros com feedback visual

### Interface Streamlit
- CSS customizado para experiência em tela cheia
- Componentes HTML integrados para embedding do jogo
- Sistema de estado para controle de fluxo da aplicação
- Imagens convertidas para base64 para carregamento otimizado

### Gerenciamento de Estado
- `python_server_thread_launched_final_ux`: Controla se o servidor foi iniciado
- `python_server_init_error_final_ux`: Armazena erros de inicialização
- `game_started`: Controla se o jogo foi iniciado pelo usuário

## 🎯 Fluxo da Aplicação

1. **Inicialização**: Verifica arquivos necessários e inicia servidor HTTP
2. **Tela Inicial**: Exibe título, botão de iniciar e preview da mesa
3. **Carregamento**: Ao clicar "Iniciar Jogo", carrega o jogo em iframe
4. **Jogo**: Experiência em tela cheia com controles nativos

## 🛠️ Resolução de Problemas

### Arquivo não encontrado
- Verifique se `index.html` está na raiz do projeto
- Confirme se `mesa.png` existe para o preview

### Erro de porta
- O servidor usa a porta 8001 por padrão
- Certifique-se de que a porta não está em uso
- Modifique `LOCAL_GAME_SERVER_PORT` se necessário

### Problemas de carregamento
- Aguarde alguns segundos após iniciar a aplicação
- Verifique o console Python para mensagens de erro
- Reinicie a aplicação se necessário

## 📝 Requisitos do Sistema

- **Python**: 3.7 ou superior
- **Streamlit**: Versão compatível (ver requirements.txt)
- **Navegador**: Qualquer navegador moderno com suporte a iframes
- **Sistema**: Windows, macOS ou Linux

## 🎮 Sobre o Jogo

O 3D Pinball foi originalmente incluído no Windows e é um dos jogos de pinball mais nostálgicos do PC. Esta implementação web preserva toda a jogabilidade original em um ambiente web.

## 📄 Licença

Este projeto é fornecido como está, para fins educacionais e de entretenimento. Os direitos do jogo 3D Pinball Space Cadet pertencem aos seus respectivos proprietários.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests
- Compartilhar feedback

## 📞 Suporte

Para dúvidas, entre em contato comigo, Ary Ribeiro, via email aryribeiro@gmail.com

---

**Desenvolvido com ❤️ usando Python e Streamlit**

**Fork da Alula:** https://github.com/alula/SpaceCadetPinball/tree/gh-pages
