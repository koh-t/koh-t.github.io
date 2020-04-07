import os
from pathlib import Path
from datetime import datetime

timenow = datetime.today().strftime('%Y-%m-%d-%H%M%S')

def signite(timenow):
    from gsheets import Sheets
    # https://github.com/xflr6/gsheets
    sheets = Sheets.from_files('./client_secret.json', './storage.json')
    savedir = './csv/signate_' + timenow + '/'

    with Path(savedir) as f:
        if not f.exists():
            os.mkdir(f)

    url = 'https://docs.google.com/spreadsheets/d/1CnQOf6eN18Kw5Q6ScE_9tFoyddk4FBwFZqZpt_tMOm4'
    s = sheets.get(url)
    titles = s.sheets.titles()
    for (i, title) in enumerate(titles):
        fname = savedir + title + '.csv'
        s.sheets[i].to_csv(fname, encoding='utf-8', dialect='excel')

