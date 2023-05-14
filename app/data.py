from langchain.prompts import PromptTemplate
from pydantic import validate_arguments, FilePath

from telegram_loader import TelegramChatLoader
from utils import get_logger

logger = get_logger(__file__)


# __all__ = ["get_formatter", "get_context"]


def get_formatter():
    """
    https://github.com/hwchase17/langchain/blob/master/docs/getting_started/getting_started.md
    """
    prompt_temp = PromptTemplate(
        input_variables=["context", "question"],
        template="### Context:\n{context}\n\n### Human: which message is the most related to this '{question}'\n\n### Assistant:",  # using only data from context
    )
    return prompt_temp


def create_vectorstore():
    raise NotImplementedError()


@validate_arguments
def get_documents(filepath: FilePath):
    loader = TelegramChatLoader(str(filepath))
    return loader.load()


def merge_docs(docs):
    try:
        contents = (i.page_content for i in docs)
    except:
        contents = (i["page_content"] for i in docs)
    merged = "\n\n".join(contents)
    return merged


@validate_arguments
def get_context(query: str, chat_path: FilePath):
    logger.warning("this should be rewritten using langchain retriever")
    logger.warning("query is not used, hardcoded relevant documents")
    documents = get_documents(chat_path)
    context = merge_docs(documents[-230:-220])
    return context
