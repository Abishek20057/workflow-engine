# Workflow Automation Engine

This project is a workflow automation system built using Python and FastAPI.

Features:
- Create workflows
- Add steps
- Define rules
- Execute workflows

Run project:

pip install -r requirements.txt
uvicorn main:app --reload
User / Browser
        │
        ▼
FastAPI Backend
        │
        ▼
Workflow Engine
        │
        ├── Workflows
        ├── Steps
        └── Rules
        │
        ▼
Execution Result