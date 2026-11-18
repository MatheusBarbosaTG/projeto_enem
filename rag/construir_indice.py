"""Prepara os textos e cria o banco vetorial (ChromaDB).

Entradas : rag/docs/*.txt|.md|.pdf  +  rag/fontes.csv (metadados)  +  outputs/resumo_analise.md
           e outputs/resultados_ml.md (resultados da própria análise)
Saída    : rag/chroma_db/ (coleção 'enem')
Uso      : python rag/construir_indice.py
"""
import re
from pathlib import Path

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "rag" / "docs"
BANCO = RAIZ / "rag" / "chroma_db"
MODELO_EMB = "paraphrase-multilingual-MiniLM-L12-v2"  # bom para português
TAM, SOBRA = 900, 150


def ler(arq: Path) -> str:
    if arq.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(str(arq)).pages)
    return arq.read_text(encoding="utf-8", errors="ignore")


def limpar(t: str) -> str:
    t = re.sub(r"-\n(\w)", r"\1", t)          # hifenização de fim de linha
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def dividir(t: str):
    """Divide em blocos de ~TAM caracteres respeitando parágrafos, com sobreposição."""
    partes, atual = [], ""
    for par in re.split(r"\n\s*\n", t):
        if len(atual) + len(par) > TAM and atual:
            partes.append(atual)
            atual = atual[-SOBRA:] + "\n" + par
        else:
            atual += ("\n\n" if atual else "") + par
        while len(atual) > TAM * 1.5:           # parágrafos gigantes
            partes.append(atual[:TAM]); atual = atual[TAM - SOBRA:]
    if atual.strip():
        partes.append(atual)
    return partes


fontes = pd.read_csv(RAIZ / "rag" / "fontes.csv", dtype=str).fillna("")
itens = [(DOCS / r.arquivo, r._asdict()) for r in fontes.itertuples(index=False) if (DOCS / r.arquivo).exists()]
faltando = [r.arquivo for r in fontes.itertuples(index=False) if not (DOCS / r.arquivo).exists()]
if faltando:
    print("Aviso: arquivos listados em fontes.csv e não encontrados em rag/docs/:", faltando)

# Resultados da análise estruturada também alimentam o agente
for nome, titulo in [("resumo_analise.md", "Resumo da análise dos microdados do ENEM (este projeto)"),
                     ("resultados_ml.md", "Resultados de Machine Learning (este projeto)")]:
    p = RAIZ / "outputs" / nome
    if p.exists():
        itens.append((p, {"arquivo": nome, "titulo": titulo, "fonte": "Análise do grupo sobre microdados do INEP",
                          "link": "", "data_acesso": "", "tema": "análise própria"}))

cliente = chromadb.PersistentClient(path=str(BANCO))
try:
    cliente.delete_collection("enem")
except Exception:
    pass
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODELO_EMB)
col = cliente.create_collection("enem", embedding_function=ef, metadata={"hnsw:space": "cosine"})

ids, textos, metas = [], [], []
for caminho, m in itens:
    for i, parte in enumerate(dividir(limpar(ler(caminho)))):
        ids.append(f"{m['arquivo']}::{i}")
        textos.append(parte)
        metas.append({k: m.get(k, "") for k in ("titulo", "fonte", "link", "data_acesso", "tema")} | {"chunk": i})
for i in range(0, len(ids), 100):
    col.add(ids=ids[i:i + 100], documents=textos[i:i + 100], metadatas=metas[i:i + 100])
print(f"Indexados {len(ids)} trechos de {len(itens)} documentos em {BANCO}")
