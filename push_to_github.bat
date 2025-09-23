@echo off
echo ========================================
echo    Baseball Sim - Push to GitHub
echo ========================================
echo.

echo Checking for changes...
git status

echo.
echo Staging all changes...
git add .

echo.
echo Committing changes...
set /p commit_msg="Enter commit message (or press Enter for 'Updated code'): "
if "%commit_msg%"=="" set commit_msg=Updated code

git commit -m "%commit_msg%"

echo.
echo Pushing to GitHub...
git push

echo.
echo ========================================
echo    Push Complete!
echo ========================================
echo.
echo Your changes have been pushed to:
echo https://github.com/rickpersak/baseball-simulation-game
echo.
pause
