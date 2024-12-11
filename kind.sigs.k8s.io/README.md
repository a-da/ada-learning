# Kind

Setup local K8s on MacOS and Ubuntu.

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

