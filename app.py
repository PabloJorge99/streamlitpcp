import streamlit as st
import importlib
import os

PAGINAS_DIR = "paginas"

def carregar_paginas():
    paginas = {}
    for arquivo in os.listdir(PAGINAS_DIR):
        if arquivo.endswith(".py") and not arquivo.startswith("_"):
            nome = arquivo[:-3]
            try:
                modulo = importlib.import_module(f"{PAGINAS_DIR}.{nome}")
                paginas[nome] = modulo
            except Exception as e:
                st.error(f"Erro ao carregar {nome}: {str(e)}")
    return paginas

# Configuração da página
st.set_page_config(
    page_title="Controle PCP",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega páginas
paginas = carregar_paginas()

# Sidebar
with st.sidebar:
    st.title("🏭 Controle PCP")
    st.markdown("---")
    
    # Botão Início
    if st.button("🏠 Página Inicial", key="inicio"):
        st.session_state.pagina = "Inicio"
    st.markdown("---")

    
    st.subheader("📝 Acompanhar Pedidos")
    if st.button("📝 Pedidos", key="pedidos"):
        st.session_state.pagina = "Pedidos"
    if st.button("📝 Pedidos Paralelos", key="pedidos_paralelos"):
        st.session_state.pagina = "Pedidos_Paralelos"
    st.markdown("---")


    st.subheader("🔎 Controle")
    if st.button("📚 Lotes", key="lotes"):
        st.session_state.pagina = "Lotes"
    if st.button("🧾 Ofs", key="ofs"):
        st.session_state.pagina = "Ofs"
    if st.button("📦 Estoque", key="estoque"):
        st.session_state.pagina = "Estoque"

    st.subheader("📋 Planejamento")
    if st.button("📋 Programação", key="programação"):
        st.session_state.pagina ="Planejamento"
    
    st.subheader("🏭 Produção")
    if st.button("📊 Produção Geral", key="producao"):
        st.session_state.pagina = "Producao_Geral"
    if st.button("⚙️ Usinagem", key="usinagem"):
        st.session_state.pagina = "Usinagem"
    if st.button("🪚 Estamparia", key="estamparia"):
        st.session_state.pagina = "Estamparia"
    if st.button("🔧 Solda", key="solda"):
        st.session_state.pagina = "Solda"
    if st.button("🧩 Montagem", key="montagem"):
        st.session_state.pagina = "Montagem"

# Página padrão
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# Carrega a página selecionada
if st.session_state.pagina in paginas:
    paginas[st.session_state.pagina].main()
else:
    st.error("Página não encontrada!")