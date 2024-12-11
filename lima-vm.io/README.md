# Lima

Setup K8s environment amd64 on arm64 host.

https://lima-vm.io/docs/usage/

Install Lima

```bash
git clone https://github.com/lima-vm/lima.git
cd lima
make
make install
```

Show vm's

```bash
$ ./_output/bin/limactl list
NAME        STATUS     SSH                VMTYPE    ARCH      CPUS    MEMORY    DISK     DIR
ada-lima    Running    127.0.0.1:33005    qemu      x86_64    2       8GiB      30GiB    ~/.lima/ada-lima
```

Stop vm

```bash
$ ./_output/bin/limactl stop ada-lima
INFO[0000] Sending SIGINT to hostagent process 902698
INFO[0000] Waiting for the host agent and the driver processes to shut down
INFO[0000] [hostagent] Received SIGINT, shutting down the host agent
INFO[0000] [hostagent] Shutting down the host agent
INFO[0000] [hostagent] Stopping forwarding "/run/lima-guestagent.sock" (guest) to "/home/ubuntu/.lima/ada-lima/ga.sock" (host)
INFO[0000] [hostagent] Unmounting "/home/ubuntu"
INFO[0000] [hostagent] Unmounting "/tmp/lima"
INFO[0000] [hostagent] Shutting down QEMU with the power button
INFO[0000] [hostagent] Sending QMP system_powerdown command
INFO[0066] [hostagent] QEMU has exited
```

Delete vm

```bash
./_output/bin/limactl delete ada-lima
INFO[0000] The qemu driver process seems already stopped
INFO[0000] The host agent process seems already stopped
INFO[0000] Removing *.pid *.sock *.tmp under "/home/ubuntu/.lima/ada-lima"
INFO[0000] Removing "/home/ubuntu/.lima/ada-lima/ha.sock"
INFO[0000] Deleted "ada-lima" ("/home/ubuntu/.lima/ada-lima")
```

Prepare lima 

```
sudo apt-get install qemu-utils
sudo apt install qemu-system-x86
```

Create Lima config

```bash
$ ./_output/bin/limactl create --name=ada-lima --arch=x86_64 --cpus=2 --disk=40 --memory=10
? Creating an instance "ada-lima" Proceed with the current configuration
INFO[0001] Attempting to download the image              arch=x86_64 digest="sha256:05bbfe57d7701c685d8c65f4d34cebe947bc89e3509c4d8a2b9c77f39e91f3ca" location="https://cloud-images.ubuntu.com/releases/24.10/release-20241109/ubuntu-24.10-server-cloudimg-amd64.img"
INFO[0002] Using cache "/home/ubuntu/.cache/lima/download/by-url-sha256/34285004a5a0d8294d0fa023a74e47ad44f780ae0a9a50bd27689a9a93d310fe/data"
INFO[0002] Attempting to download the nerdctl archive    arch=x86_64 digest="sha256:e117ee6af35dc1ba66fb68fa99baf45bc2123c5261e7e41aa0a199de55ec9443" location="https://github.com/containerd/nerdctl/releases/download/v2.0.1/nerdctl-full-2.0.1-linux-amd64.tar.gz"
INFO[0002] Using cache "/home/ubuntu/.cache/lima/download/by-url-sha256/7d3048f2653a4c1783d2aff89fa2bccca3eb5bfcbdb3fb6dafbb7c7750a78951/data"
INFO[0002] Run `limactl start ada-lima` to start the instance.
```

Start Lima
```bash
$ ./_output/bin/limactl start ada-lima
? Creating an instance "ada-lima" Proceed with the current configuration
INFO[0001] Attempting to download the image              arch=x86_64 digest="sha256:05bbfe57d7701c685d8c65f4d34cebe947bc89e3509c4d8a2b9c77f39e91f3ca" location="https://cloud-images.ubuntu.com/releases/24.10/release-20241109/ubuntu-24.10-server-cloudimg-amd64.img"
INFO[0002] Using cache "/home/ubuntu/.cache/lima/download/by-url-sha256/34285004a5a0d8294d0fa023a74e47ad44f780ae0a9a50bd27689a9a93d310fe/data"
INFO[0002] Attempting to download the nerdctl archive    arch=x86_64 digest="sha256:e117ee6af35dc1ba66fb68fa99baf45bc2123c5261e7e41aa0a199de55ec9443" location="https://github.com/containerd/nerdctl/releases/download/v2.0.1/nerdctl-full-2.0.1-linux-amd64.tar.gz"
INFO[0002] Using cache "/home/ubuntu/.cache/lima/download/by-url-sha256/7d3048f2653a4c1783d2aff89fa2bccca3eb5bfcbdb3fb6dafbb7c7750a78951/data"
INFO[0002] Run `limactl start ada-lima` to start the instance.
```

Shell Lima
```bash
$ ./_output/bin/limactl shell ada-lima -- bash -c 'date'
Wed Dec 11 10:46:32 UTC 2024
```


