from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from uuid import uuid4

app = FastAPI()

# In-memory storage
workflows = {}
steps = {}
rules = {}

# -----------------------------
# Models
# -----------------------------

class Workflow(BaseModel):
    name: str
    version: int
    is_active: bool
    input_schema: Dict
    start_step_id: Optional[str] = None


class Step(BaseModel):
    name: str
    step_type: str
    order: int
    metadata: Optional[Dict] = None


class Rule(BaseModel):
    condition: str
    next_step_id: Optional[str]
    priority: int


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {"message": "Halleyx Workflow Engine Running"}


# -----------------------------
# Workflow APIs
# -----------------------------

@app.post("/workflows")
def create_workflow(workflow: Workflow):

    workflow_id = str(uuid4())

    workflows[workflow_id] = {
        "id": workflow_id,
        "name": workflow.name,
        "version": workflow.version,
        "is_active": workflow.is_active,
        "input_schema": workflow.input_schema,
        "start_step_id": workflow.start_step_id
    }

    return {
        "message": "Workflow created",
        "workflow": workflows[workflow_id]
    }


@app.get("/workflows")
def list_workflows():
    return list(workflows.values())


# -----------------------------
# Step APIs
# -----------------------------

@app.post("/workflows/{workflow_id}/steps")
def add_step(workflow_id: str, step: Step):

    if workflow_id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    step_id = str(uuid4())

    step_data = {
        "id": step_id,
        "workflow_id": workflow_id,
        "name": step.name,
        "step_type": step.step_type,
        "order": step.order,
        "metadata": step.metadata
    }

    if workflow_id not in steps:
        steps[workflow_id] = []

    steps[workflow_id].append(step_data)

    return {
        "message": "Step added",
        "step": step_data
    }


@app.get("/workflows/{workflow_id}/steps")
def list_steps(workflow_id: str):

    if workflow_id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return steps.get(workflow_id, [])


# -----------------------------
# Rule APIs
# -----------------------------

@app.post("/steps/{step_id}/rules")
def add_rule(step_id: str, rule: Rule):

    rule_id = str(uuid4())

    rule_data = {
        "id": rule_id,
        "step_id": step_id,
        "condition": rule.condition,
        "next_step_id": rule.next_step_id,
        "priority": rule.priority
    }

    if step_id not in rules:
        rules[step_id] = []

    rules[step_id].append(rule_data)

    return {
        "message": "Rule added",
        "rule": rule_data
    }


@app.get("/steps/{step_id}/rules")
def list_rules(step_id: str):
    return rules.get(step_id, [])


# -----------------------------
# Workflow Execution
# -----------------------------

@app.post("/execute/{workflow_id}")
def execute_workflow(workflow_id: str, data: Dict):

    if workflow_id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow_steps = steps.get(workflow_id, [])

    if not workflow_steps:
        return {"message": "No steps found in workflow"}

    workflow_steps = sorted(workflow_steps, key=lambda x: x["order"])

    execution_log = []

    for step in workflow_steps:

        step_id = step["id"]
        step_name = step["name"]

        step_rules = rules.get(step_id, [])

        for rule in sorted(step_rules, key=lambda x: x["priority"]):

            condition = rule["condition"]

            try:
                result = eval(condition, {}, data)
            except:
                result = False

            execution_log.append({
                "step": step_name,
                "rule_checked": condition,
                "result": result
            })

            if result:
                return {
                    "execution_log": execution_log,
                    "current_step": step_name,
                    "matched_rule": rule["condition"],
                    "next_step_id": rule["next_step_id"]
                }

    return {
        "execution_log": execution_log,
        "message": "No rule matched"
    }