import torch
from transformers import AutoModelForCausalLM, LlamaTokenizer

from utils import get_logger


logger = get_logger(__name__)


def get_model():
    """Returns StableLM model and tokenizer"""
    logger.warning("Using a model StableLM of size 26GB!")
    model_id = "thebloke/stable-vicuna-13B-HF"
    tokenizer = LlamaTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id
    )  # , device_map="auto", load_in_8bit=False)
    return model, tokenizer


def get_response(prompt, model, tokenizer, device=torch.device("cpu")):
    """Process input prompt and return processed model output"""
    # todo: handle different devices
    logger.warning("different devices are not handled")
    logger.info("Processing the input")
    ids = tokenizer.encode(prompt, return_tensors="pt")
    ids = ids.to(device)
    output_ids = model.generate(ids, max_length=1024)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text
