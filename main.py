from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

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
        status = "Rejected ❌"

    elif amount < 1000:
        status = "Auto Approved 🎉"

    elif amount < 10000:
        status = "Manager Approval Required 👨‍💼"

    else:
        status = "Finance Approval Required 💰"

    workflow_data.append({
        "name": expense.name,
        "amount": amount,
        "status": status
    })

    return {
        "status": status,
        "active": len(workflow_data)
    }


@app.get("/workflows")
def workflows():
    return workflow_data


@app.get("/result/{status}", response_class=HTMLResponse)
def result_page(status: str):

    return f"""
    <html>

    <head>

    <title>Workflow Result</title>

    <style>

    body{{
        font-family:"Times New Roman";
        background:#0f2027;
        color:white;
        text-align:center;
        margin-top:150px;
    }}

    .box{{
        font-size:60px;
        animation:pop 1s infinite alternate;
    }}

    @keyframes pop{{
        from{{transform:scale(1)}}
        to{{transform:scale(1.2)}}
    }}

    a{{
        color:#00c6ff;
        font-size:20px;
    }}

    </style>

    </head>

    <body>

    <div class="box">
    {status}
    </div>

    <br><br>

    <a href="/">⬅ Back to Workflow Dashboard</a>

    </body>

    </html>
    """