from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import ollama
import os


MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3:latest")
TOP_K = 3

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="vectordb",
    embedding_function=embeddings
)

question = input("Ask a question: ")

results = db.similarity_search(question, k=TOP_K)

context = "\n\n".join(
    f"Source {i + 1}: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
    for i, doc in enumerate(results)
)

prompt = f"""
You are a helpful assistant answering questions using only the provided context.
If the answer is not in the context, say you do not know based on the documents.

Context:
{context}

Question:
{question}

Answer:
""".strip()

try:
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={"temperature": 0.1},
    )
except Exception as exc:
    print("\nCould not get an answer from Ollama.")
    print("Make sure Ollama is installed, running, and the model is available.")
    print(f"Expected model: {MODEL_NAME}")
    print(f"Original error: {exc}")
else:
    print("\nAnswer:")
    print(response["response"].strip())

print("\nSources:")
for i, doc in enumerate(results):
    print(f"{i + 1}. {doc.metadata.get('source', 'unknown')}")
