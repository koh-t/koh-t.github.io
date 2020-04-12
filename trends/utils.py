
import re
import glob
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

def get_jag():
    timenow = datetime.today().strftime('%Y-%m-%d')
    fname = './csv/COVID-19-' + timenow + '.csv'
    if not os.path.exists(fname):
        df = pd.read_csv('https://dl.dropboxusercontent.com/s/6mztoeb6xf78g5w/COVID-19.csv')
        df.to_csv(fname)


def load_data():
    files = glob.glob('./csv/*.csv')
    files.sort()
    file = files[-1]
    savedir = file[:-4] + '/'
    with Path(savedir) as f:
        if not f.exists():
            os.mkdir(f)

    df = pd.read_csv(file)
    return df, savedir