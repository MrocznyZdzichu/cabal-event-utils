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