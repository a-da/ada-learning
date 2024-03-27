# Why

Jenkins is de facto a CI for enterprises. At lease was used back in 2019 in Klarna.

# How

## Flow

Let's automate deployments of the server on the free cloud.oracle.com server.
The automation will be done on top of the [Minikube](../minikube.sigs.k8s.io/README.md) instance,
with [Argo CD](../argo-cd.readthedocs.io/README.md).

## Install Jenkins

```bash
kubectl apply -f argo-cd.yaml
```

## Get user/password

```bash
kubectl get secret jenkins -n default -o jsonpath="{.data.jenkins-admin-user}" | base64 -d
kubectl get secret jenkins -n default -o jsonpath="{.data.jenkins-admin-password}" | base64 -d
```
## Start/Open Jenkins

Make port forwarding with SSH tunnel

``` bash
$ export PORT=19501 && ssh -t -t -L $PORT:127.0.0.1:$PORT oraclu kubectl port-forward svc/jenkins $PORT:8080 -n default 
```

Open page

``` bash
open http://127.0.0.1:19502 
``` 
