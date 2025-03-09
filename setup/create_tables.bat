@echo off
setlocal

set "WORK_DIR=%cd%"

cd %WORK_DIR%

set "DB_CONTAINER=cabal-events-utils-database-1"

docker exec -i %DB_CONTAINER% sqlplus sys/admin as sysdba < db-setup.sql