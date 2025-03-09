from fastapi import FastAPI, HTTPException

from DBManager import DBManager
from Source import *

app = FastAPI()

dbm = DBManager(in_docker=True)

@app.get("/get-current-event-table")
def get_current_event():
    try:
        table_name = get_current_event_table(dbm)
        if table_name is None:
            raise HTTPException(status_code=404, detail="Brak danych w tabeli")
        return {"table_name": table_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))