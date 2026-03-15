from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# store workflow history
workflow_data = []


class Expense(BaseModel):
    name: str
    amount: int


# Home page
@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend.html") as f:
        return f.read()


# Submit expense
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

    # save workflow entry
    workflow_entry = {
        "name": expense.name,
        "amount": amount,
        "status": status
    }

    workflow_data.append(workflow_entry)

    return {
        "status": status,
        "active": len(workflow_data)
    }


# Animated result page
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

    .result{{
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

    <div class="result">
    {status}
    </div>

    <br><br>

    <a href="/">⬅ Back to Dashboard</a>

    </body>

    </html>
    """


# Workflow history table
@app.get("/workflows", response_class=HTMLResponse)
def workflows():

    rows = ""

    for w in workflow_data:
        rows += f"""
        <tr>
            <td>{w['name']}</td>
            <td>{w['amount']}</td>
            <td>{w['status']}</td>
        </tr>
        """

    return f"""
    <html>

    <head>

    <title>Workflow History</title>

    <style>

    body{{
        font-family:"Times New Roman";
        background:#0f2027;
        color:white;
        text-align:center;
        padding:40px;
    }}

    table{{
        margin:auto;
        border-collapse:collapse;
        width:70%;
        background:#1e3c5a;
    }}

    th,td{{
        padding:15px;
        border:1px solid #00c6ff;
    }}

    th{{
        background:#00c6ff;
        color:black;
    }}

    tr:hover{{
        background:#2c5364;
    }}

    a{{
        color:#00c6ff;
        font-size:18px;
    }}

    </style>

    </head>

    <body>

    <h1>Workflow History</h1>

    <table>

    <tr>
        <th>Employee Name</th>
        <th>Amount</th>
        <th>Status</th>
    </tr>

    {rows}

    </table>

    <br><br>

    <a href="/">⬅ Back to Dashboard</a>

    </body>

    </html>
    """