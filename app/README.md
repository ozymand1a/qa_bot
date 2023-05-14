# How to start a web service

1. install dependencies
```poetry install```
2. enter to poetry environment
```poetry shell```

## Start a document retrieval system
```python
uvicorn document_retrieval_system:app  --port 8866 --host 0.0.0.0
```


## Start model inference service

```python
uvicorn server:app  --port 8867 --host 0.0.0.0
```

## Make a request

```python
python client.py ask_question --llm_port 8867 --docs_search_port 8866 --question "football related project"
```

Result:
```
### Context:
None on 2019-01-31T20:38:37: I am learning new Python and I want to help design a site that presents the results of the names of the competing teams and the results in football

Jonathan Konyi on 2022-09-05T21:58:02: Hi !
Some tutorial for making live score football website in django

Neymar on 2021-02-27T13:26:03: Can anyone suggest a basic project in web development?

### Human: which message is the most related to this 'football related project'

### Assistant: The message from Jonathan Konyi is the most related to the football related project.
```
