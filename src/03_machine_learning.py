"""Machine Learning no nível município: (1) regressão da nota média municipal a partir do perfil
socioeconômico; (2) clusterização de municípios. Validação cruzada 5-fold (poucos milhares de linhas).
Justificativa de NÃO modelar no nível individual: os arquivos não permitem ligar o perfil socioeconômico à nota de
cada participante, e só com rede/UF/localização o modelo seria pouco informativo."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score, silhouette_score
from sklearn.model_selection import KFold, cross_val_predict, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import config as C

mun = pd.read_parquet(C.BASE_MUNICIPIOS)
num = ["RENDA_MEDIA_ORD", "PCT_RENDA_ATE_1SM", "PCT_RENDA_ACIMA_5SM", "PCT_MAE_SUPERIOR", "PCT_PAI_SUPERIOR",
       "PCT_FEMININO", "PCT_PRETA_PARDA", "PCT_ESCOLA_PRIVADA", "PCT_WIFI", "PCT_COMPUTADOR"]
mun[num + ["NOTA_MEDIA"]] = mun[num + ["NOTA_MEDIA"]].astype(float)
X, y = mun[num + ["UF"]], mun["NOTA_MEDIA"]
pre = ColumnTransformer([("n", StandardScaler(), num), ("u", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["UF"])])
modelos = {"Baseline (média)": DummyRegressor(), "Regressão Ridge": Ridge(alpha=1.0),
           "Gradient Boosting": HistGradientBoostingRegressor(random_state=42, max_iter=200, learning_rate=.05)}
kf = KFold(5, shuffle=True, random_state=42)
S = ["# Resultados de Machine Learning (nível município)\n",
     f"Alvo: nota média do município. {len(mun):,} municípios; validação cruzada 5-fold.\n",
     "## Regressão\n| Modelo | MAE (pontos) | R² |\n|---|---|---|"]
preds = {}
for nome, m in modelos.items():
    pr = cross_val_predict(make_pipeline(pre, m), X, y, cv=kf)
    preds[nome] = pr
    S.append(f"| {nome} | {mean_absolute_error(y, pr):.1f} | {r2_score(y, pr):.3f} |")

# Importância por permutação (modelo ajustado em treino, avaliado em teste)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.25, random_state=1)
gb = make_pipeline(pre, modelos["Gradient Boosting"]).fit(Xtr, ytr)
pi = permutation_importance(gb, Xte, yte, n_repeats=10, random_state=1, scoring="r2")
imp = pd.Series(pi.importances_mean, index=X.columns).sort_values()
fig, ax = plt.subplots(figsize=(7, 4.5)); imp.plot.barh(ax=ax, color="#2a6f97")
ax.set(title="Importância das variáveis (queda no R² ao embaralhar)"); fig.tight_layout(); fig.savefig(C.FIGS / "10_importancia_variaveis.png", dpi=150); plt.close(fig)
S.append("\n## Importância das variáveis\n" + imp.sort_values(ascending=False).round(4).to_frame("importancia").to_markdown())

fig, ax = plt.subplots(figsize=(5.5, 5)); pr = preds["Gradient Boosting"]
ax.scatter(y, pr, s=8, alpha=.4); lim = [y.min(), y.max()]; ax.plot(lim, lim, "r--")
ax.set(xlabel="Real", ylabel="Previsto (CV)", title="Nota média municipal: real x previsto"); fig.tight_layout()
fig.savefig(C.FIGS / "11_real_vs_previsto.png", dpi=150); plt.close(fig)

# Clusterização de municípios por perfil socioeconômico
Z = StandardScaler().fit_transform(mun[num])
sil = {k: silhouette_score(Z, KMeans(k, n_init=5, random_state=0).fit_predict(Z)) for k in range(2, 7)}
k = max(sil, key=sil.get)
mun["CLUSTER"] = KMeans(k, n_init=10, random_state=0).fit_predict(Z)
perfil = mun.groupby("CLUSTER")[num + ["NOTA_MEDIA"]].mean().round(1)
perfil["municípios"] = mun["CLUSTER"].value_counts().sort_index()
perfil.to_csv(C.SAIDAS / "perfis_clusters.csv", encoding="utf-8-sig")
mun[["CO_MUNICIPIO", "MUNICIPIO", "UF", "CLUSTER"]].to_csv(C.SAIDAS / "municipios_clusters.csv", index=False, encoding="utf-8-sig")
S.append(f"\n## Clusterização (KMeans) de municípios\nSilhouette por k: { {a: round(b, 3) for a, b in sil.items()} }; k escolhido = {k}.\n" + perfil.to_markdown())
fig, ax = plt.subplots(figsize=(9, 4)); sns.heatmap(perfil[num + ["NOTA_MEDIA"]], annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set_title("Perfil médio dos clusters"); fig.tight_layout(); fig.savefig(C.FIGS / "12_clusters.png", dpi=150); plt.close(fig)

S.append("\n## Observações\nO modelo descreve associações entre municípios (nível ecológico), não causalidade, e não deve ser usado "
         "para julgar indivíduos ou escolas. Machine Learning no nível individual foi considerado inadequado porque PARTICIPANTES e "
         "RESULTADOS não podem ser ligados por participante.")
(C.SAIDAS / "resultados_ml.md").write_text("\n".join(S), encoding="utf-8")
print("\n".join(S))
