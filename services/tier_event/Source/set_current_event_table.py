SCHEMA = "DATA_TIER_EVENT"
TABLE  = "CURRENT_EVENT_TABLE"

def set_current_event_table(dbm, new_table_name):
    sql = f"update {SCHEMA}.{TABLE} set TABLE_NAME = :table_name"
    res = dbm.execute_update(sql, {'table_name': f'{new_table_name}'})
    _recreate_summary_views(dbm, new_table_name)
    return res

def _create_tiers_runs_in_week_view(dbm, current_table_name):
    sql = f"""
CREATE OR REPLACE VIEW {SCHEMA}.V_TIER_RUNS_IN_WEEK as
select
	WEEK
	,TIER
	,count(*) as RUN_COUNT
from {SCHEMA}.{current_table_name}
group by
	WEEK
	,TIER
    """
    dbm.execute_insert(sql, {})

def _create_dung_runs_per_week_view(dbm, current_table_name):
    sql = f"""
    CREATE OR REPLACE VIEW {SCHEMA}.V_DUNGS_PER_WEEK as 
SELECT
	WEEK
	,TIER
	,DUNGEON
	,count(*) as RUN_COUNT
from {SCHEMA}.{current_table_name}
group by
	WEEK
	,TIER
	,DUNGEON
"""
    dbm.execute_insert(sql, {})

def _create_dung_runs_per_day_view(dbm, current_table_name):
    sql = f"""
CREATE OR REPLACE VIEW {SCHEMA}.V_DUNGS_PER_DAY as 
select
	WEEK
	,DAYOFWEEK
	,TIER
	,DUNGEON
	,count(*) as RUN_COUNT
from {SCHEMA}.{current_table_name}
group by
	WEEK
	,DAYOFWEEK
	,DUNGEON
	,TIER
    """
    dbm.execute_insert(sql, {})

def _recreate_summary_views(dbm, current_table_name):
    _create_tiers_runs_in_week_view(dbm, current_table_name)
    _create_dung_runs_per_week_view(dbm, current_table_name)
    _create_dung_runs_per_day_view(dbm, current_table_name)