from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Optional
from agents.planner import PlanAgent
from agents.tools import tool_agent
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class WorkflowState(TypedDict):
    query: str
    tasks: List[Dict[str, str]]
    current_task_index: int
    results: List[Dict[str, str]]
    iteration_count: int
    user_tasks: Optional[List[Dict[str, str]]]

def plan_node(state: WorkflowState) -> WorkflowState:
    logger.info(f"Planning node, iteration {state.get('iteration_count', 0)}")
    tasks = state.get("user_tasks") or []  # Use user_tasks if provided
    if not tasks:  # Only plan if no user_tasks
        plan_agent = PlanAgent()
        tasks = plan_agent.plan(state["query"])
    return {
        "query": state["query"],
        "tasks": tasks,
        "current_task_index": 0,
        "results": [],
        "iteration_count": state.get("iteration_count", 0) + 1,
        "user_tasks": state.get("user_tasks")
    }

def tool_node(state: WorkflowState) -> WorkflowState:
    if state["current_task_index"] >= len(state["tasks"]):
        logger.info("No more tasks to process in tool node")
        return state
    task = state["tasks"][state["current_task_index"]]
    if task["status"] != "deleted":  # Skip deleted tasks
        result = tool_agent(task["description"])
        task["status"] = "completed"
        state["results"].append({"task_id": task["id"], "result": f"Mock response for task: {task['description']}"})
    return {
        **state,
        "current_task_index": state["current_task_index"] + 1,
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def should_continue(state: WorkflowState) -> str:
    max_iterations = 10
    if state.get("iteration_count", 0) >= max_iterations:
        logger.info(f"Max iterations ({max_iterations}) reached, ending workflow")
        return "end"
    if state["current_task_index"] >= len(state["tasks"]):
        logger.info("All tasks processed, ending workflow")
        return "end"
    return "tool"

def build_workflow():
    graph = StateGraph(WorkflowState)
    graph.add_node("plan", plan_node)
    graph.add_node("tool", tool_node)
    graph.set_entry_point("plan")
    graph.add_edge("plan", "tool")
    graph.add_conditional_edges(
        "tool",
        should_continue,
        {
            "tool": "tool",
            "end": END
        }
    )
    return graph.compile()

def run_workflow(query: str, user_tasks: Optional[List[Dict[str, str]]] = None, approve: bool = False) -> Dict:
    initial_state = {
        "query": query,
        "tasks": user_tasks or [],
        "current_task_index": 0,
        "results": [],
        "iteration_count": 0,
        "user_tasks": user_tasks
    }
    graph = build_workflow()
    result = graph.invoke(initial_state)
    if approve:
        for task in result["tasks"]:
            if task["status"] != "deleted":
                task["status"] = "completed"
    return {
        "query": result["query"],
        "tasks": result["tasks"],
        "results": result["results"]
    }