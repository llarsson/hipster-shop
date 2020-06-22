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

## Cache and Estimator

You can find the code for the Hipster Shop [Cache](https://github.com/llarsson/caching-grpc-reverse-proxy) and [Estimator](https://github.com/llarsson/grpc-caching-estimator) in their respective repos. The names of the projects are out of date and imply far more generality than they should. The [gRPC caching interceptors](https://github.com/llarsson/grpc-caching-interceptors/) are what is general about this proposed software, the Cache and Estimator components themselves are project-specific. However, the code for these components is easy to generate using [our modified Protobuf compiler](https://github.com/llarsson/protobuf) and a future software engineering development task would be to automate generation of Cache and Estimator components from Protobuf service descriptors, so that a service mesh could offer this functionality natively.

## Data set

The data set from the paper is [in another repo](https://github.com/llarsson/hipster-shop-experiments).

