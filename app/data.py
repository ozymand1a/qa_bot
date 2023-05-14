from langchain.prompts import PromptTemplate
from pydantic import validate_arguments, FilePath

from telegram_loader import TelegramChatLoader 
from utils import get_logger

logger = get_logger(__file__)


def get_formatter():
    """
    https://github.com/hwchase17/langchain/blob/master/docs/getting_started/getting_started.md
    """
    prompt_temp = PromptTemplate(
        input_variables=["context", "question"],
        template="### Context:\n{context}\n\n### Human: {question}\n\n### Assistant:"
    )
    return prompt_temp


def create_vectorstore():
    raise NotImplementedError()


@validate_arguments
def get_documents(filepath: FilePath):
    loader = TelegramChatLoader(str(filepath))
    return loader.load()


def merge_docs(docs):
    contents = (i.page_content for i in docs)
    merged = "\n\n".join(contents)
    return merged


@validate_arguments
def get_context(query: str, chat_path: FilePath):
    logger.warning("this should be rewritten using langchain retriever")
    logger.warning("query is not used, hardcoded relevant documents")
    documents = get_documents(chat_path)
    context = merge_docs(documents[-230:-220])
    return context
