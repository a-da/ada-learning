# Kind

Setup local K8s on macOS and Ubuntu.

## Ensure that docker can access external IP

If not, configure docker DNS.

```bash
$ grep 'DOCKER_OPTS' /etc/default/docker
# Use DOCKER_OPTS to modify the daemon startup options.
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"

# if not, enable it 
vim /etc/default/docker
# add
# DOCKER_OPTS="--dns=my-private-dns-server-ip --dns=8.8.8.8"
```

## Install Dependencies

```bash
sudo apt install golang -y
go install sigs.k8s.io/kind@v0.25.0
go install sigs.k8s.io/cloud-provider-kind@latest

mkdir -p $HOME/go/bin
cd $HOME/go/bin
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl

vim .bashrc # add $HOME/go/bin to the path
```

## Find the external IP of the kind server

```bash
$ EXTERNAL_IP=$(curl -s ifconfig.me) && echo "external IP: ${EXTERNAL_IP}"
external IP: 99.158.01.30 # example output
```

## Deploy

Generate config.yml

```bash
vim ./run.sample.sh adjust deploy.py arguments  
./run.sample.sh
```

### Extract and update kubeadm on Control Plane Node

Once the deployment is done, configure K8s API with external IP

```bash
docker exec ada-oraclu-arm-control-plane \
  kubectl get configmap kubeadm-config \
    -n kube-system \
    -o jsonpath='{.data.ClusterConfiguration}' > /tmp/kubeadm.yaml

vim /tmp/kubeadm.yaml
# Add the EXTERNAL_IP to the certSANs list in kubeadm.yaml:
# apt update
# apt install vim
# vim kubeadm.yaml
# apiServer:
#    certSANs:
#      ...
#      - "99.158.01.30"     # New external IP example
```

### Regenerate the API Server Certificate

```bash
cat /tmp/kubeadm.yaml | 
  docker exec -i ada-oraclu-arm-control-plane sh -c 'cat > /tmp/kubeadm.yaml'
docker exec -it ada-oraclu-arm-control-plane bash
# Back up the old certificates
> mv /etc/kubernetes/pki/apiserver.{crt,key} ~
# Generate new certificates with the updated SANs:
> kubeadm init phase certs apiserver --config /tmp/kubeadm.yaml
> exit
```

## Configure client

### Configure client on local

```bash
$ kind export kubeconfig \
  --name=ada-oraclu-arm \
  --kubeconfig=$HOME/.kube/kind-ada-oraclu-arm.yml

$ vim $HOME/.kube/kind-ada-oraclu-arm.yml
# replace 0.0.0.0 with EXTERNAL_IP value !!!! 

```

### Test kubeconfig

```bash
$ export KUBECONFIG=$HOME/.kube/kind-ada-oraclu-arm.yml && \
  kubectl config use-context kind-ada-oraclu-arm # k8s activate kind-ada-oraclu-arm
$ kubectl get nodes
NAME                           STATUS   ROLES           AGE   VERSION
ada-oraclu-arm-control-plane   Ready    control-plane   94m   v1.31.2
ada-oraclu-arm-worker          Ready    <none>          93m   v1.31.2
ada-oraclu-arm-worker2         Ready    <none>          93m   v1.31.2
```

### Configure client on remote

After creating 'kubeconfig' see [Configure client on local](#configure-client-on-local),
follow the below commands.

```bash
scp oraclu:/home/ubuntu/.kube/kind-ada-oraclu-arm.yml  $HOME/.kube/kind-ada-oraclu-arm.yml
```

Test kubeconfig on remote, see [Test kubeconfig](#test-kubeconfig).

## Destroy

```bash
kind delete clusters ada-oraclu-arm
```

Delete registry if needed

```bash
docker rm -f kind-registry
```

Stop all running containers (Optional)

```bash
docker stop $(docker ps -aq)
```

Remove all containers (Optional)

```bash
docker rm $(docker ps -aq)
```

Remove all images (Optional)

```bash
docker rmi $(docker images -q)
```

Drop all containers and images if needed

```bash
docker system prune --all --force
```
