import streamlit as st
from app.components.navbar import navbar
from app.database.db import init_db
from app.utils.calculations import calcular_saldo

st.set_page_config(page_title="Gestão da Viagem Europa 2026", layout="wide")

# Navbar superior
navbar()

st.title("🌍 Painel de Controle - Viagem Europa 2026")
st.markdown("Gerencie seu roteiro, orçamento e reservas de forma inteligente e centralizada.")

# Inicializa o banco
init_db()

orcamento_total = st.session_state.get("orcamento_total", 6000)
gastos = st.session_state.get("gastos_totais", 0)
saldo = calcular_saldo(orcamento_total, gastos)

st.metric("💰 Saldo Restante (€)", f"{saldo:.2f}", delta=f"{-gastos:.2f}")
st.progress(gastos / orcamento_total)

st.info("Use o menu lateral para acessar Roteiro, Despesas, Reservas e Relatórios.")

