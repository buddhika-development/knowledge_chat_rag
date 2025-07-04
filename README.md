![r](https://github.com/user-attachments/assets/41d0345a-9831-4e66-9d63-847141c9e6bd)

# 🧠 RAG Chatbot with Your Own Documents  
### Built with LangChain + Ollama + Chroma

This project builds a **Retrieval-Augmented Generation (RAG)** system that allows you to chat with your own documents using **LangChain**, **Ollama** for LLMs, and **Chroma** as the vector database.

---

## 🚀 Tech Stack

- **LangChain**: Orchestration and chaining of components
- **Ollama**: Local LLM backend (e.g., `gemma3:1b`, `deepseek-r1:1.5b`)
- **Chroma**: Lightweight local vector store for embeddings
- **Python**: FastAPI/Flask backend (optional)

---

## 📦 Installation

```bash
# Clone the project
git clone https://github.com/buddhika-development/knowledge_chat_rag
cd knowledge_chat_rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---
## Add enviorenment variables
```bash
model_name= <model_name>
temp= <model_temperature>
base_url= <ollama_running_host>
```
