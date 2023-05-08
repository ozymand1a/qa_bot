# [+-] Stage 1
# given preload database, retrieve some messages
# and respond to the question

# [ ] Stage 2
# Ability to change a database to query from
# %%

import torch
from fastapi import FastAPI

from model import get_model, get_response
from data import get_formatter, get_context
from utils import get_logger

# %%
from pathlib import Path
from utils import get_data_path
# get_data_path()
question = "which message from the context says about problem with bots?"
chat_path = Path(__file__).parent.parent / 'data' / 'django_chat_history.json'
context = get_context(question, chat_path)
prompt_formatter = get_formatter()

prompt = prompt_formatter.format(context=context, question=question)

# %%
logger = get_logger(__name__)
model, tokenizer = get_model()
# app = FastAPI()


# @app.get("/")
# async def root():
#     """
#         https://server-ip.com:8887/q?who-wrote-about-camping?
#     """

# %%
response = get_response(prompt, model, tokenizer)

print(response)
    # postprocess the response

    # torch.cuda.empty_cache()
    
    # return {"message": response}

