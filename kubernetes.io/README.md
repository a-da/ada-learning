# I FAILED TO SETUP ! TO RETRY ON FRESH OS, maybe on TUXEDO

Important (!) [minikube.sigs.k8s.io](../minikube.sigs.k8s.io/README.md) minikube can not be used as a proper stage env,
and for this reason we are using for that case pure K8s setup.

Follow https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

# Download the binary

``` bash
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
```

# Validate the binary
``` bash
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl.sha256"
$ echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
kubectl: OK
```

# Install kubectl

``` bash
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
$ kubectl version --client
Client Version: v1.29.0
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
```

# Install using native package management
``` bash
$ sudo apt-get update
# apt-transport-https may be a dummy package; if so, you can skip that package
$ sudo apt-get install -y apt-transport-https ca-certificates curl

$ curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
$ echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

$ sudo apt-get update
$ sudo apt-get install -y kubectl
```
