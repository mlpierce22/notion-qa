import logging
import os
from pprint import pprint

from llama_index import VectorStoreIndex
from llama_index.chat_engine.types import ChatMode
from llama_index.vector_stores import ChromaVectorStore

from app.engine.constants import STORAGE_DIR
from app.engine.context import create_service_context, create_storage_context
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("uvicorn")

def get_chat_engine():
    service_context = create_service_context()
    storage_context = create_storage_context()

    # check if storage already exists
    if not os.path.exists(STORAGE_DIR):
        raise Exception(
            "StorageContext is empty - call 'python app/engine/generate.py' to generate the storage first"
        )

    # load the existing index
    logger.info(f"Loading index from {STORAGE_DIR}...")
    
    index = VectorStoreIndex.from_vector_store(
            vector_store=storage_context.vector_store,
            service_context=service_context,
        )

    logger.info(f"Finished loading index from {STORAGE_DIR}")

    return index.as_chat_engine(chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT, verbose=True)