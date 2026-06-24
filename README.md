# MSP test RAG

We want to test a RAG for the ISMAR project. The idea is to augment the MSP planning activity with a dynamic RAG tool that allows planner to quickly query the status of an area in different scenarios in a conversational style. Since the queried plan is being built, a potential issue to further investigate is how to update the vector db when things changes. 

## First step
In this first step, we aim to:

- build a standard RAG system based on only one area (the North Adriatic Sea, NAS) for the moment. 
- use Langchain with ChromaDB and using a simple llama model for easy testing (llama3.2:8b should be good and small enough for local testing). 
- develop a API interface for chat
- build a simple GUI for testing

## Second step
In this second step, we aim to:

- understand how to dynamically add and remove documents in the vector database
- add the documents of the other areas
- develop a "tool" functionality to select different areas (perhaps, it should also be used for selecting different scenarios)

# Resources

Langchain: https://github.com/langchain-ai/langchain 

Chroma DB: https://github.com/chroma-core/chroma


LLM Model: llama3.1:8b

Embeddings: 
- *embeddinggemma*: quite small and multilingual (let's use this one for the moment)
- *nomic-embed-text-v2-moe*: probably better performances but larger

Data documents of the NAS area: ./data

# How to run it on YOUR system

### Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.com) installed and running locally (if using a local model)

---

### 1. Install dependencies

Open a terminal, navigate to the project root folder, and run:

    pip install -r requirements.txt

---

### 2. Create a `.env` file

In the project root folder, create a new file called exactly `.env` (no other extension) and paste in the following:

    LLM_MODEL=llama3.2:3b
    LLM_API_KEY=
    LLM_BASE_URL=http://localhost:11434/api
    EMBED_MODEL=embeddinggemma

    PROMPT_TEMPLATE=qa_prompt.j2

- Change the values depending on which LLM you want to use. If using a provider like OpenAI, fill in `LLM_API_KEY` and update `LLM_BASE_URL` and `LLM_MODEL` accordingly.
- Change the value of `PROMPT_TEMPLATE` to the name of a new jinja2 file you create containing the prompt if you want to change the prompt used by the RAG.

---

### 3. Ingest the data

Run the ingestion script to process and index the documents:

    # Windows
    python app\rag\ingest.py

    # Mac / Linux
    python app/rag/ingest.py

This embeds all files in `data/NAS` into a local vector database and may take a few minutes depending on your hardware.

> **You only need to do this once.** If a `chroma_db` folder already exists in the project root, skip this step — unless the contents of `data/NAS` have changed.

---

### 4. Run the app

    # Windows
    python app\ui.py

    # Mac / Linux
    python app/ui.py

Once running, open your browser and go to [http://localhost:5000](http://localhost:5000) to start chatting with the MSP RAG.

### 5. Run in batch mode

Edit the `questions.txt` file with one question per line, then run:

    python batch.py questions.txt

Results are saved automatically to the `logs/` folder as a JSON file.

Or you can specify the name of the output to make it easier to find.

    python batch.py questions.txt --output results/my_run.json