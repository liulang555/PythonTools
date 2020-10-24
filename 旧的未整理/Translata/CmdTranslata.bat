@echo off
cls
set PATH=%PATH%;
:my_loop
if "%~1"=="" goto completed
echo %1
"python" "D:\QQCloudSync\Python\Translata\Translata.py" %1
SHIFT
goto my_loop
:completed
PAUSE
