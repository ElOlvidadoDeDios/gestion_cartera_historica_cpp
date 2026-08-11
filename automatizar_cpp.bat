@echo off
chcp 65001 > nul

echo ============================================================
echo   ETL UNIFICADO - GESTION Y ACTUALIZACION DE CARTERA
echo ============================================================
echo/

cd /d "D:\Proyectos\gestion_cartera_historica_cpp"

REM ---> AQUI ESTA LA MAGIA: Entramos a la burbuja <---
call env\Scripts\activate

echo [1/3] Sincronizando productividad diaria (Tiempo Real)...
python sync_productividad_diaria.py
if errorlevel 1 (
    echo [ERROR] Fallo en la sincronizacion diaria.
    pause
    exit /b
)
echo/

echo [2/3] Sincronizando metas y cartera mensual (Agencias/Asesores)...
python sync_cartera_mensual.py
if errorlevel 1 (
    echo [ERROR] Fallo en el proceso de cartera mensual.
    pause
    exit /b
)
echo/

echo [3/3] Ejecutando pipeline historico y refresco de Power BI...
python main.py variational
if errorlevel 1 (
    echo [ERROR] Fallo en el pipeline principal (variational).
    pause
    exit /b
)
echo/

echo ============================================================
echo   PROCESO COMPLETADO CON EXITO
echo ============================================================

REM ---> Salimos de la burbuja <---
deactivate

timeout /t 5 >nul