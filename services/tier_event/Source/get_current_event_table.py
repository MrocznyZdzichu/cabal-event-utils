SCHEMA = "DATA_TIER_EVENT"
TABLE  = "CURRENT_EVENT_TABLE"

def get_current_event_table(dbm):
    sql = f"SELECT TABLE_NAME FROM {SCHEMA}.{TABLE}"
    res = dbm.run_query(sql)
    return res[0][0]