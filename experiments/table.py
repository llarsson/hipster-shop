#!/usr/bin/env python3

import pandas as pd
import sys
import glob

from parse import parse_directory

algos = ['static-0', 'dynamic-adaptive-0.1', 'dynamic-updaterisk-0.1']

header_aliases = {
        'cached_requests' : 'Cached requests',
        'upstream_requests' : 'Upstream requests',
        'cache_fraction': 'Cached request fraction',
        'total_requests' : 'Total requests',
        'received_bytes': 'Received bytes',
        'transmitted_bytes': 'Sent bytes',
        'total_bytes' : 'Total bytes',
        'reduction': 'Reduction',
}

def parse_requests(results_directory):
    results = pd.DataFrame(index=algos, columns=['total_requests', 'cached_requests', 'upstream_requests', 'cache_fraction'])

    for algo in algos:
        sources = []
        cached = 0
        upstream = 0

        for source in glob.glob('{}/*{}*-caching.csv'.format(results_directory, algo)):
            df = pd.read_csv(source)
            cached += df.query('source == "cache"').shape[0]
            upstream += df.query('source == "upstream"').shape[0]

        results['cached_requests'][algo] = cached
        results['upstream_requests'][algo] = upstream
        results['total_requests'][algo] = cached + upstream
        results['cache_fraction'][algo] = cached / (cached + upstream)
    
    return results.astype({'cached_requests': 'int64', 'upstream_requests': 'int64', 'cache_fraction': 'float64', 'total_requests': 'int64'})


def make_table(received_bytes, transmitted_bytes, requests):
    table = pd.DataFrame(index=algos)

    recv_sums = received_bytes.sum(axis=0)
    table['received_bytes'] = [ recv_sums['{}_received_bytes'.format(algo)] for algo in algos ]

    xmit_sums = transmitted_bytes.sum(axis=0)
    table['transmitted_bytes'] = [ xmit_sums['{}_transmitted_bytes'.format(algo)] for algo in algos ]

    table['total_bytes'] = table['received_bytes'] + table['transmitted_bytes']

    table = table.astype('int64')

    table['reduction'] = (1 - table['total_bytes'] / table['total_bytes']['static-0'])

    table = pd.concat([table, requests], axis=1)

    return table


if __name__=="__main__":
    sources = []
    for results_directory in sys.argv[1:]:
        (received_bytes, transmitted_bytes) = parse_directory(results_directory)
        requests = parse_requests(results_directory)
        table = make_table(received_bytes, transmitted_bytes, requests)
        sources.append(table)

    table = pd.concat(sources)
    table = table.groupby(table.index).mean()

    print(table)

    with open('hipsterShopCachedRequests.tex', 'w') as f:
        desired_columns=['total_requests', 'cached_requests', 'upstream_requests', 'cache_fraction']
        f.write(table.to_latex(columns=desired_columns, header=[header_aliases[header] for header in desired_columns], float_format="%.2f", escape=False, bold_rows=True,
        caption="Caching of requests in Hipster Shop, as reported by caches installed in components that communicate with others. Note that the number of requests includes both those that could be cached and those that cannot, see Section~\\ref{secHipsterShopCacheability}.", label='tabHipsterShopCachedRequests'))

    with open('hipsterShopNetworkTraffic.tex', 'w') as f:
        desired_columns=['total_bytes', 'received_bytes', 'transmitted_bytes', 'reduction']
        f.write(table.to_latex(columns=desired_columns, header=[header_aliases[header] for header in desired_columns], float_format="%.2f", escape=False, bold_rows=True,
        caption="Inter-Pod network traffic in Hipster Shop. Note that traffic within individual Pods does not count toward these numbers, only traffic between Pods.", label='tabHipsterShopNetworkTraffic'))


