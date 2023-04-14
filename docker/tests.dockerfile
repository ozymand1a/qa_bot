FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1

RUN mkdir /qa_bot
WORKDIR /qa_bot

COPY requirements.txt /qa_bot
RUN pip install -U pip && pip install -U setuptools && pip install -r requirements.txt

COPY . /qa_bot

ENTRYPOINT ["sh", "entrypoint.sh"]
