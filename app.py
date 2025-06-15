import streamlit as st
from main import run_workflow
import json
import base64
import os

# Function to encode image as base64
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        st.warning(f"Image file {image_path} not found. Using default background.")
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set page title
st.title("🧠 Agentic Workflow with LangGraph")

# Add background image
image_path = "assets/bg.jpg"  # Local image path
base64_image = get_base64_image(image_path)
if base64_image:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{base64_image});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp > div {{
            background-color: rgba(255, 255, 255, 0.85);  /* Semi-transparent white overlay */
            padding: 20px;
            border-radius: 10px;
            margin: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    # Fallback CSS without image
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f2f6;  /* Light gray fallback */
        }
        .stApp > div {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 10px;
            margin: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Query input
query = st.text_area("Enter your query:", height=100)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None
if "edit_buffer" not in st.session_state:
    st.session_state.edit_buffer = {}

# Generate tasks button
if st.button("Generate Tasks"):
    if query:
        result = run_workflow(query)
        st.session_state.tasks = result["tasks"]
        st.session_state.workflow_result = result
        st.session_state.edit_buffer = {}
        st.subheader("Generated Tasks:")
        for task in st.session_state.tasks:
            if "Error" in task["description"]:
                st.error(f"Task {task['id']}: {task['description']}")
            else:
                st.write(f"Task {task['id']}: {task['description']}")
    else:
        st.error("Please enter a query.")

# Edit tasks section
if st.session_state.tasks:
    st.subheader("Edit Tasks")
    # Display tasks with consistent IDs
    for task in st.session_state.tasks:
        if task["status"] != "deleted":  # Skip deleted tasks
            st.write(f"- Task {task['id']}: {task['description']} (Status: {task['status']})")
    for task in st.session_state.tasks:
        if task["status"] != "deleted":
            with st.expander(f"Task {task['id']}: {task['description']}"):
                with st.form(key=f"edit_form_{task['id']}"):
                    default_desc = st.session_state.edit_buffer.get(task['id'], task['description'])
                    new_desc = st.text_input(f"Edit description for Task {task['id']}", value=default_desc, key=f"edit_input_{task['id']}")
                    submit = st.form_submit_button(f"Save Task {task['id']}")
                    if submit:
                        st.session_state.edit_buffer[task['id']] = new_desc
                        for t in st.session_state.tasks:
                            if t["id"] == task["id"]:
                                t["description"] = new_desc
                                t["status"] = "pending"
                                st.success(f"Updated Task {task['id']}: {new_desc}")
                                break
                        st.session_state.edit_buffer.pop(task['id'], None)
                        st.rerun()
                if st.button(f"Delete Task {task['id']}", key=f"delete_{task['id']}"):
                    for t in st.session_state.tasks:
                        if t["id"] == task["id"]:
                            t["status"] = "deleted"
                            break
                    st.session_state.edit_buffer.pop(task['id'], None)
                    st.rerun()

    # Add new task form
    with st.form(key="add_task_form"):
        new_task_desc = st.text_input("Add new task description:")
        add_submit = st.form_submit_button("Add Task")
        if add_submit and new_task_desc:
            new_id = max([int(task["id"]) for task in st.session_state.tasks], default=0) + 1
            st.session_state.tasks.append({"id": str(new_id), "description": new_task_desc, "status": "pending"})
            st.rerun()

    # Approve and run workflow button
    if st.button("Approve and Run Workflow"):
        if st.session_state.tasks:
            # Filter out deleted tasks and create edited_tasks
            edited_tasks = [
                {"id": task["id"], "description": task["description"], "status": task["status"]}
                for task in st.session_state.tasks
                if task["status"] != "deleted"
            ]
            if edited_tasks:
                result = run_workflow(query, user_tasks=edited_tasks, approve=True)
                st.session_state.workflow_result = result
                st.subheader("Results")
                for res in result["results"]:
                    st.write(f"Task {res['task_id']}: {res['result']}")
            else:
                st.error("No tasks available to run.")
        else:
            st.error("No tasks to run.")