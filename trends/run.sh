!#!/bin/bash
echo "update covid trends!"
cd /Users/koh/Dropbox/Proj-web/koh-t.github.io/trends
source activate pt_env
python main.py
conda deactivate pt_env

git add .
git commit -m "web update"
git push origin master

exit 0
