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
    Strona główna z interfejsem zarządzania oraz podsumowaniem statystyk.
    """
    try:
        table_name = get_current_event_table(dbm)
        all_tables = get_all_event_tables(dbm)
        
        # Pobranie danych ze statystycznych widoków
        sql_tier_runs = "SELECT * FROM DATA_TIER_EVENT.V_TIER_RUNS_IN_WEEK order by week, tier"
        summary_tier_runs = dbm.run_query(sql_tier_runs, {})
        
        sql_dungs_week = "SELECT * FROM DATA_TIER_EVENT.V_DUNGS_PER_WEEK order by week, tier, dungeon"
        summary_dungs_week = dbm.run_query(sql_dungs_week, {})
        
        sql_dungs_day = "SELECT * FROM DATA_TIER_EVENT.V_DUNGS_PER_DAY order by week, dayofweek, tier, dungeon"
        summary_dungs_day = dbm.run_query(sql_dungs_day, {})

    except Exception as e:
        table_name = "Error fetching data"
        all_tables = []
        summary_tier_runs = []
        summary_dungs_week = []
        summary_dungs_day = []

    return templates.TemplateResponse("index.html", {
        "request": request,
        "table_name": table_name,
        "all_tables": all_tables,
        "summary_tier_runs": summary_tier_runs,
        "summary_dungs_week": summary_dungs_week,
        "summary_dungs_day": summary_dungs_day,
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

@app.post("/add-tier-run")
async def add_tier_run(
    week: int = Form(...),
    dayofweek: int = Form(...),
    tier: str = Form(...),
    dungeon: str = Form(...),
    run_count: int = Form(...)
):
    try:
        current_table = get_current_event_table(dbm)
        add_runs_done(dbm, current_table, week, dayofweek, tier, dungeon, run_count)
        return {"message": "Runs added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-summary-data")
async def get_summary_data():
    try:
        sql_tier_runs = "SELECT * FROM DATA_TIER_EVENT.V_TIER_RUNS_IN_WEEK order by week, tier"
        summary_tier_runs = dbm.run_query(sql_tier_runs, {})
        
        sql_dungs_week = "SELECT * FROM DATA_TIER_EVENT.V_DUNGS_PER_WEEK order by week, tier, dungeon"
        summary_dungs_week = dbm.run_query(sql_dungs_week, {})
        
        sql_dungs_day = "SELECT * FROM DATA_TIER_EVENT.V_DUNGS_PER_DAY order by week, dayofweek, tier, dungeon"
        summary_dungs_day = dbm.run_query(sql_dungs_day, {})

        return {
            "summary_tier_runs": summary_tier_runs,
            "summary_dungs_week": summary_dungs_week,
            "summary_dungs_day": summary_dungs_day,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
