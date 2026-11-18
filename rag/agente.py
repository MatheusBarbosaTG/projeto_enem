"""Agente de dados com RAG.

Fluxo: pergunta -> embedding -> busca por similaridade no ChromaDB -> trechos + pergunta vão
para o modelo de linguagem -> resposta ancorada nas fontes.

Requer a variável de ambiente ANTHROPIC_API_KEY (opcional: ENEM_MODELO). Sem chave, o agente
devolve apenas os trechos recuperados, o que já permite demonstrar a busca semântica.
Teste rápido: python rag/agente.py "Qual a relação entre renda e desempenho no ENEM?"
"""
import os
import sys
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

RAIZ = Path(__file__).resolve().parent.parent
MODELO_EMB = "paraphrase-multilingual-MiniLM-L12-v2"
MODELO_LLM = os.getenv("ENEM_MODELO", "claude-sonnet-5-5")
K = 5

_col = None


def _colecao():
    global _col
    if _col is None:
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODELO_EMB)
        _col = chromadb.PersistentClient(path=str(RAIZ / "rag" / "chroma_db")).get_collection("enem", embedding_function=ef)
    return _col


def buscar(pergunta: str, k: int = K):
    r = _colecao().query(query_texts=[pergunta], n_results=k)
    return [{"trecho": d, "distancia": dist, **m} for d, m, dist in zip(r["documents"][0], r["metadatas"][0], r["distances"][0])]


def responder(pergunta: str):
    fontes = buscar(pergunta)
    contexto = "\n\n".join(f"[{i + 1}] ({f['titulo']} – {f['fonte']})\n{f['trecho']}" for i, f in enumerate(fontes))
    if not os.getenv("ANTHROPIC_API_KEY"):
        return "_Sem ANTHROPIC_API_KEY: exibindo só os trechos mais relevantes._", fontes
    import anthropic
    msg = anthropic.Anthropic().messages.create(
        model=MODELO_LLM, max_tokens=800,
        system=("Você é um assistente de dados sobre o desempenho no ENEM. Responda em português, apenas com base nos "
                "trechos fornecidos. Cite as fontes pelo número entre colchetes, como [1]. Se os trechos não bastarem, "
                "diga que não há informação suficiente; não invente números. Não tente identificar pessoas."),
        messages=[{"role": "user", "content": f"Trechos:\n{contexto}\n\nPergunta: {pergunta}"}],
    )
    return msg.content[0].text, fontes


if __name__ == "__main__":
    resp, fontes = responder(" ".join(sys.argv[1:]) or "Qual a relação entre renda e desempenho no ENEM?")
    print(resp, "\n")
    if not os.getenv("ANTHROPIC_API_KEY"):
        for i, f in enumerate(fontes, 1):
            print(f"[{i}] ({f['titulo']})\n{f['trecho']}\n")
    print("Fontes:")
    for i, f in enumerate(fontes, 1):
        print(f"[{i}] {f['titulo']} – {f['fonte']} {f['link']}")
