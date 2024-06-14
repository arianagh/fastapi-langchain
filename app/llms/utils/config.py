# flake8: noqa

import os

from dotenv import load_dotenv

load_dotenv()

SEARCH_RESULT_EMBEDDINGS_LOOKUPS = {'k': 3}
OPEN_API_KEY = os.environ.get("OPEN_API_KEY", "")
LLM_MODEL = 'gpt-3.5-turbo-16k'
EMBEDDING_MODEL = 'text-embedding-3-small'


class ChromaConfig:
    HOST: str = os.getenv('CHROMADB_HOST', 'localhost')
    PORT: int = int(os.getenv('CHROMADB_PORT', '8005'))
    CHROMADB_TOKEN = os.environ.get('CHROMADB_TOKEN', '')
    CHROMA_CLIENT_AUTH_PROVIDER = os.environ.get('CHROMA_CLIENT_AUTH_PROVIDER', '')


DEFAULT_PROMPT = """
I want you to act as a funny and friendly customer support AI for my customers.
"""
