#!/usr/bin/python

import csv
import sys
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('year')
args = parser.parse_args()


def printf(format, *values):
    print(format % values)


ignore_votes_for = ['UNDERVOTES', 'BLANK VOTE', 'BLANK VOTE/SCATTERING',
                    'BLANK VOTE/VOID VOTE/SCATTERING', 'OTHER', 'WRITEIN']

party_votes = {}
party_count = {}
total_reps = 0
total_votes = 0
with open(str(Path.home()) + '/Downloads/1976-2020-house.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['year'] != args.year:
            continue
        if row['candidate'] in ignore_votes_for:
            continue
        frac = 1.0 if (row['candidatevotes'] == row['totalvotes']) else int(
            row['candidatevotes']) / int(row['totalvotes'])
        if frac < 0.01:
            continue
        if row['party'] == '':
            row['party'] = 'NO PARTY AFFILIATION'
        printf('%s district %s; %s (%s) with %5.2f%%',
               row['state'], row['district'], row['candidate'], row['party'], 100.0 * frac)
        if row['party'] in party_votes:
            party_votes[row['party']] += frac
        else:
            party_votes[row['party']] = frac
        if row['party'] in party_count:
            party_count[row['party']] += 1
        else:
            party_count[row['party']] = 1
        total_reps += 1
        total_votes += frac

printf('Party results for %s:', args.year)
for party in sorted(party_votes, key=party_votes.get, reverse=True):
    printf('%-30s: %3d reps with %6.2f votes', party,
           party_count[party], party_votes[party])

printf('\nGRAND TOTAL: %d reps with %0.2f votes', total_reps, total_votes)
