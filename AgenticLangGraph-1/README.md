python -m ensurepip --upgrade
python -m pip --version

Downloaded bfg-1.14.0.jar and ran the following 3 commands below:
java -jar bfg-1.14.0.jar --delete-files .env
git reflog expire --expire=now --all
'''This command tells Git to immediately remove all old reflog entries for all branches, making it easier for the next git gc (garbage collection) to permanently delete unreachable objects (such as files you removed from history with BFG or filter-repo).
Why is it used after BFG/filter-repo?
To ensure that sensitive data (like secrets) you removed from history are not still accessible via the reflog, and can be fully deleted by garbage collection.'''
git gc --prune=now --aggressive