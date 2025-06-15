from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class FeedbackAgent:
    def reflect_and_refine(self, tasks: List[Dict[str, Any]], query: str) -> tuple[List[Dict[str, Any]], List[str]]:
        feedback = []
        refined_tasks = tasks.copy()

        keywords = query.lower().split()
        task_descriptions = [task["description"].lower() for task in refined_tasks]
        for keyword in keywords:
            if len(keyword) > 3 and not any(keyword in desc for desc in task_descriptions):
                feedback.append(f"Adding task for missing aspect: {keyword}")
                refined_tasks.append({
                    "id": str(len(refined_tasks) + 1),
                    "description": f"Address {keyword} in the plan",
                    "status": "pending"
                })

        seen = set()
        i = 0
        while i < len(refined_tasks):
            desc = refined_tasks[i]["description"].lower()
            if desc in seen:
                feedback.append(f"Removing redundant task: {refined_tasks[i]['description']}")
                refined_tasks[i]["status"] = "deleted"
            else:
                seen.add(desc)
            i += 1

        for task in refined_tasks:
            if len(task["description"].split()) < 5 and task["status"] != "deleted":
                feedback.append(f"Modifying vague task: {task['description']}")
                task["description"] = f"Refined: {task['description']} with detailed steps"

        refined_tasks = [task for task in refined_tasks if task["status"] != "deleted"]
        return refined_tasks, feedback

    def needs_refinement(self, tasks: List[Dict[str, Any]], results: List[Dict[str, Any]], query: str) -> bool:
        pending_tasks = any(task["status"] == "pending" for task in tasks)
        completed_task_ids = {result["task_id"] for result in results}
        tasks_needing_results = [task for task in tasks if task["status"] == "completed" and task["id"] not in completed_task_ids]
        return pending_tasks or bool(tasks_needing_results)

    def evaluate_task(self, subtask: str, result: str) -> str:
        logger.info(f"Evaluating subtask: {subtask}, result: {result}")
        if "error" in result.lower():
            return "modify"
        elif "irrelevant" in result.lower():
            return "delete"
        elif len(result.split()) < 5:
            return "add"
        elif len(subtask.split()) < 3:
            return "modify"
        else:
            return "accept"

feedback_agent_instance = FeedbackAgent()

def feedback_agent(subtask: str, result: str) -> str:
    return feedback_agent_instance.evaluate_task(subtask, result)