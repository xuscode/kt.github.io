@echo off
@REM set date=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%

cd /d %~dp0
rem git pull
rem git status
rem git config --global --add safe.directory E:/200-CODE/Dassault_Systemes/3DEXPERIENCE_Automation
rem git remote add origin git@gitee.com:xuscode/all_catia_code.git
rem git add B27 B421 B422 B423
rem git rm --cached -r 3DEXPERIENCE_Release B27

rem git add *.md *.vb *.cs *.catvba *.CATScript *.bas  *.py *.cpp *.h *.DSGen *.tsrc *.osm   *.CATNls *.CATRsc *.mk *.ico *.rc *.afr *.xml *.cmd *.bat *.png *.bmp *.ico

git pull
git add .

@echo WRITE UPDATE AND PRESS ENTER:
::set /p GetYourLog=
rem git commit -m "%date%"
git commit -m "%date%  %time%"
git push -u origin main
timeout /t 20

@REM cd /d .\files\BDG_CASE_WUHAN_CENTER
@REM git rm --cached . -rf
@REM git add .


