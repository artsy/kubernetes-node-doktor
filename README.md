# kubernetes-node-doktor

Keeps your Kubernetes nodes healthy

<img height="300" src="doktor.jpg">

### Setup

- Install Python 3.6
- Install dependencies with [Pipenv](https://docs.pipenv.org/en/latest/) using `pipenv sync`

### Running

Intended to be run on a Kubernetes node as a Daemonset

The environment variable `NODENAME` must be set to the name of the node running the Pod, using the Kubernetes downwards API

```
env:
  - name: NODENAME
    valueFrom:
      fieldRef:
        fieldPath: spec.nodeName
```

The environment variable `KUBECONFIG` must be set to a Kubectl config file with appropriate RBAC permissions to:
- Get Pods
- Get Events
- Delete Pods
- Cordon Nodes
