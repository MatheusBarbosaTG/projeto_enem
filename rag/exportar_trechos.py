"""Sem chave de API: roda as 5 perguntas na busca vetorial e salva os trechos recuperados em
perguntas_trechos.md (para redigir as respostas ancoradas nas fontes)."""
from agente import buscar

PERGUNTAS = [
    "Qual a diferença de nota média entre escolas públicas e privadas?",
    "Quais variáveis socioeconômicas mais se associam à nota no ENEM?",
    "Como a renda familiar se relaciona com o desempenho nas diferentes áreas?",
    "Quais as diferenças regionais no desempenho do ENEM?",
    "Quais cuidados éticos e de privacidade esse tipo de análise exige?",
]

with open("perguntas_trechos.md", "w", encoding="utf-8") as out:
    for n, q in enumerate(PERGUNTAS, 1):
        out.write(f"# Pergunta {n}: {q}\n\n")
        for i, f in enumerate(buscar(q), 1):
            out.write(f"## [{i}] {f['titulo']} – {f['fonte']} (dist. {f['distancia']:.3f})\n{f['trecho']}\n\n")
print("Gerado: perguntas_trechos.md")
