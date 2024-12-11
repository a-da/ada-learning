# Kind

Setup local K8s on MacOS and Ubuntu.

## Install Dependencies

```bash
sudo apt install golang
go install sigs.k8s.io/kind@v0.25.0
go install sigs.k8s.io/cloud-provider-kind@latest
vim .bashrc # add $HOME/go/bin to the path
```

Start cloud-provider-kind

```bash
mkdir $HOME/logs
ubuntu@lima-ada-lima:/home/ubuntu/github.com/a-da/ada-learning:kind.sigs.k8s.io/kind.sigs.k8s.io$ nohup cloud-provider-kind &>> $HOME/logs/cloud-provider-kind.log &
```

## Deploy

```bash
./deploy ada-oraclu-amd docker|podman|nerdctl
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

