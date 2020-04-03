#!/bin/bash

set -euo pipefail

duration=1800

if [ ! -d results ]; then
    mkdir -p results
fi

# TODO only run if git repo is up to date

kubectl delete -f ../release/kubernetes-manifests.yaml &> /dev/null || true
kubectl delete -f ../release/loadgenerator.yaml &> /dev/null || true

for experiment in static-0 dynamic-adaptive-0.1 dynamic-updaterisk-0.1; do
    echo "Will run experiment for ${experiment}"

    echo "Deploying Hipster Store"
    kubectl apply -f ../release/kubernetes-manifests-${experiment}.yaml

    while kubectl get pods --no-headers | grep -v 'Running'; do
        echo 'Not everything is Running yet'
        sleep 2
    done

    start=$(TZ=GMT date +"%Y%m%d%H%M%S")
    echo "Starting experiment at ${start} in UTC epoch time"

    echo "Sleeping a minute to not miss load ramp-up period..."
    sleep 60

    echo "Deploying load generator"
    kubectl apply -f ../release/loadgenerator.yaml

    echo "Sleeping for ${duration} seconds"
    sleep ${duration}

    echo "Removing load generator"
    kubectl delete -f ../release/loadgenerator.yaml
    kubectl wait -f ../release/loadgenerator.yaml --for=delete

    echo "Sleeping for an additional minute to not miss ramp-down period..."
    sleep 60

    end=$(TZ=GMT date +"%Y%m%d%H%M%S")
    echo "Experiment ended at ${end} in UTC epoch time"

    echo "Storing cache CSV files for the components with caching enabled"
    for component in frontend recommendation checkout; do
        kubectl exec $(kubectl get pods | grep ${component} | cut -d ' ' -f 1) -c caching-grpc-reverse-proxy cat data.csv > results/${experiment}-${component}-caching.csv
    done

    echo "Removing Hipster Shop"
    kubectl delete -f ../release/kubernetes-manifests-${experiment}.yaml
    kubectl wait -f ../release/kubernetes-manifests-${experiment}.yaml --for=delete

    echo "Storing time series data in files"
    ./query_csv.py http://localhost:9090 ${experiment}_received_bytes \
        'sum(irate(container_network_receive_bytes_total{namespace="default"}[1m]))' \
        ${start} ${end} '15s' > results/received_bytes_${experiment}.csv

    ./query_csv.py http://localhost:9090 ${experiment}_transmitted_bytes \
        'sum(irate(container_network_transmit_bytes_total{namespace="default"}[1m]))' \
        ${start} ${end} '15s' > results/transmitted_bytes_${experiment}.csv

    echo "Sleeping 2 minutes before moving on..."
    sleep 120
done
