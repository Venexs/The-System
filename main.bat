@echo off

:: Activating the virtual environment
call venv\Scripts\activate

:: Running the Python script using Python 3.9
py -3.9 gui.py

:: Deactivating the virtual environment after the script finishes
deactivate
