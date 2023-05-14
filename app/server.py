from pathlib import Path

import torch
from fastapi import FastAPI
from pydantic import BaseModel

from model import get_model, get_response
from utils import get_data_path, get_logger
from data import get_context, get_formatter

# todo: Ability to change a database to query from
# todo: log to file !!!
# todo: another endpoints for adding new messages(as text or as file)


class Question(BaseModel):
    question: str


class QAService:
    def __init__(
        self,
        model,
        tokenizer,
        device,
        chat_path: Path = Path(__file__).parent.parent
        / "data"
        / "django_chat_history.json",
    ):
        self.chat_path = chat_path
        self.prompt_formatter = get_formatter()
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def question2prompt(self, question: Question) -> str:
        context = get_context(question.question, self.chat_path)
        prompt = self.prompt_formatter.format(context=context, question=question)
        return prompt

    def process_prompt(self, prompt: str):
        response = get_response(prompt, self.model, self.tokenizer, self.device)
        torch.cuda.empty_cache()
        return response

    def process_question(self, question: Question) -> str:
        """Method to define a business logic"""
        prompt = self.question2prompt(question)
        response = self.process_prompt(prompt)
        return response

    def _postprocess_answer(self):
        pass


app = FastAPI()

logger = get_logger(__name__)

import torch

DEVICE = torch.device("cuda:1")


model, tokenizer = get_model()
logger.warning("bad thing happened here")
model.to(DEVICE)  # todo: handle this
service = QAService(model=model, tokenizer=tokenizer, device=DEVICE)


@app.get("/answer")
async def query(question: Question):
    """Process question using LLM on the chat history"""
    logger.info(f"received a request with question: {question.question}")
    answer = service.process_question(question)
    return {"answer": answer}
