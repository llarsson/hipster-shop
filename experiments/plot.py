#!/usr/bin/env python3

import glob
import pandas as pd
import matplotlib.pyplot as plt
import sys

from matplotlib.backends.backend_pdf import PdfPages

from parse import parse_directory


def plot_network_traffic(received_bytes, transmitted_bytes):
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True, constrained_layout=True)

    fig.suptitle('Network traffic (bytes/sec)\n\n')

    static_ax = ax[0]
    static_ax.plot(transmitted_bytes['relative_timestamp'], transmitted_bytes['static-0_transmitted_bytes'], color='black')

    adaptive_ax = ax[1]
    adaptive_ax.plot(transmitted_bytes['relative_timestamp'], transmitted_bytes['dynamic-adaptive-0.1_transmitted_bytes'], color='black')

    updaterisk_ax = ax[2]
    updaterisk_ax.plot(transmitted_bytes['relative_timestamp'], transmitted_bytes['dynamic-updaterisk-0.1_transmitted_bytes'], color='black')

    static_ax.plot(received_bytes['relative_timestamp'], -received_bytes['static-0_received_bytes'], color='black')
    adaptive_ax.plot(received_bytes['relative_timestamp'], -received_bytes['dynamic-adaptive-0.1_received_bytes'], color='black')
    updaterisk_ax.plot(received_bytes['relative_timestamp'], -received_bytes['dynamic-updaterisk-0.1_received_bytes'], color='black')

    static_ax.fill_between(received_bytes['relative_timestamp'], -received_bytes['static-0_received_bytes'], transmitted_bytes['static-0_transmitted_bytes'], facecolor='white', edgecolor='black', hatch='||', label='Static TTL (0)')
    adaptive_ax.fill_between(received_bytes['relative_timestamp'], -received_bytes['dynamic-adaptive-0.1_received_bytes'], transmitted_bytes['dynamic-adaptive-0.1_transmitted_bytes'], facecolor='white', hatch='//', edgecolor='black', label='Adaptive TTL (0.1)')
    updaterisk_ax.fill_between(received_bytes['relative_timestamp'], -received_bytes['dynamic-updaterisk-0.1_received_bytes'], transmitted_bytes['dynamic-updaterisk-0.1_transmitted_bytes'], facecolor='white', edgecolor='black', hatch='\\\\', label='Update-risk based (0.1)')

    fig.legend(ncol=3, bbox_to_anchor=(0.98, 0.95), frameon=False)

    plt.show()

    fig.savefig('hipsterShopNetworkTraffic.pdf', bbox_inches='tight')



if __name__=="__main__":
    recv_sources = []
    xmit_sources = []
    for results_directory in sys.argv[1:]:
        (received_bytes, transmitted_bytes) = parse_directory(results_directory)
        received_bytes['relative_timestamp'] = received_bytes.index
        transmitted_bytes['relative_timestamp'] = transmitted_bytes.index
        received_bytes.index = pd.to_datetime(received_bytes.index, unit='s')
        transmitted_bytes.index = pd.to_datetime(transmitted_bytes.index, unit='s')
        recv_sources.append(received_bytes)
        xmit_sources.append(transmitted_bytes)

    received_bytes = pd.concat(recv_sources)
    received_bytes = received_bytes.groupby(received_bytes.index).mean()

    transmitted_bytes = pd.concat(xmit_sources)
    transmitted_bytes = transmitted_bytes.groupby(transmitted_bytes.index).mean()

    print(received_bytes)

    plot_network_traffic(received_bytes, transmitted_bytes)
