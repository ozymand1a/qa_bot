# todo: Ability to change a database to query from
# todo: another endpoints for adding new messages(as text or as file)
import pickle
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores.faiss import FAISS

from data import get_documents
from utils import get_logger
from type_defs import Question


class SimilaritySearch:
    """Class to do similarity search for a given database and queries"""

    # todo: caching option
    def __init__(self, k=3):
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.cached_vectorstore_path = None
        self.k = k
        self._vectorstore = None
        self._retriever = None

    def _embed_docs(self, docs_path, save_path: Optional[Path] = None):
        documents = get_documents(docs_path)
        vectorstore = FAISS.from_documents(documents, self.embeddings)

        if save_path is not None:
            with open(save_path, "wb") as f:
                pickle.dump(vectorstore, f)
                self.cached_vectorstore_path = save_path

        return vectorstore

    def _get_retriever(self, vectorstore):
        retriever = vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": self.k}
        )
        return retriever

    def setup(self, docs_path):
        self._vectorstore = self._embed_docs(docs_path)
        self._retriever = self._get_retriever(self._vectorstore)

    def find_similar_k(self, query: str, k: int = 3):
        if self._retriever is None:
            raise ValueError("this class is not setup")

        rel_docs = self._retriever.get_relevant_documents(query)
        return rel_docs


app = FastAPI()
logger = get_logger(__name__)
DEFAULT_CHAT_PATH = Path(__file__).parent.parent / "data" / "django_chat_history.json"
docs_search = SimilaritySearch()
docs_search.setup(DEFAULT_CHAT_PATH)


@app.get("/search")
async def search(question: Question):
    """Find similar documents for the question"""
    logger.info("received a request to find similar docs")
    rel_docs = docs_search.find_similar_k(question.question)
    return {"relevant_documents": rel_docs}


# todo: implement
# @app.post("/update")
# async def update(messages: str):
#     pass
