"""Análise exploratória e estatística (nível participante e nível município).
Saídas: tabelas/figuras em outputs/ e outputs/resumo_analise.md (também usado pelo agente RAG)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
import config as C

sns.set_theme(style="whitegrid")
res = pd.read_parquet(C.BASE_RESULTADOS)
mun = pd.read_parquet(C.BASE_MUNICIPIOS)
L = ["# Resumo da análise dos microdados do ENEM 2025 (gerado automaticamente)\n",
     f"Nível participante: {len(res):,} participantes com notas válidas. Nível município: {len(mun):,} municípios com dados "
     "socioeconômicos (arquivo PARTICIPANTES) e de desempenho (arquivo RESULTADOS). Os dois arquivos não têm chave "
     "individual comum; por isso a relação entre perfil socioeconômico e nota é analisada por município (análise ecológica).\n"]


def salvar(fig, nome):
    fig.tight_layout(); fig.savefig(C.FIGS / nome, dpi=150); plt.close(fig)


# 1) Estatísticas descritivas
desc = res[C.NOTAS + ["NOTA_MEDIA"]].agg(["count", "mean", "median", "min", "max", "std"]).T.round(2)
desc.index = [C.NOMES_NOTAS.get(i, "Nota média") for i in desc.index]
desc.to_csv(C.SAIDAS / "estatisticas_descritivas.csv", encoding="utf-8-sig")
L.append("## Estatísticas descritivas das notas (0 a 1000)\n" + desc.to_markdown() + "\n")
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(res["NOTA_MEDIA"], bins=40, kde=True, ax=ax, color="#2a6f97")
ax.axvline(res["NOTA_MEDIA"].mean(), color="red", ls="--", label="Média"); ax.axvline(res["NOTA_MEDIA"].median(), color="green", ls=":", label="Mediana")
ax.set(title="Distribuição da nota média (participantes)", xlabel="Nota média", ylabel="Participantes"); ax.legend()
salvar(fig, "01_distribuicao_nota_media.png")

# 2) Grupos no nível participante
def comparar(col, nome, arq, ordem=None, filtro=None):
    d = res if filtro is None else res[filtro]
    g = d.groupby(col)["NOTA_MEDIA"].agg(["count", "mean", "median", "std"]).round(2)
    if ordem:
        g = g.reindex([o for o in ordem if o in g.index])
    g.to_csv(C.SAIDAS / f"grupo_{col.lower()}.csv", encoding="utf-8-sig")
    L.append(f"## Nota média por {nome}\n" + g.to_markdown() + "\n")
    fig, ax = plt.subplots(figsize=(8, 4.2))
    sns.boxplot(data=d, x="NOTA_MEDIA", y=col, order=list(g.index), ax=ax, color="#8ecae6", showfliers=False)
    ax.set(title=f"Nota média por {nome}", xlabel="Nota média", ylabel="")
    salvar(fig, arq)

comparar("REDE", "rede (pública x privada)", "02_nota_por_rede.png", filtro=res["REDE"] != "Não informada")
comparar("DEPENDENCIA", "dependência administrativa", "03_nota_por_dependencia.png", ["Federal", "Estadual", "Municipal", "Privada"])
comparar("LOCALIZACAO", "localização da escola", "04_nota_por_localizacao.png", filtro=res["LOCALIZACAO"] != "Não informada")
comparar("UF", "UF da prova", "05_nota_por_uf.png", ordem=list(res.groupby("UF")["NOTA_MEDIA"].mean().sort_values().index))

pub = res.loc[res["REDE"] == "Pública", "NOTA_MEDIA"]; pri = res.loc[res["REDE"] == "Privada", "NOTA_MEDIA"]
t, p = stats.ttest_ind(pri, pub, equal_var=False); u, pu = stats.mannwhitneyu(pri, pub)
d = (pri.mean() - pub.mean()) / ((pri.var() + pub.var()) / 2) ** 0.5
L.append(f"## Teste: escola privada x pública (participantes)\nDiferença de médias: {pri.mean() - pub.mean():.1f} pontos "
         f"(privada {pri.mean():.1f}; pública {pub.mean():.1f}). t de Welch = {t:.2f} (p = {p:.3g}); Mann-Whitney p = {pu:.3g}; d de Cohen = {d:.2f}.\n")

areas = res[res["REDE"] != "Não informada"].groupby("REDE")[C.NOTAS].mean().rename(columns=C.NOMES_NOTAS).round(1)
areas.to_csv(C.SAIDAS / "areas_por_rede.csv", encoding="utf-8-sig")
L.append("## Média por área e rede\n" + areas.to_markdown() + "\n")
fig, ax = plt.subplots(figsize=(8, 4.5)); areas.T.plot.bar(ax=ax, color=["#fb8500", "#219ebc"])
ax.set(title="Média por área e rede", ylabel="Nota"); plt.xticks(rotation=20); salvar(fig, "06_areas_por_rede.png")

comp = res.groupby("REDE")[C.COMPETENCIAS].mean().round(1)
L.append("## Redação: média das competências (0 a 200) por rede\n" + comp.to_markdown() + "\n")

cor = res[C.NOTAS].corr(method="spearman").round(2)
fig, ax = plt.subplots(figsize=(6.5, 5)); sns.heatmap(cor.rename(index=C.NOMES_NOTAS, columns=C.NOMES_NOTAS), annot=True,
                                                     cmap="RdBu_r", center=0, vmin=-1, vmax=1, ax=ax)
ax.set_title("Correlação de Spearman entre áreas"); salvar(fig, "07_correlacao_areas.png")

# 3) Nível município: perfil socioeconômico
socio = ["RENDA_MEDIA_ORD", "PCT_RENDA_ATE_1SM", "PCT_RENDA_ACIMA_5SM", "PCT_MAE_SUPERIOR", "PCT_PAI_SUPERIOR", "PCT_ESCOLA_PRIVADA", "PCT_WIFI", "PCT_COMPUTADOR"]
dm = mun[socio + ["NOTA_MEDIA"]].describe().T.round(2)
dm.to_csv(C.SAIDAS / "estatisticas_municipios.csv", encoding="utf-8-sig")
L.append("## Municípios: estatísticas do perfil socioeconômico e da nota média\n" + dm.to_markdown() + "\n")
cm = mun[socio + ["NOTA_MEDIA"]].corr(method="spearman").round(2)
cm.to_csv(C.SAIDAS / "correlacao_municipios.csv", encoding="utf-8-sig")
fig, ax = plt.subplots(figsize=(7.5, 6)); sns.heatmap(cm, annot=True, cmap="RdBu_r", center=0, vmin=-1, vmax=1, ax=ax)
ax.set_title("Correlação de Spearman (municípios)"); salvar(fig, "08_correlacao_municipios.png")
linhas = []
for v in socio:
    r_, p_ = stats.spearmanr(mun[v], mun["NOTA_MEDIA"]); linhas.append(f"- {v}: Spearman = {r_:.2f} (p = {p_:.3g})")
L.append("## Correlação município: perfil socioeconômico x nota média\n" + "\n".join(linhas) +
         "\n\nInterpretação cautelosa: são associações entre municípios (nível ecológico); não valem automaticamente para indivíduos.\n")
fig, ax = plt.subplots(figsize=(7, 5))
sns.scatterplot(data=mun, x="RENDA_MEDIA_ORD", y="NOTA_MEDIA", size="N_RESULTADOS", sizes=(10, 150), alpha=.5, ax=ax, legend=False)
sns.regplot(data=mun, x="RENDA_MEDIA_ORD", y="NOTA_MEDIA", scatter=False, color="red", ax=ax)
ax.set(title="Renda média do município x nota média", xlabel="Renda média (código ordinal)", ylabel="Nota média")
salvar(fig, "09_renda_vs_nota_municipios.png")

por_uf = mun.groupby("UF")[["RENDA_MEDIA_ORD", "NOTA_MEDIA", "PCT_ESCOLA_PRIVADA"]].mean().round(2).sort_values("NOTA_MEDIA")
por_uf.to_csv(C.SAIDAS / "municipios_por_uf.csv", encoding="utf-8-sig")
L.append("## Média dos municípios por UF\n" + por_uf.to_markdown() + "\n")

(C.SAIDAS / "resumo_analise.md").write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
