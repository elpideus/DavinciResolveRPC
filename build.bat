@echo off
setlocal

echo ============================================================
echo  DaVinci Resolve RPC - Build Script
echo ============================================================
echo.

REM Activate venv if present
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo [1/4] Installing / updating dependencies...
pip install --quiet pypresence psutil pystray Pillow pyinstaller
if errorlevel 1 goto :error

echo [2/4] Generating icon...
python generate_icon.py
if errorlevel 1 goto :error

echo [3/4] Building executable with PyInstaller...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "DaVinciResolveRPC" ^
    --icon "icon.ico" ^
    --add-data "icon.ico;." ^
    resolve_rpc.py
if errorlevel 1 goto :error

echo [4/4] Done!
echo.
echo Output: dist\DaVinciResolveRPC.exe
echo.
echo Next step: compile installer.iss with Inno Setup to produce the installer.
goto :end

:error
echo.
echo Build failed. See error above.
exit /b 1

:end
endlocal
