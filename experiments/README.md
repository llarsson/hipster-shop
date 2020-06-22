# Experiments

## Cluster setup

We create a minikube cluster for these experiments. It consumes 4 CPU cores, 10GiB of RAM, and 32GiB of disk.

The kube-prometheus distribution is used to set up Prometheus. Clone it into a directory (suggested: as a sibling of where ever you cloned this repo).

Assuming you do not already have a minikube cluster of at least the size stated above, simply do:

```
cd experiments/
./cluster.sh
```

That should set everything up for you.

## Port forwarding

You will likely want to set up port forwarding for both Grafana and the Prometheus services:

```
kubectl --context minikube --namespace monitoring port-forward svc/prometheus-k8s 9090
kubectl --context minikube --namespace monitoring port-forward svc/grafana 3000
```

You can now reach the services via their ports on `localhost`. The default credentials for Grafana, changed upon first login, are `admin/admin`.

If your minikube-running computer is not your main workstation, you can use SSH port forwarding as well to get local machine access to it:

`ssh -L 3000:localhost:3000 computer-that-runs-minikube`

Now your main computer (laptop?) can access Grafana on its http://localhost:3000/

Do the same for Prometheus if desired.

## Running experiments

If everything's set up and your `kubectl` default context is that of the minikube, you can just start the `./run-experiments.sh` script from within the `experiments/` directory. It uses the modified Kubernetes manifests in the `release/` directory.

You can plot the data using `./plot.py`, passing in the names of the directories where your results are stored as parameters.

## Data set

The data set from the paper is [in another repo](https://github.com/llarsson/hipster-shop-experiments).

