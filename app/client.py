import requests
from fire import Fire
from pprint import pprint
import json


def run(question: str = "What is the capital of France?", port: int = 8000):
    url = f"http://0.0.0.0:{port}/answer"
    data = {"question": question}

    response = requests.get(url, json=data)
    print(response.json()["answer"])  # json.dumps(, indent=4))


if __name__ == "__main__":
    Fire(run)
