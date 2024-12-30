@echo off
call venv\Scripts\activate || echo "Activate virtual environment failed. Make sure it exists."
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
