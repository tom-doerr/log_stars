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

def get_num_stars_last_x_hours(hours):
    df = pd.read_csv('stars.csv')

    df['Time'] = pd.to_datetime(df['Time'])
    hours_str = str(hours)

    datapoints_last_x_hours = df[df['Time'] > datetime. now() - pd.Timedelta(hours_str + 'h')]
    datapoints_last_x_hours_oldest = datapoints_last_x_hours['Time'].min()
    # Get star value for the oldest datapoint.
    datapoints_last_x_hours_oldest_value = datapoints_last_x_hours[
        datapoints_last_x_hours['Time'] == datapoints_last_x_hours_oldest]['Stars'].iloc[0]

    datapoints_last_x_hours_newest = datapoints_last_x_hours['Time'].max()
    # Get star value for the newest datapoint.
    datapoints_last_x_hours_newest_value = datapoints_last_x_hours[
        datapoints_last_x_hours['Time'] == datapoints_last_x_hours_newest]['Stars'].iloc[0]

    num_stars_last_x_hours = (datapoints_last_x_hours_newest_value - \
        datapoints_last_x_hours_oldest_value) / hours

    return num_stars_last_x_hours

def plot_stars(data, filename=None):
    '''
    Plots the data from the file stars.csv using matplotlib.

    stars.csv:
    Time,Repo,Stars
    2021-09-27 01:30:41.780979,tom-doerr/zsh_codex,156
    '''
    df = pd.read_csv(data)

    df['Time'] = pd.to_datetime(df['Time'])

    num_stars_last_hour = get_num_stars_last_x_hours(1)
    num_stars_last_5_hours_per_hour = get_num_stars_last_x_hours(5)

    print(f'{num_stars_last_hour:.0f} stars in the last hour, {num_stars_last_5_hours_per_hour:.0f} stars per hour on average')



    plt.plot(df['Time'], df['Stars'], '-o')

    plt.xlabel('Time')
    plt.ylabel('Stars')
    plt.title('Stars over Time')

    # Rotate the x labels.
    plt.xticks(rotation=45)

    if filename:
        plt.savefig(filename)
    else:
        plt.show()


if __name__ == '__main__':
    plot_stars('stars.csv', 'stars.png')

