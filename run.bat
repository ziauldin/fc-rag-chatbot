@echo off
echo ===========================================
echo    STARTING FC TRAINING RAG CHATBOT
echo ===========================================
echo.

REM ---- CHANGE DIRECTORY TO PROJECT FOLDER ----
cd /d "%~dp0"

REM ---- CHECK IF PYTHON EXISTS ----
echo Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not added to PATH.
    pause
    exit /b
)

REM ---- ACTIVATE VENV IF EXISTS ----
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
)

REM ---- INSTALL REQUIRED PACKAGES ----
echo Installing required Python packages...
pip install -r requirements.txt

REM ---- DELETE OLD CHROMADB VECTOR DB ----
echo Resetting old ChromaDB database...
if exist "vector_db" (
    rmdir /s /q vector_db
    echo Old vector database removed.
) else (
    echo No existing vector db found. Skipping.
)

REM ---- STARTING FLASK SERVER ----
echo Launching FC Training RAG Chatbot...
start "" http://127.0.0.1:5000

python app.py

echo.
echo Chatbot stopped.
pause
