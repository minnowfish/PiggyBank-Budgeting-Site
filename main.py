from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

import sqlite3
connection = sqlite3.connect("my_database")

connection.execute('''CREATE TABLE IF NOT EXISTS userData (
date TEXT, 
current_bal INTEGER, 
expense_name STRING, 
expense_value INTEGER, 
income_name STRING, 
income_value INTEGER, 
final_bal INTEGER);''')


app = FastAPI()
def get_db():
   db = session()
   try:
      yield db
   finally:
      db.close()
    
templates = Jinja2Templates(directory = "templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get_data")
async def get_data():
    connection = sqlite3.connect("my_database")
    cursor = connection.cursor()

    cursor.execute("SELECT date, current_bal, expense_name, expense_value, income_name, income_value, final_bal FROM userData")

    data = cursor.fetchall()

    connection.close()
    data_list = []
    for row in data:
        data_list.append({
            "date": row[0],
            "current_bal": row[1],
            "expense_name": row[2],
            "expense_value": row[3],
            "income_name": row[4],
            "income_value": row[5],
            "final_bal": row[6]
        })

    return data_list


