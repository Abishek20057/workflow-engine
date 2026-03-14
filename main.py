from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid

app = FastAPI()

# -------------------------------
# In-memory storage
# -------------------------------

workflows = {}
steps = {}
rules = {}

# -------------------------------
# Models
# -------------------------------

class Workflow(BaseModel):
    name: str
    version: int
    is_active: bool
    input_schema: dict
    start_step_id: str | None = None


class Step(BaseModel):
    name: str
    step_type: str
    order: int
    metadata: dict | None = None


class Rule(BaseModel):
    condition: str
    next_step_id: str | None
    priority: int


class Expense(BaseModel):
    name: str
    amount: int


# -------------------------------
# Homepage
# -------------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend.html") as f:
        return f.read()


# -------------------------------
# Workflow APIs
# -------------------------------

@app.post("/workflows")
def create_workflow(workflow: Workflow):

    workflow_id = str(uuid.uuid4())

    workflows[workflow_id] = {
        "id": workflow_id,
        "name": workflow.name,
        "version": workflow.version,
        "is_active": workflow.is_active,
        "input_schema": workflow.input_schema,
        "start_step_id": workflow.start_step_id
    }

    return {"message": "Workflow created", "workflow": workflows[workflow_id]}


@app.get("/workflows")
def list_workflows():
    return list(workflows.values())


# -------------------------------
# Steps APIs
# -------------------------------

@app.post("/workflows/{workflow_id}/steps")
def add_step(workflow_id: str, step: Step):

    if workflow_id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    step_id = str(uuid.uuid4())

    steps[step_id] = {
        "id": step_id,
        "workflow_id": workflow_id,
        "name": step.name,
        "step_type": step.step_type,
        "order": step.order,
        "metadata": step.metadata
    }

    return {"message": "Step added", "step": steps[step_id]}


@app.get("/workflows/{workflow_id}/steps")
def list_steps(workflow_id: str):

    result = []

    for step in steps.values():
        if step["workflow_id"] == workflow_id:
            result.append(step)

    return result


# -------------------------------
# Rules APIs
# -------------------------------

@app.post("/steps/{step_id}/rules")
def add_rule(step_id: str, rule: Rule):

    if step_id not in steps:
        raise HTTPException(status_code=404, detail="Step not found")

    rule_id = str(uuid.uuid4())

    rules[rule_id] = {
        "id": rule_id,
        "step_id": step_id,
        "condition": rule.condition,
        "next_step_id": rule.next_step_id,
        "priority": rule.priority
    }

    return {"message": "Rule added", "rule": rules[rule_id]}


@app.get("/steps/{step_id}/rules")
def list_rules(step_id: str):

    result = []

    for rule in rules.values():
        if rule["step_id"] == step_id:
            result.append(rule)

    return result


# -------------------------------
# Workflow Execution
# -------------------------------

@app.post("/execute/{workflow_id}")
def execute_workflow(workflow_id: str):

    if workflow_id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow = workflows[workflow_id]
    current_step_id = workflow["start_step_id"]

    execution_log = []

    while current_step_id:

        step = steps.get(current_step_id)

        if not step:
            break

        execution_log.append(f"Executing step: {step['name']}")

        step_rules = [
            r for r in rules.values() if r["step_id"] == current_step_id
        ]

        step_rules.sort(key=lambda x: x["priority"])

        next_step = None

        for rule in step_rules:
            if rule["condition"] == "DEFAULT":
                next_step = rule["next_step_id"]
                break

        current_step_id = next_step

    return {
        "message": "Workflow executed",
        "log": execution_log
    }


# -------------------------------
# Expense Workflow (User Friendly)
# -------------------------------

@app.post("/submit-expense")
def submit_expense(expense: Expense):

    amount = expense.amount

    if amount < 1000:
        status = "Auto Approved"

    elif amount < 10000:
        status = "Manager Approval Required"

    else:
        status = "Finance Approval Required"

    return {
        "message": f"Request submitted by {expense.name}",
        "amount": amount,
        "status": status
    }