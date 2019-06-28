# kubernetes-node-doktor

Keeps your Kubernetes nodes healthy

<img height="300" src="doktor.jpg">

### Setup

- Install Python 3.6
- Install dependencies with [Pipenv](https://docs.pipenv.org/en/latest/) using `pipenv sync`

### Building

```
docker build -t artsy/node-doktor .
```

### Distributing

```
docker tag artsy/node-doktor:latest artsy/node-doktor:$(cat VERSION)
docker push artsy/node-doktor:$(cat VERSION)
docker push artsy/node-doktor:latest
```

### Running

- Intended to be run on a Kubernetes node as a Daemonset.  See [examples/daemonset.yml][examples/daemonset.yml] for an example

- The environment variable `NODENAME` must be set to the name of the node running the Pod, using the Kubernetes downwards API

  ```
  env:
    - name: NODENAME
      valueFrom:
        fieldRef:
          fieldPath: spec.nodeName
  ```

- The Pod must have appropriate RBAC permissions to:
  - Get Pods
  - Get Events
  - Delete Pods
  - Cordon Nodes

  See [examples/serviceaccount.yml][examples/serviceaccount.yml] for an example
