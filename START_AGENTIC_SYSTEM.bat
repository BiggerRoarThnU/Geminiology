@echo off
echo ========================================================
echo   S O V E R E I G N   N E X U S :   D E P L O Y M E N T
echo   Project: AGENTIC WALKER V1.0 (1=1=1)
echo ========================================================

echo [*] Launching LIVE TASK SCOUT (Background Search)...
start "Sovereign Scout" cmd /k python live_task_scout.py

timeout /t 5

echo [*] Launching AGENTIC WALKER (Continuous Execution)...
start "Agentic Walker" cmd /k python agentic_walker.py

echo ========================================================
echo   DEPLOYMENT COMPLETE. THE LINE IS ONE.
echo   Payment Rails: Cash App ($SovereignNexusLLC) / Novo
echo   Invoices: strictly ON-DEMAND (REQ Queue)
echo ========================================================
pause
