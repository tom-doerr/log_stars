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


    datapoints_last_hour = df[df['Time'] > datetime. now() - pd.Timedelta('1h')]
    datapoints_last_hour_oldest = datapoints_last_hour['Time'].min()
    # Get star value for the oldest datapoint.
    datapoints_last_hour_oldest_value = datapoints_last_hour[
        datapoints_last_hour['Time'] == datapoints_last_hour_oldest]['Stars'].iloc[0]

    datapoints_last_hour_newest = datapoints_last_hour['Time'].max()
    # Get star value for the newest datapoint.
    datapoints_last_hour_newest_value = datapoints_last_hour[
        datapoints_last_hour['Time'] == datapoints_last_hour_newest]['Stars'].iloc[0]

    num_stars_last_hour = datapoints_last_hour_newest_value - \
        datapoints_last_hour_oldest_value


    datapoints_last_5_hours_per_hour_oldest = df[df['Time'] > datetime. now() - pd.Timedelta('5h')]
    datapoints_last_5_hours_per_hour_oldest_oldest = datapoints_last_5_hours_per_hour_oldest['Time'].min()
    # Get star value for the oldest datapoint.
    datapoints_last_5_hours_per_hour_oldest_oldest_value = datapoints_last_5_hours_per_hour_oldest[
        datapoints_last_5_hours_per_hour_oldest['Time'] == datapoints_last_5_hours_per_hour_oldest_oldest]['Stars'].iloc[0]

    datapoints_last_5_hours_per_hour_oldest_newest = datapoints_last_5_hours_per_hour_oldest['Time'].max()
    # Get star value for the newest datapoint.
    datapoints_last_5_hours_per_hour_oldest_newest_value = datapoints_last_5_hours_per_hour_oldest[
        datapoints_last_5_hours_per_hour_oldest['Time'] == datapoints_last_5_hours_per_hour_oldest_newest]['Stars'].iloc[0]

    num_stars_last_5_hours_per_hour = (datapoints_last_5_hours_per_hour_oldest_newest_value - \
        datapoints_last_5_hours_per_hour_oldest_oldest_value) / 5

    # Print them in one line.
    print()
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

