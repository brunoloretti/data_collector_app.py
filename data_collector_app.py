import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Coleta Rápida - SAC & PRICE", page_icon="⚡", layout="centered")

# Forçando o tamanho gigante extremo nas fontes e cores sólidas de fundo
st.markdown("""
    <style>
    /* Estilo geral e tamanho monstruoso para os botões e textos */
    div.stButton > button {
        width: 100% !important;
        height: 180px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.35) !important;
        transition: 0.1s ease-in-out !important;
    }
    div.stButton > button:active {
        transform: scale(0.94) !important;
    }

    /* Coluna 1: SAC -> Fundo Roxo e Texto GIGANTE */
    div[data-testid="column"]:nth-of-type(1) button {
        background-color: #7B1FA2 !important;
    }
    div[data-testid="column"]:nth-of-type(1) button div p, 
    div[data-testid="column"]:nth-of-type(1) button p,
    div[data-testid="column"]:nth-of-type(1) button span {
        font-size: 55px !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
    }

    /* Coluna 2: PRICE -> Fundo Verde e Texto GIGANTE */
    div[data-testid="column"]:nth-of-type(2) button {
        background-color: #1B5E20 !important;
    }
    div[data-testid="column"]:nth-of-type(2) button div p, 
    div[data-testid="column"]:nth-of-type(2) button p,
    div[data-testid="column"]:nth-of-type(2) button span {
        font-size: 55px !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Coleta Rápida: SAC & PRICE")
st.markdown("Toque no botão correspondente para registrar o dado instantaneamente.")

if "log" not in st.session_state:
    st.session_state.log = []

st.markdown("<br>", unsafe_allow_html=True)

# Organizar os dois botões gigantes lado a lado
col1, col2 = st.columns(2)

with col1:
    if st.button("SAC", use_container_width=True, key="btn_sac"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.log.append({"Categoria": "SAC", "Timestamp": timestamp})
        st.toast("Registrado: SAC!", icon="✅")

with col2:
    if st.button("PRICE", use_container_width=True, key="btn_price"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.log.append({"Categoria": "PRICE", "Timestamp": timestamp})
        st.toast("Registrado: PRICE!", icon="✅")

st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("📊 Contagem Atual")

if st.session_state.log:
    df_log = pd.DataFrame(st.session_state.log)
    counts = df_log["Categoria"].value_counts().reset_index()
    counts.columns = ["Categoria", "Total"]
    st.dataframe(counts, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        csv = df_log.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados (CSV)",
            data=csv,
            file_name=f"coleta_sac_price_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with c2:
        if st.button("🗑️ Limpar Histórico", use_container_width=True, key="btn_clear"):
            st.session_state.log = []
            st.rerun()
else:
    st.info("Nenhum dado coletado ainda. Toque em SAC ou PRICE acima para começar.")
