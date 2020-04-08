#!/usr/bin/env python3

import glob
import pandas as pd

def normalize_timestamps(df):
    df['timestamp'] = df['timestamp'] - df['timestamp'][0]
    return df

def parse_directory(results_directory):
    received_bytes_sources = []
    for source in glob.glob('{}/received_bytes_*.csv'.format(results_directory)):
        df = normalize_timestamps(pd.read_csv(source)).set_index('timestamp')
        received_bytes_sources.append(df)

    received_bytes = pd.concat(received_bytes_sources, axis=1)

    transmitted_bytes_sources = []
    for source in glob.glob('{}/transmitted_bytes_*.csv'.format(results_directory)):
        df = normalize_timestamps(pd.read_csv(source)).set_index('timestamp')
        transmitted_bytes_sources.append(df)

    transmitted_bytes = pd.concat(transmitted_bytes_sources, axis=1)

    return (received_bytes, transmitted_bytes)
