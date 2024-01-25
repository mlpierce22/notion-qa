## Getting Started

### Virtual Environment
I recommend setting up a virtual environment so you don't have python package conflicts. Do this with `python -v venv [name]`. I called mine `env` so it's easy to remember. If you do the same, it's already gitignored at the root

### Backend
1. `cd backend`
2. Create a `.env` file with the following keys:
```
MODEL="llama2"
EMBED_MODEL="BAAI/bge-small-en-v1.5"
OBSIDIAN_PATH="/path/to/obsidian"
NOTION_INTEGRATION_TOKEN="secret_blah" # Create a notion integration: https://www.notion.so/my-integrations
TEMPERATURE=0
```
3. Install requirements (p.s. I just dumped my venv environment in here, so there may be extras, sorry :))
4. Generate the index. This will take a HOT second (It takes 23 minutes to fetch and index 3784 of my files on my macbook with an m3 chip). I recommend just starting it and walking away. You can use `caffeinate -is [command]` to keep it awake if that's an issue (If you do, you need to use the full python path).
```
python backend/app/engine/generate.py --fetch-docs
```
> If you wan to just rebuild the index without rebuilding all the documents, don't include the `--fetch-docs` flag
5. This will create a cache and a storage folder. `storage` has your chromadb, `cache` has your documents. These files are quite large. Running the generate command again without the `--fetch-docs` flag will use the documents in the cache when generating embeddings.

### Frontend
1. `cd frontend`
2. `bun install` - https://bun.sh/
3. Create the following `.env` file:
```
MODEL=llama2
NEXT_PUBLIC_MODEL=llama2
```

#### Some notes on the `.env` file
The model here should match the model defined in the backend. That being said, these models can be any model available on https://ollama.ai/library

### Running it
1. Ensure that ollama is running. If not, run `ollama serve`. You can find more info here: https://ollama.ai/
2. Install `GNU parallel`
3. Run both the frontend and backend in parallel, just run the following from the root of the repository:
```
bash run.sh
```

## Credit
- The boilerplate for codebase was created using [`create-llama`](https://github.com/run-llama/LlamaIndexTS/tree/main/packages/create-llama).