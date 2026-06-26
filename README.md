# RAG PDF Assistant

This project is a small local Retrieval-Augmented Generation (RAG) proof of concept. It loads PDF files from a `docs` folder, splits them into chunks, stores embeddings in a local Chroma vector database, and answers questions using retrieved document context with Ollama.

## Project Structure

```text
rag-poc/
├── README.md
└── rag/
    ├── docs/              # PDF documents used as the knowledge source
    ├── vectordb/          # Generated Chroma vector database
    ├── ingest.py          # Loads PDFs and creates the vector database
    ├── query.py           # Asks questions against the vector database
    └── requirement.txt    # Python dependencies
```

## Requirements

- Python 3.10 or newer
- Ollama installed and running
- An Ollama model available locally, for example `llama3:latest`

Install Ollama from:

```text
https://ollama.com/
```

Pull the default model used by this project:

```powershell
ollama pull llama3
```

## Setup

From the project root:

```powershell
cd rag
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirement.txt
```

## Add Documents

Place your PDF files inside:

```text
rag/docs/
```

The current sample documents include troubleshooting guides, runbooks, incident reports, RCA notes, and deployment SOPs.

## Build the Vector Database

Run the ingestion script from inside the `rag` folder:

```powershell
python ingest.py
```

This script:

1. Loads PDFs from `docs/`
2. Splits pages into smaller text chunks
3. Creates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
4. Stores the vectors in `vectordb/`

## Ask Questions

After ingestion is complete, run:

```powershell
python query.py
```

Enter a question when prompted. The script retrieves the top matching chunks from Chroma and sends them to Ollama with instructions to answer only from the provided context.

## Change the Ollama Model

By default, `query.py` uses:

```text
llama3:latest
```

You can override it with the `OLLAMA_MODEL` environment variable:

```powershell
$env:OLLAMA_MODEL="mistral:latest"
python query.py
```

Make sure the model exists locally:

```powershell
ollama pull mistral
```

## Notes for GitHub

The `vectordb/` folder is generated output and can become large. It is usually better to exclude it from Git and regenerate it with `python ingest.py` after cloning the repo.

Recommended `.gitignore` entries:

```text
rag/vectordb/
rag/.venv/
__pycache__/
*.pyc
```

## Typical Workflow

```powershell
cd rag
.\.venv\Scripts\Activate.ps1
python ingest.py
python query.py
```

