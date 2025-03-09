SCHEMA = "DATA_TIER_EVENT"
RESERVED_NAMES = ['CURRENT_EVENT_TABLE']

def get_all_event_tables(dbm):
    sql = f"SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = '{SCHEMA}' and TABLE_NAME not in ({','.join([f'\'{x}\'' for x in RESERVED_NAMES])})"
    res = dbm.run_query(sql)
    return [x[0] for x in res]