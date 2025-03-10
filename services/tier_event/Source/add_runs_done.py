SCHEMA = "DATA_TIER_EVENT"

def add_runs_done(dbm, table_name, week, dayofweek, tier, dungeon, run_count=1):
    sql = f"""
    INSERT INTO {SCHEMA}.{table_name} (WEEK, DAYOFWEEK, TIER, DUNGEON)
    VALUES (:week, :dayofweek, :tier, :dungeon)
    """
    for it in range(1, run_count+1):
        dbm.execute_insert(sql, {'week': week, 'dayofweek': dayofweek, 'tier': tier, 'dungeon': dungeon})