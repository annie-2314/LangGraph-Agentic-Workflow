from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from typing import List, Dict
import logging
import time
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

class PlanAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ_API_KEY not found in .env")
            raise ValueError("GROQ_API_KEY not found")
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model="llama3-8b-8192"
        )
        self.prompt = ChatPromptTemplate.from_template(
            "Split the following query into 8-9 specific subtasks to address its requirements. "
            "Return as a bulleted list with one-line descriptive subtasks as full sentences "
            "(5-15 words each, no colons). Example: '- Research project requirements and scope.'\n\n{query}"
        )

    def plan(self, query: str) -> List[Dict[str, str]]:
        try:
            logger.info(f"Processing query: {query}")
            chain = self.prompt | self.llm
            for attempt in range(3):
                try:
                    response = chain.invoke({"query": query})
                    logger.info(f"Groq API response: {response.content}")
                    lines = [line.strip() for line in response.content.split("\n") if line.strip()]
                    tasks = []
                    for line in lines:
                        if line.startswith(("Here are", "To address")):
                            continue
                        cleaned = re.sub(r"^[•\-\*]\s*", "", line).strip()
                        if cleaned:
                            tasks.append({
                                "id": str(len(tasks) + 1),
                                "description": cleaned,
                                "status": "pending"
                            })
                    return tasks[:5] if tasks else [{"id": "1", "description": "No tasks generated", "status": "error"}]
                except Exception as e:
                    logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
                    if attempt < 2:
                        time.sleep(1)
                    else:
                        raise e
        except Exception as e:
            logger.error(f"Error in Groq API call: {str(e)}")
            return [{"id": "1", "description": f"Error: {str(e)}", "status": "error"}]