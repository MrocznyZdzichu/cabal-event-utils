SCHEMA = "DATA_TIER_EVENT"
TABLE  = "CURRENT_EVENT_TABLE"

def set_current_event_table(dbm, new_table_name):
    sql = f"update {SCHEMA}.{TABLE} set TABLE_NAME = :table_name"
    res = dbm.execute_update(sql, {'table_name': f'{new_table_name}'})
    return res