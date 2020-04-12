import os
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


def _create_csv(pdf, idx, savedir):
    pdf = pd.to_datetime(pdf['確定日YYYYMMDD'])
    pdf = pdf.value_counts().sort_index()

    pdf_perweek = pdf.rolling('7d', min_periods=1).mean()
    pdf_cumsum = pdf.cumsum()
    pdf = pd.concat([pdf_cumsum, pdf_cumsum, pdf_perweek, pdf_perweek], axis=1)
    pdf.columns = ['cumsum', 'log10_cumsum', 'rolling', 'log10_rolling']

    pdf['log10_cumsum'] = np.round(np.log10(pdf['log10_cumsum']), 3)
    pdf['log10_rolling'] = np.round(np.log10(pdf['log10_rolling']), 3)

    pdf.to_csv(savedir + idx + '.csv')  # , header=False)

    # plt.close()
    # pdf.plot(x='log10_cumsum', y='log10_rolling', grid=True)
    # plt.title(idx)
    # plt.xlabel('総症例数 (対数)')
    # plt.ylabel('前週の新規症例数 (対数)')
    # plt.show()
    # plt.savefig(savedir + idx + '.png')


def create_csv(df, savedir):
    prefs_count = df['居住都道府県'].value_counts()
    for idx in prefs_count.index:
        pdf = df[df['居住都道府県'] == idx]
        _create_csv(pdf, idx, savedir)

    jdf = df[df.居住都道府県コード.notnull()]
    _create_csv(jdf, '全国', savedir)


def check_signate():
    loaddir = 'csv/signate_2020-04-07-063646/'
    fname = loaddir + '罹患者.csv'
    df = pd.read_csv(fname, error_bad_lines=False)

    df = df[['受診都道府県', '公表日']]
    df.columns = ['pref', 'day']
    df = df.dropna()

    cpref = df.pref.value_counts()
    print(cpref)
