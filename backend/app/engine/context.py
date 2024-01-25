import chromadb
from llama_index import ServiceContext, StorageContext
from llama_index.vector_stores import ChromaVectorStore
from app.context import create_base_context
from app.engine.constants import CHUNK_SIZE, CHUNK_OVERLAP, STORAGE_DIR, VECTOR_STORE_COLLECTION_NAME, STORAGE_GENERATE
import logging

logger = logging.getLogger("uvicorn")

def create_service_context():
    base = create_base_context()
    return ServiceContext.from_defaults(
        llm=base.llm,
        embed_model=base.embed_model,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

def create_storage_context(is_generate=False):
    path = STORAGE_GENERATE if is_generate else STORAGE_DIR
    chroma_client = chromadb.PersistentClient(path=path)
    collection = chroma_client.get_or_create_collection(name=VECTOR_STORE_COLLECTION_NAME)
    return StorageContext.from_defaults(vector_store=ChromaVectorStore(chroma_collection=collection))

def delete_former_index():
    chroma_client = chromadb.PersistentClient(path=STORAGE_GENERATE)
    try:
        chroma_client.delete_collection(name=VECTOR_STORE_COLLECTION_NAME)
    except:
        logger.info("No vector store exists, this must be a first time setup")