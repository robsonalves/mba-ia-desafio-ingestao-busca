# Desafio MBA Engenharia de Software com IA - Full Cycle

## Ingestao e Busca Semantica com LangChain e PostgreSQL

Sistema RAG (Retrieval-Augmented Generation) que realiza ingestao de documentos PDF e permite busca semantica via CLI, respondendo perguntas exclusivamente com base no conteudo do documento.

## Tecnologias

- **Python 3.11+**
- **LangChain** - framework para orquestracao de LLMs
- **PostgreSQL + pgVector** - banco vetorial para armazenamento de embeddings
- **OpenAI** - modelo de embeddings text-embedding-3-small e LLM gpt-5-nano
- **Docker / Docker Compose** - para execucao do banco de dados

## Estrutura do Projeto

```
docker-compose.yml
requirements.txt
.env.example
src/
  ingest.py
  search.py
  chat.py
document.pdf
README.md
```

## Pre-requisitos

- Python 3.11+
- Docker e Docker Compose
- Chave de API da OpenAI

## Como Executar

### 1. Clonar o repositorio

```bash
git clone https://github.com/robsonalves/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

### 2. Configurar variaveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo .env com suas credenciais:

```
OPENAI_API_KEY=sua-chave-aqui
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=document_chunks
PDF_PATH=document.pdf
```

### 3. Criar e ativar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Subir o banco de dados

```bash
docker compose up -d
```

O Docker Compose sobe o PostgreSQL com a extensao pgVector ja habilitada.

### 6. Executar a ingestao do PDF

```bash
python src/ingest.py
```

O script carrega o PDF, divide em chunks de 1000 caracteres com overlap de 150, gera embeddings e armazena no banco vetorial.

### 7. Rodar o chat

```bash
python src/chat.py
```

## Exemplo de Uso

```
==================================================
Chat RAG - Pergunte sobre o documento
Digite 'sair' para encerrar
==================================================

Faca sua pergunta: Qual o faturamento da empresa?

Processando...

RESPOSTA: O faturamento foi de 10 milhoes de reais.

Faca sua pergunta: Qual e a capital da Franca?

Processando...

RESPOSTA: Nao tenho informacoes necessarias para responder sua pergunta.
```

## Como Funciona

1. **Ingestao**: O script de ingestao carrega o PDF, divide o conteudo em pedacos de 1000 caracteres com sobreposicao de 150, gera os embeddings via OpenAI e salva os vetores no PostgreSQL com pgVector.

2. **Busca**: Ao receber uma pergunta, o sistema vetoriza a pergunta, busca os 10 trechos mais relevantes no banco vetorial, monta um prompt com esse contexto e envia para a LLM gerar a resposta.

3. **Chat**: Interface de linha de comando que permite ao usuario fazer perguntas em loop. As respostas sao geradas exclusivamente com base no conteudo do documento ingerido. Perguntas fora do contexto sao recusadas.
