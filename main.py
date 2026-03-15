from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()


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

    if amount < 1000:

        status = "Auto Approved 🎉"

    elif amount < 10000:

        status = "Manager Approval Required 👨‍💼"

    else:

        status = "Finance Approval Required 💰"

    return {
        "name": expense.name,
        "amount": amount,
        "status": status
    }