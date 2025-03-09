SCHEMA = "DATA_TIER_EVENT"

def create_new_event_table(dbm, table_name):
    sql = f"""
create table {SCHEMA}.{table_name} (
	"WEEK"	NUMBER,
	"DAYOFWEEK"	NUMBER,
	"TIER"	VARCHAR2(2 CHAR),
	"DUNGEON"	VARCHAR2(16 CHAR)
)
    """
    dbm.execute_insert(sql, {})