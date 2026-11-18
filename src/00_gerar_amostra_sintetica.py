"""Gera arquivos SINTÉTICOS com o esquema de PARTICIPANTES_2025 e RESULTADOS_2025 (sem chave em comum).
Serve só para testar o código. NUNCA use os resultados no relatório.
Uso: python src/00_gerar_amostra_sintetica.py [n_participantes]
"""
import sys
import numpy as np
import pandas as pd
import config as C

n = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
rng = np.random.default_rng(7)
nm = 300
mun = pd.DataFrame({"cod": 3500000 + np.arange(nm), "uf": rng.choice(["MG", "SP", "BA", "RJ", "PA", "CE"], nm),
                    "ses": rng.normal(0, 1, nm)})
mun["nome"] = "Municipio " + mun["cod"].astype(str)
LET = list("ABCDEFGHIJKLMNOPQ")


def sorteia_mun(k):
    p = rng.dirichlet(np.ones(nm) * 2)
    return rng.choice(nm, k, p=p)


# PARTICIPANTES
i = sorteia_mun(n)
ses = mun["ses"].to_numpy()[i] + rng.normal(0, .7, n)
renda_idx = np.clip((4 + 2.5 * ses + rng.normal(0, 1.5, n)).round(), 0, 16).astype(int)
p = pd.DataFrame({
    "NU_INSCRICAO": 210000000000 + np.arange(n), "TP_FAIXA_ETARIA": rng.integers(1, 12, n),
    "TP_SEXO": rng.choice(["M", "F"], n, p=[.42, .58]), "TP_COR_RACA": rng.choice(range(6), n, p=[.02, .38, .09, .48, .02, .01]),
    "IN_TREINEIRO": rng.choice([0, 1], n, p=[.95, .05]),
    "CO_MUNICIPIO_PROVA": mun["cod"].to_numpy()[i], "NO_MUNICIPIO_PROVA": mun["nome"].to_numpy()[i], "SG_UF_PROVA": mun["uf"].to_numpy()[i],
    "Q001": np.array(list("ABCDEFGH"))[np.clip((2 + 1.2 * ses + rng.normal(0, 1.3, n)).round(), 0, 7).astype(int)],
    "Q002": np.array(list("ABCDEFGH"))[np.clip((2.3 + 1.2 * ses + rng.normal(0, 1.3, n)).round(), 0, 7).astype(int)],
    "Q005": rng.integers(1, 7, n), "Q006": rng.choice(["A", "B"], n, p=[.6, .4]), "Q007": np.array(LET)[renda_idx],
    "Q020": np.where(rng.random(n) < 1 / (1 + np.exp(-(1.5 + ses))), "B", "A"),
    "Q021": np.where(rng.random(n) < 1 / (1 + np.exp(-(0.2 + ses))), "B", "A"),
    "Q023": rng.choice(list("ABCDEF"), n, p=[.75, .05, .02, .1, .05, .03]),
})
p.to_csv(C.CSV_PARTICIPANTES, sep=";", index=False, encoding="latin-1")

# RESULTADOS (independente de PARTICIPANTES, como no arquivo real)
m = int(n * 0.9)
j = sorteia_mun(m)
ses_r = mun["ses"].to_numpy()[j]
priv = rng.random(m) < 1 / (1 + np.exp(-(ses_r * 1.2 - 1.5)))
dep = np.where(priv, 4, rng.choice([1, 2, 3], m, p=[.04, .86, .10]))
base = 480 + 35 * ses_r + 55 * priv + rng.normal(0, 55, m)
r = pd.DataFrame({
    "NU_SEQUENCIAL": rng.permutation(m) + 1, "CO_ESCOLA": 30000000 + rng.integers(0, 5000, m),
    "TP_DEPENDENCIA_ADM_ESC": dep, "TP_LOCALIZACAO_ESC": rng.choice([1, 2], m, p=[.93, .07]),
    "CO_MUNICIPIO_PROVA": mun["cod"].to_numpy()[j], "NO_MUNICIPIO_PROVA": mun["nome"].to_numpy()[j], "SG_UF_PROVA": mun["uf"].to_numpy()[j],
})
for c in ["CN", "CH", "LC", "MT"]:
    r[f"TP_PRESENCA_{c}"] = rng.choice([0, 1], m, p=[.2, .8])
r["TP_STATUS_REDACAO"] = rng.choice([1, 2, 3, 4, 6], m, p=[.93, .01, .02, .02, .02])
for c, k in [("CN", .9), ("CH", 1), ("LC", 1), ("MT", 1.2)]:
    r[f"NU_NOTA_{c}"] = np.clip(base * k - 50 + rng.normal(0, 40, m), 0, 1000).round(1)
for k in range(1, 6):
    r[f"NU_NOTA_COMP{k}"] = np.clip(base / 5 - 40 + rng.normal(0, 40, m), 0, 200) // 20 * 20
r["NU_NOTA_REDACAO"] = r[[f"NU_NOTA_COMP{k}" for k in range(1, 6)]].sum(axis=1)
aus = (r[["TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT"]] == 0).any(axis=1)
r.loc[aus, C.NOTAS + C.COMPETENCIAS] = np.nan
r.to_csv(C.CSV_RESULTADOS, sep=";", index=False, encoding="latin-1")
print(f"Sintéticos: {n} participantes, {m} resultados, {nm} municípios.")
