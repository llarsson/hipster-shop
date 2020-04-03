#!/bin/bash

set -euo pipefail

KUBE_PROMETHEUS_DIR=../../kube-prometheus/

if ! minikube status | grep 'host: Running' > /dev/null; then
    echo "minikube does not seem to be running"
    # 10 GiB RAM, 4 CPU cores, and 32 GiB disk for Kubernetes 1.18.0
    minikube start --cpus=4 --memory 10240 --disk-size 32768 --driver virtualbox --kubernetes-version='v1.18.0'
fi

if ! kubectl --context minikube describe namespace monitoring &> /dev/null; then
    echo "Prometheus does not seem to be installed"
    pushd ${KUBE_PROMETHEUS_DIR}
    kubectl --context minikube apply -f manifests/setup
    sleep 30
    kubectl --context minikube apply -f manifests
fi

while kubectl --context minikube get pods --namespace monitoring --no-headers | grep -v 'Running'; do
    echo "Prometheus not correctly set up just yet, waiting..."
    sleep 2
done
