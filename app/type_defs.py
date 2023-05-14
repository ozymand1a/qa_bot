from pydantic import BaseModel


class Question(BaseModel):
    question: str


class Prompt(BaseModel):
    prompt: str


class QuestionNContext(BaseModel):
    question: str
    context: str
