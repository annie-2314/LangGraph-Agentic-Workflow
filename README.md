# Agentic Workflow with LangGraph

This repository implements an agentic workflow using LangGraph, featuring a pipeline that splits user queries into subtasks, solves them iteratively with tools, and supports task modification via a Streamlit UI. The solution is hosted live for testing and includes a video explanation.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Live Demo](#live-demo)
- [Video Explanation](#video-explanation)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [License](#license)

---

## Project Overview

This project fulfills an agentic workflow task, leveraging LangGraph to manage task planning, execution, and refinement. A *PlanAgent* decomposes queries into 7–8 descriptive subtasks, a *ToolAgent* executes tasks, and a *Streamlit UI* allows users to edit, delete, or add tasks. The workflow ensures robust error handling and accurate results, with a local background image (assets/bg.jpg) for visual appeal.

---

## Features

- *Query Decomposition*: Generates 7–8 one-line subtasks (5–15 words) per query.
- *Task Management*: Supports modifying, deleting, and adding tasks via Streamlit UI.
- *Task Execution*: Uses a mock ToolAgent to simulate task resolution.
- *Error Handling*: Manages API failures and LangGraph recursion errors.
- *Streamlit UI*: Interactive interface with a custom background image.
- *LangGraph Integration*: Orchestrates workflow with state management.

---

## Architecture

The workflow follows a cyclical process:

- *PlanAgent* (agents/planner.py): Uses Groq API to split queries into 7–8 subtasks.
- *ToolAgent* (agents/tools.py): Executes tasks using a mock LLM.
- *Workflow* (main.py): Manages state and transitions using LangGraph.
- *UI* (app.py): Streamlit interface for query input and task management.

### LangGraph Flow

- *Nodes*: plan, tool
- *Edges*: plan → tool → conditional (tool or end)
- *State*: Tracks query, tasks, results, and iterations to prevent recursion errors

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Git
- Groq API Key (https://console.groq.com)
- JPEG image named bg.jpg in assets/ for background

### Steps

1. *Clone the Repository*:

   bash
   git clone https://github.com/annie-2314/LangGraph-Agentic-Workflow.git
   cd agentic-workflow-langgraph
   

2. *Create a Virtual Environment*:

   bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   

3. *Install Dependencies*:

   bash
   pip install --upgrade pip
   pip install -r requirements.txt
   

4. *Set Up Environment Variables*:

   - Copy .env.example to .env:

     bash
     cp .env.example .env
     

   - Add your Groq API key to .env:

     
     GROQ_API_KEY=your_groq_api_key_here
     

5. *Add Background Image*:

   - Place a JPEG named bg.jpg inside the assets/ folder.

6. *Run the Application*:

   bash
   streamlit run app.py
   

   Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

- *Enter a Query*: Input a query (e.g., "Plan a day") in the Streamlit UI.
- *Generate Tasks*: Click "Generate Tasks" to view 7–8 subtasks.
- *Edit Tasks*: Modify, delete, or add tasks using the UI.
- *Run Workflow*: Click "Approve and Run Workflow" to see results.

### Example Query: "Plan a day" Output

- Task 1: Set clear goals and prioritize daily tasks.
- Task 2: Create a schedule with time allocations.
- Task 3: Organize essential meetings and appointments.
- Task 4: Plan focused work sessions to avoid distractions.
- Task 5: Allocate time for breaks and self-care.
- Task 6: Review and adjust the plan for flexibility.
- Task 7: Identify resources needed for tasks.
- Task 8: Track progress and note incomplete tasks.

---

## Screenshots

### Initial Screen

![Initial Screen of the Streamlit App](assets/1st%20web%20page.png)

### Generate Tasks

![Generate Tasks](assets/query%20and%20gen%20tasks.png)

### Modify Task

![Modify Task](assets/modify%20task.png)

### Modified Task Display

![Modified Task Display](assets/show%20modification.png)

### Delete Task

![Delete Task](assets/del%20task%20showing.png)

### Add Task

![Add Task](assets/add%20task%206.png)

### Added Task Display

![Add Task Display](assets/show%20added%20task.png)

---

## Live Demo

🟢 Hosted Live on Streamlit:  
[https://agentic-workflow-langgraph.streamlit.app](https://agentic-workflow-langgraph.streamlit.app)

---

## Video Explanation

🎥 A 5–10 minute walkthrough is available here:  
[YouTube Link](https://www.google.com/search?q=Your-Video-Link-Here)

---

## Technologies Used

- *LangGraph* – Workflow orchestration
- *Streamlit* – UI framework
- *Groq API* – LLM for task planning
- *Python* – Core programming
- *LangChain* – LLM tool integration
- *Other Dependencies* – Listed in requirements.txt

---

## File Structure


agentic-workflow/
├── agents/
│   ├── __init__.py
│   ├── planner.py          # PlanAgent for query decomposition
│   ├── tools.py            # ToolAgent for task execution
│   └── feedback.py         # Unused feedback agent
├── assets/
│   └── bg.jpg              # Background image for UI   
├── app.py                  # Streamlit UI
├── main.py                 # LangGraph workflow orchestration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md               # Project documentation
└── .gitignore              # Git ignore rules


---

