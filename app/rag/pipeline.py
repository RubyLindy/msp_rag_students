from app.rag.retriever import retrieve
from app.rag.llm import generate
from jinja2 import Environment, FileSystemLoader
import os

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
jinja_env = Environment(loader=FileSystemLoader(PROMPTS_DIR))


def answer(query):
    retrieved = retrieve(query)

    docs = retrieved["documents"]
    metadatas = retrieved["metadatas"]
    distances = retrieved["distances"]

    context = "\n\n".join(docs)

    template = jinja_env.get_template("qa_prompt.j2")
    prompt = template.render(context=context, query=query)

    answer_text = generate(prompt)

    seen = {}
    for m, d in zip(metadatas, distances):
        source = m["source"]
        if source not in seen or d < seen[source]:
            seen[source] = d

    sources = [{"file": source, "distance": round(distance, 4)} for source, distance in seen.items()]

    return {
        "answer": answer_text,
        "sources": sources
    }