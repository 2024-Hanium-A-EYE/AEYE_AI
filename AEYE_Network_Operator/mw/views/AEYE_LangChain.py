"""
from langchain import OpenAI
from .AEYE_KEY import aeye_key as key
import os



def aeye_langchain(dissease : str)-> str :
    os.environ["OPENAI_API_KEY"] = key.API

    llm = OpenAI(model_name=key.Model)

    

    return llm.invoke(key.PROMPT + "Disease : {}".format(dissease))
"""