"""Tratamento dos microdados do ENEM 2025 (PARTICIPANTES + RESULTADOS).

Uso: python src/01_tratar_dados.py [--participantes caminho] [--resultados caminho]

Produz:
  data/enem_resultados.parquet : notas por participante + escola/UF (sem socioeconômico)
  data/enem_municipios.parquet : uma linha por município de prova (perfil socioeconômico + desempenho)
Os dois arquivos não têm chave individual em comum; a ligação é feita por CO_MUNICIPIO_PROVA (análise ecológica).
"""
import argparse
import pandas as pd
import config as C

ap = argparse.ArgumentParser()
ap.add_argument("--participantes", default=str(C.CSV_PARTICIPANTES))
ap.add_argument("--resultados", default=str(C.CSV_RESULTADOS))
ap.add_argument("--min-municipio", type=int, default=30, help="Mínimo de participantes por município nas duas bases")
args = ap.parse_args()
log = []


def detectar_encoding(caminho: str) -> str:
    try:
        pd.read_csv(caminho, sep=";", nrows=50000, encoding="utf-8", dtype=str)
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


# ---------------------------------------------------------------- PARTICIPANTES -> perfil por município
enc = detectar_encoding(args.participantes)
acum, total_p, trein = [], 0, 0
for ch in pd.read_csv(args.participantes, sep=";", encoding=enc, usecols=C.COLS_PARTICIPANTES, chunksize=500_000,
                      dtype={"Q001": "string", "Q002": "string", "Q007": "string", "Q020": "string", "Q021": "string",
                             "Q023": "string", "TP_SEXO": "string"}):
    total_p += len(ch)
    trein += int((ch["IN_TREINEIRO"] == 1).sum())
    ch = ch[(ch["IN_TREINEIRO"] == 0) & ch["Q007"].isin(C.RENDA_ORDEM)].copy()
    ch["renda_ord"] = ch["Q007"].map({c: i for i, c in enumerate(C.RENDA_ORDEM)})
    ch["renda_ate1"] = ch["Q007"].isin(C.RENDA_ATE_1SM)
    ch["renda_5mais"] = ch["Q007"].isin(C.RENDA_ACIMA_5SM)
    ch["wifi"] = ch["Q020"] == "B"
    ch["computador"] = ch["Q021"].isin(list("BCDE"))
    ch["priv_q023"] = ch["Q023"].isin(["D", "E"])      # somente escola privada
    ch["publ_q023"] = ch["Q023"] == "A"                 # somente escola pública
    ch["mae_sup"] = ch["Q002"].isin(C.SUPERIOR)
    ch["pai_sup"] = ch["Q001"].isin(C.SUPERIOR)
    ch["fem"] = ch["TP_SEXO"] == "F"
    ch["preta_parda"] = ch["TP_COR_RACA"].isin([2, 3])
    ch["n"] = 1
    g = ch.groupby(["CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA"], observed=True)[
        ["n", "renda_ord", "renda_ate1", "renda_5mais", "mae_sup", "pai_sup", "fem", "preta_parda",
         "wifi", "computador", "priv_q023", "publ_q023"]].sum()
    acum.append(g)
soc = pd.concat(acum).groupby(level=[0, 1, 2]).sum().reset_index()
n = soc["n"]
mun = pd.DataFrame({
    "CO_MUNICIPIO": soc["CO_MUNICIPIO_PROVA"], "MUNICIPIO": soc["NO_MUNICIPIO_PROVA"], "UF": soc["SG_UF_PROVA"],
    "N_SOCIO": n, "RENDA_MEDIA_ORD": soc["renda_ord"] / n,
    "PCT_RENDA_ATE_1SM": 100 * soc["renda_ate1"] / n, "PCT_RENDA_ACIMA_5SM": 100 * soc["renda_5mais"] / n,
    "PCT_MAE_SUPERIOR": 100 * soc["mae_sup"] / n, "PCT_PAI_SUPERIOR": 100 * soc["pai_sup"] / n,
    "PCT_FEMININO": 100 * soc["fem"] / n, "PCT_PRETA_PARDA": 100 * soc["preta_parda"] / n,
    "PCT_WIFI": 100 * soc["wifi"] / n, "PCT_COMPUTADOR": 100 * soc["computador"] / n,
    "PCT_SO_PRIVADA_Q023": 100 * soc["priv_q023"] / n, "PCT_SO_PUBLICA_Q023": 100 * soc["publ_q023"] / n,
})
log += [f"PARTICIPANTES: {total_p:,} registros lidos; {trein:,} treineiros excluídos; "
        f"{int(n.sum()):,} com renda válida em {len(mun):,} municípios de prova."]

# ---------------------------------------------------------------- RESULTADOS -> nível individual
enc = detectar_encoding(args.resultados)
partes, total_r = [], 0
for ch in pd.read_csv(args.resultados, sep=";", encoding=enc, usecols=C.COLS_RESULTADOS, chunksize=500_000):
    total_r += len(ch)
    ok = (ch[["TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT"]] == 1).all(axis=1)
    ok &= ch["TP_STATUS_REDACAO"] == 1
    ch = ch[ok].dropna(subset=C.NOTAS)
    partes.append(ch)
res = pd.concat(partes, ignore_index=True)
log.append(f"RESULTADOS: {total_r:,} registros lidos; {len(res):,} com as 4 provas presentes, redação válida e todas as notas.")
res["NOTA_MEDIA"] = res[C.NOTAS].mean(axis=1).round(2)
res["DEPENDENCIA"] = res["TP_DEPENDENCIA_ADM_ESC"].map(C.DEPENDENCIA).fillna("Não informada")
res["REDE"] = res["DEPENDENCIA"].map({"Federal": "Pública", "Estadual": "Pública", "Municipal": "Pública",
                                       "Privada": "Privada"}).fillna("Não informada")
res["LOCALIZACAO"] = res["TP_LOCALIZACAO_ESC"].map(C.LOCALIZACAO).fillna("Não informada")
res["UF"] = res["SG_UF_PROVA"]
log.append("Distribuição por rede: " + ", ".join(f"{k}={v:,}" for k, v in res["REDE"].value_counts().items()))
res.to_parquet(C.BASE_RESULTADOS, index=False)

# ---------------------------------------------------------------- desempenho por município
com_rede = res[res["REDE"] != "Não informada"]
desemp = res.groupby("CO_MUNICIPIO_PROVA").agg(
    N_RESULTADOS=("NOTA_MEDIA", "size"), NOTA_MEDIA=("NOTA_MEDIA", "mean"), NOTA_CN=("NU_NOTA_CN", "mean"),
    NOTA_CH=("NU_NOTA_CH", "mean"), NOTA_LC=("NU_NOTA_LC", "mean"), NOTA_MT=("NU_NOTA_MT", "mean"),
    NOTA_REDACAO=("NU_NOTA_REDACAO", "mean")).reset_index().rename(columns={"CO_MUNICIPIO_PROVA": "CO_MUNICIPIO"})
priv = (com_rede.assign(p=com_rede["REDE"] == "Privada").groupby("CO_MUNICIPIO_PROVA")["p"].mean() * 100
        ).rename("PCT_ESCOLA_PRIVADA").reset_index().rename(columns={"CO_MUNICIPIO_PROVA": "CO_MUNICIPIO"})
mun = mun.merge(desemp, on="CO_MUNICIPIO").merge(priv, on="CO_MUNICIPIO", how="left")
antes = len(mun)
mun = mun[(mun["N_SOCIO"] >= args.min_municipio) & (mun["N_RESULTADOS"] >= args.min_municipio)].dropna(subset=["PCT_ESCOLA_PRIVADA"])
log.append(f"Municípios com dados nas duas bases: {antes:,}; mantidos com ≥{args.min_municipio} participantes: {len(mun):,}.")
mun.round(3).to_parquet(C.BASE_MUNICIPIOS, index=False)

desc = {
    "NOTA_MEDIA": "Média simples das 5 notas (CN, CH, LC, MT, Redação), 0-1000; no município, média dos participantes",
    "DEPENDENCIA": "Dependência administrativa da escola (TP_DEPENDENCIA_ADM_ESC)", "REDE": "Pública (federal/estadual/municipal) ou privada",
    "LOCALIZACAO": "Localização da escola", "UF": "UF de realização da prova",
    "RENDA_MEDIA_ORD": "Média do código ordinal da renda familiar Q007 (0 = nenhuma ... 16 = acima de R$ 30.360)",
    "PCT_RENDA_ATE_1SM": "% com renda familiar de até 1 SM (R$ 1.518)", "PCT_RENDA_ACIMA_5SM": "% com renda familiar acima de 5 SM (R$ 7.590)",
    "PCT_WIFI": "% com Wi-Fi em casa (Q020)", "PCT_COMPUTADOR": "% com computador/notebook em casa (Q021)",
    "PCT_SO_PRIVADA_Q023": "% que cursou o médio só em escola privada (Q023 = D/E)", "PCT_SO_PUBLICA_Q023": "% que cursou só em escola pública (Q023 = A)",
    "PCT_MAE_SUPERIOR": "% cuja mãe/responsável tem ensino superior (Q002)", "PCT_PAI_SUPERIOR": "% cujo pai/responsável tem ensino superior (Q001)",
    "PCT_ESCOLA_PRIVADA": "% dos participantes do município vindos de escola privada",
    "N_SOCIO": "Participantes (não treineiros) com renda válida", "N_RESULTADOS": "Participantes com notas válidas",
}
dic = []
for nome, d in [("enem_resultados", res), ("enem_municipios", mun)]:
    t = pd.DataFrame({"base": nome, "coluna": d.columns, "tipo": d.dtypes.astype(str).values,
                      "nulos": d.isna().sum().values, "valores_unicos": d.nunique().values})
    t["descricao"] = t["coluna"].map(desc).fillna("Coluna original do INEP (ver dicionário oficial)")
    dic.append(t)
pd.concat(dic).to_csv(C.DICIONARIO, index=False, encoding="utf-8-sig")
(C.SAIDAS / "log_tratamento.txt").write_text("\n".join(log), encoding="utf-8")
print("\n".join(log))
