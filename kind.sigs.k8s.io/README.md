# Kind

Setup local K8s on MacOS and Ubuntu.

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

Start cloud-provider-kind

```bash
mkdir -p $HOME/logs
nohup cloud-provider-kind &>> $HOME/logs/cloud-provider-kind.log &
```

## Deploy

```bash
export KIND_EXPERIMENTAL_PROVIDER=docker
./deploy.sh ada-oraclu-amd docker|podman|nerdctl
```

## Configure client

```bash
scp -i ../ssh-key-2024-11-18.key name@ip:/home/ubuntu/.kube/config  $HOME/.kube/kind-ada-oraclu-arm.yml
export KUBECONFIG=$HOME/.kube/kind-ada-oraclu-arm.yml && kubectl config use-context kind-ada-oraclu-arm # k8s activate kind-ada-oraclu-arm
kubectl config set-cluster kind-ada-oraclu-arm --insecure-skip-tls-verify=true
```

## Destroy

```bash
kind delete clusters ada-oraclu-arm
```

Delete registry if needed

```bash
docker rm -f kind-registry
```

Drop all containters and images if needed

```bash
docker system prune --all --force
```



