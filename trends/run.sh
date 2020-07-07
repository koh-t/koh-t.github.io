#!/bin/bash
export GIT_COMMITTER_NAME="koh-t"
export GIT_COMMITTER_EMAIL="koh0927@gmail.com"
export GIT_AUTHOR_NAME="koh-t"
export GIT_AUTHOR_EMAIL="koh0927@gmail.com"
cd /Users/koh/Dropbox/Proj-web/koh-t.github.io/trends
/Users/koh/anaconda3/envs/pt_env/bin/python main.py
git add .
git commit -m "web update"
git push origin master
exit 0
