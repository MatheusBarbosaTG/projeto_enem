"""Configuração central: caminhos, colunas e dicionários de códigos do ENEM 2025
(arquivos PARTICIPANTES e RESULTADOS, que NÃO têm chave comum entre si)."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "data"
SAIDAS = RAIZ / "outputs"
FIGS = SAIDAS / "figuras"
for p in (DADOS, SAIDAS, FIGS):
    p.mkdir(parents=True, exist_ok=True)

CSV_PARTICIPANTES = DADOS / "PARTICIPANTES_2025.csv"
CSV_RESULTADOS = DADOS / "RESULTADOS_2025.csv"
BASE_RESULTADOS = DADOS / "enem_resultados.parquet"   # nível do participante (sem dados socioeconômicos)
BASE_MUNICIPIOS = DADOS / "enem_municipios.parquet"   # nível do município (socioeconômico + desempenho)
DICIONARIO = SAIDAS / "dicionario_de_dados.csv"

NOTAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
NOMES_NOTAS = {
    "NU_NOTA_CN": "Ciências da Natureza", "NU_NOTA_CH": "Ciências Humanas",
    "NU_NOTA_LC": "Linguagens e Códigos", "NU_NOTA_MT": "Matemática", "NU_NOTA_REDACAO": "Redação",
}
COMPETENCIAS = [f"NU_NOTA_COMP{i}" for i in range(1, 6)]

COLS_PARTICIPANTES = ["NU_INSCRICAO", "TP_FAIXA_ETARIA", "TP_SEXO", "TP_COR_RACA", "IN_TREINEIRO",
                      "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA", "Q001", "Q002", "Q005",
                      "Q007", "Q020", "Q021", "Q023"]   # Q007 = renda familiar (Q006 é só "você possui renda?")
COLS_RESULTADOS = (["NU_SEQUENCIAL", "CO_ESCOLA", "TP_DEPENDENCIA_ADM_ESC", "TP_LOCALIZACAO_ESC",
                    "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA",
                    "TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT", "TP_STATUS_REDACAO"]
                   + NOTAS + COMPETENCIAS)

DEPENDENCIA = {1: "Federal", 2: "Estadual", 3: "Municipal", 4: "Privada"}
LOCALIZACAO = {1: "Urbana", 2: "Rural"}
COR_RACA = {0: "Não declarado", 1: "Branca", 2: "Preta", 3: "Parda", 4: "Amarela", 5: "Indígena"}
ESCOLARIDADE = {
    "A": "Nunca estudou", "B": "Fundamental incompleto (até 5º ano)", "C": "Fundamental incompleto (6º ao 9º)",
    "D": "Fundamental completo", "E": "Médio completo", "F": "Superior completo", "G": "Pós-graduação", "H": "Não sei",
}
# Q007 (dicionário 2025): A = nenhuma renda; B = até R$ 1.518 (1 SM); ...; H = até R$ 7.590 (5 SM); Q = acima de R$ 30.360
RENDA_ORDEM = list("ABCDEFGHIJKLMNOPQ")
RENDA_ATE_1SM = ["A", "B"]
RENDA_ACIMA_5SM = list("IJKLMNOPQ")
SUPERIOR = ["F", "G"]
