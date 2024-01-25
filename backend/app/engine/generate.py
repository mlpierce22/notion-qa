import logging
import os
import requests
import json
from pathlib import Path
from typing import List
from llama_index import download_loader
from llama_index.schema import Document
from dotenv import load_dotenv

import sys
from pathlib import Path

# Get the path of the directory two levels above the current one
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from app.engine.constants import STORAGE_GENERATE, DOCUMENTS_FILE
from app.engine.context import create_service_context, create_storage_context, delete_former_index
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
)

load_dotenv()
NotionPageReader = download_loader('NotionPageReader')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def generate_datasource(fetch_docs: bool = False):
    logger.info("Creating new index")
    
    # First, delete the former index because we are going to rebuild it
    delete_former_index()
    service_context = create_service_context()
    storage_context = create_storage_context(is_generate=True)
    if fetch_docs:
        documents = load_obsidian()
        documents += load_notion()
        logger.info(f"Loaded {len(documents)} documents. Saving them to disk...")
        # Save documents to disk
        with open(DOCUMENTS_FILE, 'w') as f:
            doc_dicts = [doc.to_dict() for doc in documents]
            f.write(json.dumps(doc_dicts))
    else:
        logger.info(f"Loading documents from {DOCUMENTS_FILE}...")
        with open(DOCUMENTS_FILE, 'r') as f:
            doc_dicts = json.loads(f.read())
            documents = [Document.from_dict(doc_dict) for doc_dict in doc_dicts]

    logger.info(f"Embedding {len(documents)} documents. This takes about 10-15 minutes...")
    index = VectorStoreIndex.from_documents(
                show_progress=True,
                documents=documents,
                service_context=service_context, 
                storage_context=storage_context
            )

    logger.info(f"Finished creating new index. Stored in {STORAGE_GENERATE}")
    return index

def collect_input_files(root, ignore):
    """
        Collect all files in the root directory that we are "allowed" to index
    """
    input_files = []
    files_to_check = list(Path(root).iterdir())
    while len(files_to_check) > 0:
        f = files_to_check.pop()
        if f.name in ignore:
            continue
        
        # Check file names against regex strings in ignore list
        if any(f.match(ignore_pattern) for ignore_pattern in ignore):
            continue

        if f.is_dir():
            files_to_check = files_to_check + list(f.iterdir())
            continue

        input_files.append(str(f))
    
    return input_files

def load_obsidian() -> List[Document]:
    """
        Loop through every folder and file and add them to the index
    """

    ignore_patterns = set(["*.git", '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.svg', 'Attachments'])
    obsidian_path = os.getenv("OBSIDIAN_PATH")

    # Step 3: Read the directory and load the data, excluding the ignored files and images
    documents = SimpleDirectoryReader(input_files=collect_input_files(obsidian_path, ignore_patterns), exclude_hidden=True).load_data()

    return documents

def load_notion() -> List[Document]:
    integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")
    reader = NotionPageReader(integration_token=integration_token)

    logger.info("Loading Notion pages. This may take a while...")
    return reader.load_data(page_ids=fetch_all_page_ids(integration_token))

def fetch_all_page_ids(integration_token: str) -> List[str]:
    all_page_ids = []
    has_more = True
    start_cursor = None

    while has_more:
        headers = {
            'Authorization': f'Bearer {integration_token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }

        payload = {
            'filter': {
                'property': 'object',
                'value': 'page'
            }
        }

        if start_cursor is not None:
            payload['start_cursor'] = start_cursor

        response = requests.post('https://api.notion.com/v1/search', headers=headers, data=json.dumps(payload))
        response_json: dict = response.json()

        if response.status_code != 200:
            raise Exception(f'Error fetching page ids. Returned the following response: {response_json}')

        all_page_ids.extend(page['id'] for page in response_json.get('results', []))
        has_more = response_json.get('has_more', False)
        start_cursor = response_json.get('next_cursor', None)

    return all_page_ids


if __name__ == "__main__":
    # Take in argument called --fetch-docs to rebuild the documents.json file
    generate_datasource(len(sys.argv) > 1 and sys.argv[1] == "--fetch-docs")
