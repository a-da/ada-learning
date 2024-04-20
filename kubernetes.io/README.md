Setup a kuberneted is not a trivial task, it just depends.
Bellow there is effort to document how to setup on Virtual box and Ubuntu 23.10
with master only. The instructions are cofeed with a lot of reference to external links.

# Environment 

To be installed on Virtual Box with ubuntu-23.10-live-server-amd64.iso

TODO: automate the setup with ansible script

# 1. Install Virtual box

Configure NAT network.

# 2. Create a new Virtual Machine 

See [Environment](#environment) Section.

Ensure that we alocate enough resource to comply as expected in [[01]]. 

# 2. Create a new Virtual Machine 

See a screencast here [02].

# 3. Installing kubeadm

Follow the instractions from the official documentation [[03]].

## 3.1 Install all the took required 

```bash
sudo apt install THE-PAKAGE
```
THE-PAKAGE list with comments:
- **netcat-openbsd**: **nc** commands for cheking ports

## 3.2 Before you begin

We should have at least 2GB of RAM.
```bash
free -mh
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       368Mi       7.4Gi       680Ki       217Mi       7.4Gi
Swap:             0B          0B          0B
```

We should have at least 2 CPUs
```bash
$ nproc --all
4
```

Check required ports. From belows commands output looks like port is available for us.
```bash
$ nc 127.0.0.1 6443 -v
nc: connect to 127.0.0.1 port 6443 (tcp) failed: Connection refused
```

Swap configuration. From belows commands output looks like swap is disabled.
```bash
free -mh
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       368Mi       7.4Gi       680Ki       217Mi       7.4Gi
Swap:             0B          0B          0B
```

# 3.3 Check network adapters

Acordind to [05], since we have two networks we will need to add "192.168.10.4" into /etc/hosts.

```bash
$ ifconfig -a
enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.114  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fe05:e7bb  prefixlen 64  scopeid 0x20<link>
        inet6 2a02:3032:303:6d00:a00:27ff:fe05:e7bb  prefixlen 64  scopeid 0x0<global>
        ether 08:00:27:05:e7:bb  txqueuelen 1000  (Ethernet)
        RX packets 1137  bytes 159982 (159.9 KB)
        RX errors 0  dropped 1  overruns 0  frame 0
        TX packets 1467  bytes 162307 (162.3 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enp0s8: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.10.4  netmask 255.255.255.0  broadcast 192.168.10.255
        inet6 fe80::a00:27ff:fe36:916  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:36:09:16  txqueuelen 1000  (Ethernet)
        RX packets 34  bytes 9452 (9.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 49  bytes 7021 (7.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Replace in /etc/hosts
```bash
# 127.0.1.1 kube-master
192.168.10.4 kube-master
```

# 3.4 Installing a container runtime

Install **cri-dockerd**.
```bash
$ wget https://github.com/Mirantis/cri-dockerd/releases/download/v0.3.13/cri-dockerd_0.3.13.3-0.ubuntu-jammy_amd64.deb
$ sudo apt install ./cri-dockerd_0.3.13.3-0.ubuntu-jammy_amd64.deb 
```

Install Docker, follow  [[05]].

# 3.5 Installing kubeadm, kubelet and kubectl

Follow the official instruction [[06]].

[comments]: Links:::::::::::::::::::::::::::::::::

[01]: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin
[02]: https://youtu.be/EHDDm_iR1Fs?t=546
[03]: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
[04]: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#check-network-adapters
[05]: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
[06]: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl
