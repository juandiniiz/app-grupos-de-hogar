@echo off
echo Starting Grupos de Hogar Frontend...
cd /d "%~dp0frontend"

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing npm dependencies...
    npm install
)

echo.
echo Frontend running at http://localhost:5173
echo.
npm run dev
