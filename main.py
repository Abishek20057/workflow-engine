from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import re

app = FastAPI()


class Expense(BaseModel):
    name: str
    amount: int


@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/submit-expense")
def submit_expense(expense: Expense):

    name = expense.name
    amount = expense.amount

    # Validate employee name
    if not re.match("^[A-Za-z ]+$", name):
        return {"status": "❌ Employee name must contain only alphabets"}

    # Approval Logic
    if amount < 500:
        status = "❌ Request Rejected (Minimum amount is 500)"

    elif amount < 5000:
        status = "👨‍💼 Manager Approval Required"

    else:
        status = "💰 Finance Approval Required"

    return {
        "name": name,
        "amount": amount,
        "status": status
    }