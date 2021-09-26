#!/usr/bin/env python3

'''
This plots the data from the file stars.csv using visdom.

stars.csv:
Time,Repo,Stars
2021-09-27 01:30:41.780979,tom-doerr/zsh_codex,156
'''
import matplotlib
matplotlib.use("Qt5agg")

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


def plot_stars(data, filename=None):
    '''
    Plots the data from the file stars.csv using matplotlib.

    stars.csv:
    Time,Repo,Stars
    2021-09-27 01:30:41.780979,tom-doerr/zsh_codex,156
    '''
    df = pd.read_csv(data)

    df['Time'] = pd.to_datetime(df['Time'])

    plt.plot(df['Time'], df['Stars'], '-o')

    plt.xlabel('Time')
    plt.ylabel('Stars')
    plt.title('Stars over Time')

    if filename:
        plt.savefig(filename)
    else:
        plt.show()


if __name__ == '__main__':
    plot_stars('stars.csv', 'stars.png')

