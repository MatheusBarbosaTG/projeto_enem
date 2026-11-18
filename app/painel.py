"""Painel analítico + agente de dados (Streamlit).  Execução: streamlit run app/painel.py"""
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "rag"))
import config as C  # noqa: E402

st.set_page_config(page_title="ENEM 2025 – Desempenho educacional", layout="wide")


@st.cache_data
def carregar():
    res = pd.read_parquet(C.BASE_RESULTADOS, columns=["UF", "REDE", "DEPENDENCIA", "LOCALIZACAO", "NOTA_MEDIA"] + C.NOTAS)
    return res, pd.read_parquet(C.BASE_MUNICIPIOS)


res, mun = carregar()
aba_p, aba_m, aba_ml, aba_a = st.tabs(["📊 Participantes", "🏙️ Municípios", "🤖 Machine Learning", "💬 Agente de dados"])

with aba_p:
    st.title("Desempenho no ENEM 2025")
    st.caption("Notas por participante, com rede/dependência da escola e UF (o arquivo de resultados não contém dados socioeconômicos individuais).")
    with st.sidebar:
        st.header("Filtros")
        ufs = st.multiselect("UF da prova", sorted(res["UF"].unique()))
        rede = st.multiselect("Rede", sorted(res["REDE"].unique()))
        dep = st.multiselect("Dependência", sorted(res["DEPENDENCIA"].unique()))
        loc = st.multiselect("Localização da escola", sorted(res["LOCALIZACAO"].unique()))
    f = res
    for col, sel in [("UF", ufs), ("REDE", rede), ("DEPENDENCIA", dep), ("LOCALIZACAO", loc)]:
        if sel:
            f = f[f[col].isin(sel)]
    if f.empty:
        st.warning("Nenhum registro com esses filtros."); st.stop()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Participantes", f"{len(f):,}".replace(",", "."))
    c2.metric("Nota média", f"{f['NOTA_MEDIA'].mean():.1f}")
    c3.metric("Mediana", f"{f['NOTA_MEDIA'].median():.1f}")
    pr, pu = f.loc[f.REDE == "Privada", "NOTA_MEDIA"], f.loc[f.REDE == "Pública", "NOTA_MEDIA"]
    c4.metric("Privada − Pública", f"{pr.mean() - pu.mean():.1f} pts" if len(pr) and len(pu) else "—")
    amostra = f.sample(min(len(f), 200_000), random_state=1)
    a, b = st.columns(2)
    a.plotly_chart(px.histogram(amostra, x="NOTA_MEDIA", nbins=40, color="REDE", barmode="overlay", opacity=.65,
                                title="Distribuição da nota média"), use_container_width=True)
    d = f.groupby("DEPENDENCIA")["NOTA_MEDIA"].mean().reset_index()
    b.plotly_chart(px.bar(d, x="DEPENDENCIA", y="NOTA_MEDIA", title="Nota média por dependência"), use_container_width=True)
    a, b = st.columns(2)
    ar = f.groupby("REDE")[C.NOTAS].mean().rename(columns=C.NOMES_NOTAS).reset_index().melt("REDE")
    a.plotly_chart(px.bar(ar, x="variable", y="value", color="REDE", barmode="group", labels={"variable": "Área", "value": "Nota média"},
                          title="Média por área e rede"), use_container_width=True)
    u = f.groupby("UF")["NOTA_MEDIA"].mean().sort_values().reset_index()
    b.plotly_chart(px.bar(u, x="NOTA_MEDIA", y="UF", orientation="h", title="Nota média por UF"), use_container_width=True)

with aba_m:
    st.header("Perfil socioeconômico x desempenho por município")
    st.caption("Análise ecológica: associações entre municípios, não entre indivíduos.")
    ufm = st.multiselect("UF", sorted(mun["UF"].unique()), key="ufm")
    m = mun[mun["UF"].isin(ufm)] if ufm else mun
    xvar = st.selectbox("Variável socioeconômica", ["RENDA_MEDIA_ORD", "PCT_RENDA_ATE_1SM", "PCT_RENDA_ACIMA_5SM",
                                                   "PCT_MAE_SUPERIOR", "PCT_PAI_SUPERIOR", "PCT_ESCOLA_PRIVADA", "PCT_WIFI", "PCT_COMPUTADOR"])
    st.plotly_chart(px.scatter(m, x=xvar, y="NOTA_MEDIA", color="UF", size="N_RESULTADOS", hover_name="MUNICIPIO", opacity=.6,
                               trendline="ols" if len(m) > 2 else None, title=f"{xvar} x nota média"), use_container_width=True)
    st.dataframe(m.sort_values("NOTA_MEDIA", ascending=False)[["MUNICIPIO", "UF", "N_RESULTADOS", "NOTA_MEDIA", xvar]].round(1))

with aba_ml:
    st.header("Resultados de Machine Learning")
    arq = C.SAIDAS / "resultados_ml.md"
    st.markdown(arq.read_text(encoding="utf-8") if arq.exists() else "Execute `src/03_machine_learning.py`.")
    for img in ["10_importancia_variaveis.png", "12_clusters.png"]:
        if (C.FIGS / img).exists():
            st.image(str(C.FIGS / img))

with aba_a:
    st.header("Agente de dados (RAG)")
    st.caption("Responde com base nos documentos coletados e no resumo da análise, citando as fontes.")
    try:
        from agente import responder  # noqa: E402
        pergunta = st.text_input("Pergunta", placeholder="Ex.: Por que a renda se associa ao desempenho no ENEM?")
        if pergunta:
            with st.spinner("Buscando nos documentos..."):
                resp, fontes = responder(pergunta)
            st.markdown(resp)
            with st.expander("Trechos recuperados"):
                for fnt in fontes:
                    st.markdown(f"**{fnt['titulo']}** — {fnt['fonte']} ([link]({fnt['link']}))\n\n> {fnt['trecho'][:500]}...")
    except Exception as e:
        st.error(f"Agente indisponível: {e}")
