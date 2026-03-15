from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# store workflows
workflow_data = []

class Expense(BaseModel):
    name: str
    amount: int


@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend.html") as f:
        return f.read()


@app.post("/submit-expense")
def submit_expense(expense: Expense):

    amount = expense.amount

    if amount < 500:
        status = "❌ Rejected"

    elif amount < 1000:
        status = "🎉 Auto Approved"

    elif amount < 10000:
        status = "👨‍💼 Manager Approval Required"

    else:
        status = "💰 Finance Approval Required"


    # store workflow entry
    workflow_entry = {
        "name": expense.name,
        "amount": amount,
        "status": status
    }

    workflow_data.append(workflow_entry)

    return {
        "name": expense.name,
        "amount": amount,
        "status": status,
        "active": len(workflow_data)
    }


@app.get("/workflows")
def get_workflows():
    return workflow_data