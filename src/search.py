import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "document_chunks")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def get_vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL
    )


def search_and_answer(question: str) -> str:
    vector_store = get_vector_store()
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

    results = vector_store.similarity_search_with_score(question, k=10)

    contexto = "\n\n".join([doc.page_content for doc, score in results])

    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

    response = llm.invoke(prompt)
    return response.content


def search_prompt(question=None):
    """Mantido para compatibilidade com chat.py original"""
    return search_and_answer
