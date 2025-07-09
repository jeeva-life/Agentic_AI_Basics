python -m ensurepip --upgrade
python -m pip --version

Downloaded bfg-1.14.0.jar and ran the following 3 commands below:
java -jar bfg-1.14.0.jar --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive