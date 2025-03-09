from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from DBManager import DBManager
from Source import *

app = FastAPI()
templates = Jinja2Templates(directory="templates")
dbm = DBManager(in_docker=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Strona główna z interfejsem zarządzania.
    """
    try:
        table_name = get_current_event_table(dbm)
        all_tables = get_all_event_tables(dbm)  # Pobranie dostępnych tabel
    except Exception as e:
        table_name = "Error fetching data"
        all_tables = []

    return templates.TemplateResponse("index.html", {
        "request": request,
        "table_name": table_name,
        "all_tables": all_tables
    })

@app.get("/get-current-event-table")
def get_current_event():
    try:
        table_name = get_current_event_table(dbm)
        if table_name is None:
            raise HTTPException(status_code=404, detail="No data found")
        return {"table_name": table_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/set-current-event-table")
async def update_event_table(request: Request, table_name: str = Form(...)):
    try:
        rows_updated = set_current_event_table(dbm, table_name)
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-event-table/{table_name}")
async def create_event_table(table_name: str):
    try:
        create_new_event_table(dbm, table_name)
        return {"message": f"Table '{table_name}' created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
