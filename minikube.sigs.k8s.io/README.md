Importantly, (!) Minikube cannot be used as a proper stage environment, and for this reason there is a proper setup here, [kubernetes.io](../kubernetes.io/README.md).

1. Install Minikube

   Follow https://minikube.sigs.k8s.io/docs/start/

   ``` bash
   $ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_arm64.deb
   $ sudo dpkg -i minikube_latest_arm64.deb
   $ minikube start
   $ kubectl get po -A
   $ minikube kubectl -- get po -A
   $ minikube addons enable metrics-server
   ```

2. Install 'kubectl'

   Following commands https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

   ``` bash
   $ sudo apt-get update
   $ sudo apt-get install -y apt-transport-https ca-certificates curl
   $ curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
   $ echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
   $ sudo apt-get update
   $ sudo apt-get install -y kubectl
   $ kubectl version
   Client Version: v1.29.0
   Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
   Server Version: v1.28.3
   ```
