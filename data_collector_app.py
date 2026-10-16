import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Coleta Rápida - SAC & PRICE", page_icon="⚡", layout="centered")

# Estilização visual para botões gigantes e coloridos (Roxo para SAC e Verde para PRICE)
st.markdown("""
    <style>
    /* Aumentar o tamanho e espaçamento dos botões principais */
    div.stButton > button {
        font-size: 36px !important;
        font-weight: 800 !important;
        height: 140px !important;
        border-radius: 24px !important;
        border: none !important;
        color: white !important;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.25);
        transition: 0.1s ease-in-out;
    }
    div.stButton > button:active {
        transform: scale(0.96);
    }

    /* Cores específicas para cada botão via chave */
    button[key="btn_sac"] {
        background-color: #8A2BE2 !important; /* Roxo vibrante */
    }
    button[key="btn_price"] {
        background-color: #2E7D32 !important; /* Verde vibrante */
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Coleta Rápida: SAC & PRICE")
st.markdown("Toque no botão correspondente para registrar o dado instantaneamente.")

if "log" not in st.session_state:
    st.session_state.log = []

st.markdown("<br>", unsafe_allow_html=True)

# Organizar os dois botões grandes lado a lado
col1, col2 = st.columns(2)

with col1:
    if st.button("📢 SAC", use_container_width=True, key="btn_sac"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.log.append({"Categoria": "SAC", "Timestamp": timestamp})
        st.toast("Registrado: SAC!", icon="✅")

with col2:
    if st.button("💰 PRICE", use_container_width=True, key="btn_price"):
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
