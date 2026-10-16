import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Coleta Rápida - SAC & PRICE", page_icon="⚡", layout="centered")

# O grande truque aqui é usar o 'type' do botão do Streamlit para aplicar o CSS infalivelmente, 
# e usar o seletor universal (*) dentro do botão para garantir que o texto não seja sobrescrito.
st.markdown("""
    <style>
    /* Aumentando drasticamente o tamanho do botão */
    div.stButton > button {
        height: 250px !important; /* Altura massiva */
        border-radius: 40px !important;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.4) !important;
        transition: all 0.1s ease-in-out !important;
    }
    div.stButton > button:active {
        transform: scale(0.92) !important;
    }

    /* TRUQUE: Botão SAC será do tipo "primary" -> ROXO */
    button[data-testid="baseButton-primary"] {
        background-color: #8A2BE2 !important; 
        border: 4px solid #5a1299 !important;
    }
    /* Força fonte GIGANTE em qualquer texto dentro do botão primário */
    button[data-testid="baseButton-primary"] p,
    button[data-testid="baseButton-primary"] span,
    button[data-testid="baseButton-primary"] div,
    button[data-testid="baseButton-primary"] * {
        font-size: 85px !important;
        font-weight: 1000 !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
        text-transform: uppercase !important;
    }

    /* TRUQUE: Botão PRICE será do tipo "secondary" -> VERDE */
    button[data-testid="baseButton-secondary"] {
        background-color: #2E7D32 !important; 
        border: 4px solid #1a4d1e !important;
    }
    /* Força fonte GIGANTE em qualquer texto dentro do botão secundário */
    button[data-testid="baseButton-secondary"] p,
    button[data-testid="baseButton-secondary"] span,
    button[data-testid="baseButton-secondary"] div,
    button[data-testid="baseButton-secondary"] * {
        font-size: 85px !important;
        font-weight: 1000 !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
        text-transform: uppercase !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Coleta Rápida")

if "log" not in st.session_state:
    st.session_state.log = []

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # A mágica acontece aqui: type="primary" aciona o CSS do Roxo
    if st.button("SAC", type="primary", use_container_width=True, key="btn_sac"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.log.append({"Categoria": "SAC", "Timestamp": timestamp})
        st.toast("Registrado: SAC!", icon="✅")

with col2:
    # A mágica acontece aqui: type="secondary" aciona o CSS do Verde
    if st.button("PRICE", type="secondary", use_container_width=True, key="btn_price"):
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
            file_name=f"coleta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with c2:
        if st.button("🗑️ Limpar Histórico", use_container_width=True, key="btn_clear"):
            st.session_state.log = []
            st.rerun()
else:
    st.info("Nenhum dado coletado ainda.")
