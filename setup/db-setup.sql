create user DATA_TIER_EVENT;
alter user DATA_TIER_EVENT QUOTA UNLIMITED ON USERS;
create table DATA_TIER_EVENT.CURRENT_EVENT_TABLE (
    TABLE_NAME varchar2(32 char)
);
INSERT INTO DATA_TIER_EVENT.CURRENT_EVENT_TABLE 
SELECT null
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM DATA_TIER_EVENT.CURRENT_EVENT_TABLE
);