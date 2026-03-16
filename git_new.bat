CD /D %~dp0
dir

echo "# kt.github.io" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/xuscode/kt.github.io.git
git push -u origin main

pause