import os

from llama_index import ServiceContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def create_base_context():
    model = os.getenv("MODEL", "llama2")
    prompt = os.getenv("LEADING_PROMPT", None)
    temperature = os.getenv("TEMPERATURE", 0)

    embeddings_model = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
    return ServiceContext.from_defaults(
        llm=Ollama(model=model, temperature=temperature),
        embed_model=HuggingFaceEmbedding(model_name=embeddings_model),
        query_wrapper_prompt=prompt,
    )
