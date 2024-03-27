1. Install Argo CD

Prepare Argo CD: check Minikube

   ``` bash
   $ minikube status
   minikube
   type: Control Plane
   host: Running
   kubelet: Running
   apiserver: Running
   kubeconfig: Configured
   ``` 

Follow the commands in https://gitlab.com/nanuchi/argocd-app-config.

   ``` bahs
   # install Argo CD in k8s
   $ kubectl create namespace argocd
   $ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

   # login with admin user and below token (as in documentation):
   $ kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode && echo
   kbtR93X49h1ymjnv # exemple of passwoed
   # you can change and delete init password
   ```

2. Start/Open Argo CD

Make port forwarding with an SSH tunnel.

   ``` bash
   $ export PORT=19502 && ssh -t -t -L $PORT:127.0.0.1:$PORT oraclu kubectl port-forward svc/argocd-server $PORT:443 -n argocd 
   ```

Open page

   ``` bash
   open http://127.0.0.1:19502 
   ``` 

3. Provision Argo CD

   Install CLI and configure it.

   More in https://www.youtube.com/watch?v=xxF0y7V1PfA

Optional: Install 'Kustomize'

   ``` bash
   curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash
   /home/ada/kustomize /home/ada/bin/
   ```

Optional: Install Helm

   ``` bash
   curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
   sudo apt-get install apt-transport-https --yes
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
   sudo apt-get update
   sudo apt-get install helm
   ```

Install the Argo CD CLI for troubleshooting, if needed.

   ``` bash
   $ curl -sSL -o ${HOME}/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-arm64
   $ chmod +x ${HOME}/bin/argocd
   $ kubectl config set-context --current --namespace=argocd
   $ argocd login --core
   $ argocd version -n argocd
    argocd: v2.9.3+6eba5be
    BuildDate: 2023-12-01T23:24:09Z
    GitCommit: 6eba5be864b7e031871ed7698f5233336dfe75c7
    GitTreeState: clean
    GoVersion: go1.21.4
    Compiler: gc
    Platform: linux/arm64
    argocd-server: v2.9.3+6eba5be
    BuildDate: 2023-12-01T23:24:09Z
    GitCommit: 6eba5be864b7e031871ed7698f5233336dfe75c7
    GitTreeState: clean
    GoVersion: go1.21.4
    Compiler: gc
    Platform: linux/arm64
    Kustomize Version: v5.3.0 2023-12-07T10:45:14Z
    Helm Version: v3.13.3+gc8b9489
    Kubectl Version: v0.24.2
    Jsonnet Version: v0.20.0
   ```

4. Use declarative setup (see https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)

E.g., create a new Jenkins app from Helm Chart charts.jenkins.io.

   ``` bash
   $ kubectl apply -f ../jenkins.io/argo-cd.yaml
   ```
