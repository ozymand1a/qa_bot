import requests
from fire import Fire


def run(port: int = 8000):
    url = f"http://0.0.0.0:{port}/answer"
    data = {"question": "What is the capital of France?"}

    response = requests.get(url, json=data)
    print(response.json())


if __name__ == "__main__":
    Fire(run)
