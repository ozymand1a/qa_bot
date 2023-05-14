import requests
from fire import Fire
from pprint import pprint
import json


ADDRESS = "http://0.0.0.0"


def get_rel_docs(question: str, port: int = 8000, address: str = ADDRESS):
    url = f"{address}:{port}/search"
    data = {"question": question}

    response = requests.get(url, json=data)
    return response.json()["relevant_documents"]


def ask_question(
    question: str,
    llm_port: int = 8000,
    docs_search_port: int = 8001,
    address: str = ADDRESS,
):
    rel_docs = get_rel_docs(question, docs_search_port, address)

    # make request with context
    url = f"{address}:{llm_port}/api_v1/ask"
    data = {"question": question, "context": rel_docs}
    response = requests.get(url, json=data)
    print(response.json()["answer"])


if __name__ == "__main__":
    Fire()
