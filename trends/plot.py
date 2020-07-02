import os
import re
import glob
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from matplotlib import pylab as plt
from utils import dfi2newlines

def generate_scatter_pref(prefs_count, savedir, prefid):
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
    prefs = list(prefs_count.index)
    pref = prefs.pop(prefid)
    prefs.insert(0, pref)

    l = [i for i, line in enumerate(html) if 'datasets' in line][0]
    for (i, idx) in enumerate(prefs):
        fname = savedir + idx + '.csv'
        dfi = pd.read_csv(fname)
        if i == 0:
            rgba = np.array(plt.cm.tab20(0))
        else:
            rgba = np.array([1, 1, 1, 1]) * 0.9

        newlines = dfi2newlines(dfi, rgba, idx)
        for (i, newline) in enumerate(newlines):
            html.insert(l + i + 1, newline)
        l += len(newlines)
    html.insert(l + 1, '      ]\n')

    savename = './pref/scatter_' + pref + '.html'
    with open(savename, 'w') as f:
        f.writelines(html)

    savename = savedir + '/scatter_' + pref + '.html'
    with open(savename, 'w') as f:
        f.writelines(html)


def generate_scatter_day_pref(prefs_count, savedir, prefid, thresh=10):
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
    prefs = list(prefs_count.index)
    pref = prefs.pop(prefid)
    prefs.insert(0, pref)

    l = [i for i, line in enumerate(html) if 'datasets' in line][0]
    for (i, idx) in enumerate(prefs):
        fname = savedir + idx + '.csv'
        dfi = pd.read_csv(fname)
        # dfi = dfi[dfi['cumsum'] > thresh]
        if i == 0:
            rgba = np.array(plt.cm.tab20(0))
        else:
            rgba = np.array([1, 1, 1, 1]) * 0.9
        newlines = dfi2newlines(dfi, rgba, idx, 'day')
        for (i, newline) in enumerate(newlines):
            html.insert(l + i + 1, newline)
        l += len(newlines)

    html.insert(l + 1, '      ]\n')

    savename = './pref/scatter_day_' + pref + '.html'
    with open(savename, 'w') as f:
        f.writelines(html)

    savename = savedir + '/scatter_day_' + pref + '.html'
    with open(savename, 'w') as f:
        f.writelines(html)

