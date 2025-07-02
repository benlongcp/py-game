@echo off
REM Quick script creator for tests folder
REM Usage: new_test.bat test_my_feature
REM        new_test.bat debug_my_issue  
REM        new_test.bat demo_my_feature

if "%1"=="" (
    echo Usage: new_test.bat [script_name]
    echo Examples:
    echo   new_test.bat test_my_feature
    echo   new_test.bat debug_my_issue
    echo   new_test.bat demo_my_feature
    exit /b 1
)

set SCRIPT_NAME=%1
if not "%SCRIPT_NAME:~0,5%"=="test_" (
    if not "%SCRIPT_NAME:~0,6%"=="debug_" (
        if not "%SCRIPT_NAME:~0,5%"=="demo_" (
            echo ERROR: Script name must start with test_, debug_, or demo_
            exit /b 1
        )
    )
)

set TARGET_FILE=tests\%SCRIPT_NAME%.py

if exist "%TARGET_FILE%" (
    echo ERROR: File %TARGET_FILE% already exists!
    exit /b 1
)

echo Creating new script: %TARGET_FILE%
copy tests\template_test.py "%TARGET_FILE%" >nul

echo Success! Created %TARGET_FILE%
echo Edit the file to implement your script.
echo Don't forget to update the docstring!
