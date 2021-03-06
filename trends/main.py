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
from plot import generate_scatter_pref, generate_scatter_day_pref
from utils import get_jag, load_data, create_csv, dfi2newlines


def generate_scatter(prefs_count, savedir):
    template = './scatter_template.html'
    with open(template) as f:
        html = f.readlines()

    # insert days
    l = [i for i, line in enumerate(html) if '新型コロナウイルス(COVID-19)の感染者数' in line][0]
    today = savedir.split('-')
    today = today[2] + '年' + today[3] + '月' + today[4][:-1] + '日'
    html[l] = html[l][:-6] + today + html[l][-6:]

    # insert pref
    l = [i for i, line in enumerate(html) if 'scatter_++.html' in line][0]
    template = html[l].split('++')
    html.pop(l)
    for (i, pref) in enumerate(prefs_count.index):
        if i < len(prefs_count) - 1:
            newline = template[0] + pref + template[1] + pref + template[2]
        else:
            newline = template[0] + pref + template[1] + pref + template[2][:-2] + '\n'
        html.insert(l + i, newline)

    # insert pref day
    l = [i for i, line in enumerate(html) if 'scatter_day_++.html' in line][0]
    template = html[l].split('++')
    html.pop(l)
    for (i, pref) in enumerate(prefs_count.index):
        if i < len(prefs_count) - 1:
            newline = template[0] + pref + template[1] + pref + template[2]
        else:
            newline = template[0] + pref + template[1] + pref + template[2][:-2] + '\n'
        html.insert(l + i, newline)

    # insert data
    l = [i for i, line in enumerate(html) if 'datasets' in line][0]
    for (i, idx) in enumerate(prefs_count.index):
        fname = savedir + idx + '.csv'
        dfi = pd.read_csv(fname)
        rgba = np.array(plt.cm.tab20(i))
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


def generate_scatter_day(prefs_count, savedir, thresh=10):
    template = './scatter_day_template.html'
    with open(template) as f:
        html = f.readlines()

    # insert days
    l = [i for i, line in enumerate(html) if '新型コロナウイルス(COVID-19)の感染者数' in line][0]
    today = savedir.split('-')
    today = today[2] + '年' + today[3] + '月' + today[4][:-1] + '日'
    html[l] = html[l][:-6] + today + html[l][-6:]

    # insert pref
    l = [i for i, line in enumerate(html) if 'scatter_++.html' in line][0]
    template = html[l].split('++')
    html.pop(l)
    for (i, pref) in enumerate(prefs_count.index):
        if i < len(prefs_count) - 1:
            newline = template[0] + pref + template[1] + pref + template[2]
        else:
            newline = template[0] + pref + template[1] + pref + template[2][:-2] + '\n'
        html.insert(l + i, newline)

    # insert pref day
    l = [i for i, line in enumerate(html) if 'scatter_day_++.html' in line][0]
    template = html[l].split('++')
    html.pop(l)
    for (i, pref) in enumerate(prefs_count.index):
        if i < len(prefs_count) - 1:
            newline = template[0] + pref + template[1] + pref + template[2]
        else:
            newline = template[0] + pref + template[1] + pref + template[2][:-2] + '\n'
        html.insert(l + i, newline)

    # insert data
    l = [i for i, line in enumerate(html) if 'datasets' in line][0]
    for (i, idx) in enumerate(prefs_count.index):
        fname = savedir + idx + '.csv'
        dfi = pd.read_csv(fname)
        dfi = dfi[dfi['cumsum'] > thresh]
        rgba = np.array(plt.cm.tab20(i))
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
    create_csv(df, savedir)

    prefs_count = df['居住都道府県'].value_counts()
    prefs_count = prefs_count.drop('不明')
    prefs_count = prefs_count[prefs_count > 100]
    # prefs_count = prefs_count[['東京都', '大阪府', '京都府']]

    generate_scatter(prefs_count, savedir)
    generate_scatter_day(prefs_count, savedir, 10)

    for i in range(len(prefs_count)):
        generate_scatter_pref(prefs_count, savedir, i)
        generate_scatter_day_pref(prefs_count, savedir, i)

    print(0)
