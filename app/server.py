from pathlib import Path
from typing import List

import torch
from fastapi import FastAPI
from model import get_model, get_response
from pydantic import BaseModel
from type_defs import Prompt, Question, QuestionNContext
from utils import get_logger

from data import get_context, get_formatter, merge_docs

# todo: log into file !!!


class QAService:
    def __init__(self, model, tokenizer, device):
        self.prompt_formatter = get_formatter()
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def _question2prompt(self, question: str, context: List) -> str:
        merged_context = merge_docs(context)
        prompt = self.prompt_formatter.format(context=merged_context, question=question)
        return prompt

    def _process_prompt(self, prompt: str):
        response = get_response(prompt, self.model, self.tokenizer, self.device)
        torch.cuda.empty_cache()
        return response

    def _postprocess_answer(self):
        pass

    def process_question(self, question: str, context: List) -> str:
        """Method to define a business logic"""
        prompt = self._question2prompt(question, context)
        response = self._process_prompt(prompt)
        return response


app = FastAPI()

logger = get_logger(__name__)


DEVICE = torch.device("cuda:1")

model, tokenizer = get_model()
logger.warning("bad thing happened here")
model.to(DEVICE)  # todo: handle this
service = QAService(model=model, tokenizer=tokenizer, device=DEVICE)


class Metadata(BaseModel):
    source: str


class ContextModel(BaseModel):
    metadata: Metadata
    page_content: str


class QuestionModel(BaseModel):
    question: str
    context: List[ContextModel]


@app.get("/api_v1/ask")  # List[dict]  # question: Question,
async def query_w_context(data: QuestionModel):
    """Process prompt using LLM, prompt should have a context"""
    answer = service.process_question(data.question, data.context)
    return {"answer": answer}
