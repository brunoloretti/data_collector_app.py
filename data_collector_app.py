import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Coleta Rápida por Toque", page_icon="⚡", layout="centered")

st.title("⚡ Coleta Rápida de Dados")
st.markdown("Toque nos botões abaixo para registrar ocorrências instantaneamente.")

if "categories" not in st.session_state:
    st.session_state.categories = ["Categoria A", "Categoria B", "Categoria C"]

if "log" not in st.session_state:
    st.session_state.log = []

with st.expander("⚙️ Configurar Categorias"):
    new_cat = st.text_input("Adicionar nova categoria:")
    if st.button("Adicionar") and new_cat:
        if new_cat not in st.session_state.categories:
            st.session_state.categories.append(new_cat)
            st.rerun()
    
    cat_to_remove = st.selectbox("Remover categoria:", [""] + st.session_state.categories)
    if st.button("Remover") and cat_to_remove:
        st.session_state.categories.remove(cat_to_remove)
        st.rerun()

st.divider()

st.subheader("Toque para Registrar:")
if st.session_state.categories:
    cols = st.columns(len(st.session_state.categories))
    for i, cat in enumerate(st.session_state.categories):
        col = cols[i % len(cols)]
        with col:
            if st.button(f"➕ {cat}", use_container_width=True, key=f"btn_{cat}"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.log.append({"Categoria": cat, "Timestamp": timestamp})
                st.toast(f"Registrado: {cat}!", icon="✅")

st.divider()

st.subheader("📊 Contagem Atual")
if st.session_state.log:
    df_log = pd.DataFrame(st.session_state.log)
    counts = df_log["Categoria"].value_counts().reset_index()
    counts.columns = ["Categoria", "Total"]
    st.dataframe(counts, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        csv = df_log.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados (CSV)",
            data=csv,
            file_name=f"coleta_dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        if st.button("🗑️ Limpar Histórico", use_container_width=True):
            st.session_state.log = []
            st.rerun()
else:
    st.info("Nenhum dado coletado ainda. Toque em um botão acima para começar.")