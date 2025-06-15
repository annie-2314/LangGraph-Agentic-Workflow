from langchain_core.language_models import BaseChatModel
from langchain_core.outputs import ChatGeneration, ChatResult
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class MockLLM(BaseChatModel):
    def __init__(self):
        super().__init__()

    def _generate(self, messages: List[dict], stop: Optional[List[str]] = None, **kwargs) -> ChatResult:
        logger.info(f"Mock generating response for messages: {messages}")
        content = f"Mock response for task: {messages[-1]['content']}"
        generation = ChatGeneration(message={"role": "assistant", "content": content})
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock_llm"

    def predict(self, text: str) -> str:
        logger.info(f"Mock predicting for text: {text}")
        return f"Mock response for task: {text}"

llm = MockLLM()

def tool_agent(task: str) -> str:
    return llm.predict(task)

def fake_tool_selector(task: str) -> str:
    if "search" in task.lower():
        return "Google"
    elif "code" in task.lower():
        return "Jupyter"
    else:
        return "LLM"