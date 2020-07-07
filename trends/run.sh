#!/bin/bash
cd /Users/koh/Dropbox/Proj-web/koh-t.github.io/trends
/Users/koh/anaconda3/envs/pt_env/bin/python main.py
git add .
git commit -m "web update"
git config core.sshCommand "ssh -i ~/.ssh/github git push origin master"
git push origin master
exit 0
