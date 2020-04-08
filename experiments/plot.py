#!/usr/bin/env python3

import glob
import pandas as pd
import matplotlib.pyplot as plt
import sys

from parse import parse_directory


def plot_network_traffic(received_bytes, transmitted_bytes):
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)

    fig.suptitle('Network traffic (bytes/sec)')

    static_ax = ax[0]
    static_ax.plot(transmitted_bytes.index, transmitted_bytes['static-0_transmitted_bytes'], color='black', label='Static TTL (0)')

    adaptive_ax = ax[1]
    adaptive_ax.plot(transmitted_bytes.index, transmitted_bytes['dynamic-adaptive-0.1_transmitted_bytes'], color='blue', label='Adaptive TTL (0.1)')

    updaterisk_ax = ax[2]
    updaterisk_ax.plot(transmitted_bytes.index, transmitted_bytes['dynamic-updaterisk-0.1_transmitted_bytes'], color='orange', label='Update-risk based (0.1)')

    fig.legend()

    static_ax.plot(received_bytes.index, -received_bytes['static-0_received_bytes'], color='black', label='Static TTL (0)')
    adaptive_ax.plot(received_bytes.index, -received_bytes['dynamic-adaptive-0.1_received_bytes'], color='blue', label='Adaptive TTL (0.1)')
    updaterisk_ax.plot(received_bytes.index, -received_bytes['dynamic-updaterisk-0.1_received_bytes'], color='orange', label='Update-risk based (0.1)')
    plt.show()


if __name__=="__main__":
    results_directory = sys.argv[1]
    (received_bytes, transmitted_bytes) = parse_directory(results_directory)
    plot_network_traffic(received_bytes, transmitted_bytes)
