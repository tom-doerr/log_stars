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
import argparse

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
    args = get_args()
    df = pd.read_csv(data)
    # Filter the df so only data after start is included.
    df = df[df['Time'] > args.start]

    df['Time'] = pd.to_datetime(df['Time'])

    num_stars_last_hour = get_num_stars_last_x_hours(1)
    num_stars_last_5_hours_per_hour = get_num_stars_last_x_hours(5)
    num_stars_last_24h = get_num_stars_last_x_hours(24) * 24
    current_num_stars = df['Stars'].iloc[-1]

    print()
    # print all with the number at the beginning and the label at the end.
    print(f"{num_stars_last_hour:.1f} stars/hour")
    print(f"{num_stars_last_5_hours_per_hour:.1f} stars/hour over five hours")
    print(f"{num_stars_last_24h:.0f} stars over 24 hours")
    print(f"{current_num_stars:.0f} stars now")


    plt.plot(df['Time'], df['Stars'], '-o')

    plt.xlabel('Time')
    plt.ylabel('Stars')
    plt.title('Stars over Time')

    # Rotate the x labels.
    plt.xticks(rotation=45)

    # Draw vertical lines whenever a new day starts.
    plt.axvline(x=df['Time'].iloc[0], linestyle='--', color='#000000')
    for i in range(1, len(df['Time'])):
        if df['Time'].iloc[i].day != df['Time'].iloc[i - 1].day:
            plt.axvline(x=df['Time'].iloc[i], linestyle='--', color='#000000')

    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def get_args():
    parser = argparse.ArgumentParser()
    # Get the start date from which to plot.
    parser.add_argument("-s", "--start", help="Start date to plot from.")

    return parser.parse_args()

if __name__ == '__main__':
    plot_stars('stars.csv', 'stars.png')

