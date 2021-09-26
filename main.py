#!/usr/bin/env python3

'''
This script checks the number of stars of a github repo
in a certain interval and saves the data as a csv file.
'''

import argparse
from datetime import datetime
import os
import sys
import time

import requests

CSV_FILENAME = 'stars.csv'

def get_stars(repo, auth=None):
    '''
    Returns the number of stars of a github repo
    '''
    url = 'https://api.github.com/repos/' + repo
    resp = requests.get(url, auth=auth)
    if resp.status_code != 200:
        print('ERROR: Could not get stars for ' + repo)
        return 0
    return int(resp.json()['stargazers_count'])

def get_repos(file):
    '''
    Returns the repos listed in the input file
    '''
    with open(file) as f:
        reader = csv.reader(f)
        next(reader)
        repos = [row[1] for row in reader]
    return repos

def write_csv(repos, interval):
    '''
    Writes the number of stars for each repository
    to a csv file
    '''
    file_exists = os.path.isfile(CSV_FILENAME)
    while True:
        with open(CSV_FILENAME, 'a') as f:
            if not file_exists:
                f.write('Time,Repo,Stars\n')
            for repo in repos:
                stars = get_stars(repo)
                f.write('{},{},{}\n'.format(datetime.now(), repo, stars))

        time.sleep(interval)

def main():
    '''
    Main function
    '''
    parser = argparse.ArgumentParser()
    # Repo name, username and password are optional
    parser.add_argument('-r', '--repo', help='Repository name')
    parser.add_argument('-i', '--interval', help='Interval in seconds', default=60)
    args = parser.parse_args()


    repos = [args.repo]

    write_csv(repos, int(args.interval))


if __name__ == '__main__':
    main()

