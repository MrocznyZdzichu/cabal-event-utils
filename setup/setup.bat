@echo off
setlocal

set "WORK_DIR=%cd%"

cd %WORK_DIR%

@REM cd ..

echo Creating a Python virtual environment cabal-event-utils in %cd%
python -m venv cabal-event-utils
call cabal-event-utils\Scripts\activate

echo Installing Python libraries
pip install -r setup\requirements.txt

echo Registering the venv as a Jupyter kernel
pip install ipykernel
jupyter kernelspec remove -f -y cabal-event-utils
python -m ipykernel install --user --name=cabal-event-utils

echo Creating databases and registered services if any

python run_compose.py
timeout /t 60 /nobreak

echo Configuring the databases
cd setup

set "DB_CONTAINER=cabal-events-utils-database-1"

docker exec -i %DB_CONTAINER% sqlplus sys/admin as sysdba < db-setup.sql