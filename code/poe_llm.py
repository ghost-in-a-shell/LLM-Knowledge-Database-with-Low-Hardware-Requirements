import logging
from poe_api_wrapper import PoeApi
import variables
from typing import Optional, List, Dict, Mapping, Any

import langchain
from langchain.llms.base import LLM
from langchain.cache import InMemoryCache

logging.basicConfig(level=logging.INFO)
# 启动llm的缓存
langchain.llm_cache = InMemoryCache()

class PoeClient(LLM):

    @property
    def _llm_type(self) -> str:
        return "poe_chinchilla"

    
    def _call(self, message: str, 
        stop: Optional[List[str]] = None) -> str:
        """_call
        """
        client = PoeApi(variables.TOKEN)
        chat_id=variables.CHAT_ID
        bot=variables.POE_BOT
        print(message)
        if message =="!clear":
            client.chat_break(bot, chatId=chat_id)
            return "Context is now cleared"
        else:
            return client.send_message(bot, message, chat_id)
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters.
        """
        _param_dict = {
            "desc": "poe_api_chinchilla"
        }
        return _param_dict