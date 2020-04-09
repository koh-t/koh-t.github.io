
import os
import re
import glob
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from matplotlib import pylab as plt
from matplotlib import rcParams
rcParams['font.family'] = 'Hiragino Sans'

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

    plt.close()
    pdf.plot(x='log10_cumsum', y='log10_rolling', grid=True)
    plt.title(idx)
    plt.xlabel('総症例数 (対数)')
    plt.ylabel('前週の新規症例数 (対数)')
    # plt.show()
    plt.savefig(savedir + idx + '.png')

def create_csv(df,savedir):
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

def dfi2newlines(dfi, rgba, idx, type = 'trend'):
    rgba[3] = rgba[3] * 0.2
    rgba2 = rgba.copy()
    rgba2[3] = rgba2[3] * 0.1
    rgba = tuple((rgba * 256).astype(int).tolist())
    rgba2 = tuple((rgba2 * 256).astype(int).tolist())

    data = ''
    for (j, (index, row)) in enumerate(dfi.iterrows()):
        if type == 'trend':
            x = np.round(row.log10_cumsum, 3)
        elif type == 'day':
            x = j
        y = np.round(row.log10_rolling, 3)
        data = data + '{x:' + str(x) + ', y:' + str(y) + '}, '
    data = data[:-2]

    newlines = []
    newlines.append('        {\n')
    newlines.append('            label: \'' + idx + '\' ,\n')
    newlines.append('            borderColor: \'RGBA' + str(rgba) + '\', \n')
    newlines.append('            backgroundColor: \'RGBA' + str(rgba2) + '\', \n')
    newlines.append('            data: [' + data + '],\n')
    newlines.append('            fill: false, \n')
    newlines.append('            showLine: true, \n')
    newlines.append('        },\n')
    return newlines

def generate_scatter(prefs_count, savedir):
    template = './scatter_template.html'
    with open(template) as f:
        html = f.readlines()

    # insert days
    l = [i for i, line in enumerate(html) if '新型コロナウイルス(COVID-19)の感染者数' in line][0]
    today = savedir.split('-')
    today = today[2] + '年' + today[3] + '月' + today[4][:-1] + '日'
    html[l] = html[l][:-6] + today + html[l][-6:]

    # insert data
    l = [i for i, line in enumerate(html) if 'datasets' in line][0]
    for (i, idx) in enumerate(prefs_count.index):
        fname = savedir + idx + '.csv'
        dfi = pd.read_csv(fname)
        rgba = np.array(plt.cm.tab10(i))
        newlines = dfi2newlines(dfi, rgba, idx)
        for (i, newline) in enumerate(newlines):
            html.insert(l + i + 1, newline)
        l += len(newlines)
    html.insert(l + 1, '      ]\n')

    savename = 'index.html'
    with open(savename, 'w') as f:
        f.writelines(html)

    savename = savedir + '/scatter.html'
    with open(savename, 'w') as f:
        f.writelines(html)

def generate_scatter_day(prefs_count, savedir, thresh = 1-):
    template = './scatter_day_template.html'
    with open(template) as f:
        html = f.readlines()

    # insert days
    l = [i for i, line in enumerate(html) if '新型コロナウイルス(COVID-19)の感染者数' in line][0]
    today = savedir.split('-')
    today = today[2] + '年' + today[3] + '月' + today[4][:-1] + '日'
    html[l] = html[l][:-6] + today + html[l][-6:]

    # insert data
    l = [i for i, line in enumerate(html) if 'datasets' in line][0]
    for (i, idx) in enumerate(prefs_count.index):
        fname = savedir + idx + '.csv'
        dfi = pd.read_csv(fname)
        dfi = dfi[dfi['cumsum'] > thresh]
        rgba = np.array(plt.cm.tab10(i))
        newlines = dfi2newlines(dfi, rgba, idx, 'day')
        for (i, newline) in enumerate(newlines):
            html.insert(l + i + 1, newline)
        l += len(newlines)

    html.insert(l + 1, '      ]\n')

    savename = savedir + '/scatter_day.html'
    with open(savename, 'w') as f:
        f.writelines(html)

    savename = './scatter_day.html'
    with open(savename, 'w') as f:
        f.writelines(html)

if __name__ == '__main__':
    get_jag()
    df, savedir = load_data()
    if not os.path.exists(savedir):
        create_csv(df, savedir)

    prefs_count = df['居住都道府県'].value_counts()
    prefs_count = prefs_count.drop('不明')
    prefs_count = prefs_count[prefs_count > 100]
    # prefs_count = prefs_count[['東京都', '大阪府', '京都府']]

    generate_scatter(prefs_count, savedir)
    generate_scatte_dayr(prefs_count, savedir)

    print(0)



    print(0)