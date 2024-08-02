:: Getting Batch File Location Directory - Relative Path
set script_dir=%~dp0

:: Changing to Python Script Directory
cd /d %script_dir%

@echo off
:: This batch file runs the following packages:
:: getlinks.py, updatelinks.py -> Pulls data from links indicated in worksheet cells and updates it into the corresponding cells
:: **IMPORTANT** Ensure that the four following files are in the same folder as the updatelinks.bat file: env.py, getlinks.py, updatelinks.py, credentials.json

python updatelinks.py
@echo Running updatelinks.py

@echo The programme has finished running. You can close this window.
pause