import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
from database.models import fetch_jobs

st.set_page_config(page_title="Python Job Dashboard", layout="wide")
st.title("Vagas de Desenvolvedor Python")

if st.button("Atualizar Vagas"):
    st.info("Execute o scraper separadamente. Depois atualize a página.")

data = fetch_jobs()

if not data:
    st.warning("Nenhuma vaga encontrada.")
    st.stop()

df = pd.DataFrame(data, columns=["Título", "Empresa", "Localização", "Data"])
df["Data"] = pd.to_datetime(df["Data"])


col1, col2 = st.columns(2)
with col1:
    st.metric("Total de Vagas", len(df))
with col2:
    st.metric("Empresas Únicas", df["Empresa"].nunique())


st.subheader("Vagas por Localização")
st.bar_chart(df["Localização"].value_counts(), width="stretch")

st.subheader("Evolução de Vagas ao Longo do Tempo")
jobs_by_date = df.groupby(df["Data"].dt.date).size()
st.line_chart(jobs_by_date, width="stretch")

st.subheader("Tabela de Vagas")
st.dataframe(df)
