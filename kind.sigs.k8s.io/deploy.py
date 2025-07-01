#!/usr/bin/env python
"""Initialize Kind cluster"""
import argparse
import os
import time
from pathlib import Path

from bash import bash
import config_template


def upsert_kind_cluster(args: argparse.Namespace) -> None:
    """
    Create Kind cluster if not exists
    """
    print(f"[INFO] Upsert kind cluster {args.kind_name!r}")
    _, output = bash("kind get clusters")

    if any(args.kind_name == i[1] for i in output):
        print("[INFO] cluster already exists")
    else:
        config_template.main(
            api_server_port=args.apiServerPort,
            host_path=args.hostPath,
            container_path=args.containerPath
        )
        bash(
            "kind create cluster "
            f"--name={args.kind_name} "
            "--config=config.yaml"
        )


def upsert_registry_container(args: argparse.Namespace) -> None:
    """
    Create registry container if not exists
    """
    bash((
        "./kind-with-registry.sh",
        args.container_engine,
        args.kind_name
    ))


def initialize_cloud_provider_kind() -> None:
    """Start cloud provider if not started"""
    error_code, _ = bash(
        "pgrep -af cloud-provider-kind",
        exit_on_error_code=False
    )
    if not error_code:
        print('[INFO] cloud-provider-kind is up')
    else:
        print('[INFO] starting cloud-provider-kind ...')
        Path.home().joinpath("logs").mkdir(exist_ok=True)
        bash('nohup cloud-provider-kind &>> "${HOME}/logs/cloud-provider-kind.log" &')


def test_registry_container(args: argparse.Namespace) -> None:
    """
    Upload and pull from K8s docker image in/from registry
    """
    bash(f"{args.container_engine} pull gcr.io/google-samples/hello-app:1.0")
    bash(f"{args.container_engine} tag gcr.io/google-samples/hello-app:1.0 "
         "localhost:5001/hello-app:1.0")
    bash(f"{args.container_engine} push localhost:5001/hello-app:1.0")
    error_code, _ = bash(
        "kubectl get deployment/hello-server",
        exit_on_error_code=False
    )
    if not error_code:
        print('[INFO] deployment exists')
    else:
        bash("kubectl create deployment hello-server "
             "--image=localhost:5001/hello-app:1.0")


def initialize_load_balancer() -> None:
    """
    Create load balancer if not exists
    """
    print("[INFO] initialize load balancer")
    service_with_ip="service/lb-service-local"
    bash("kubectl apply -f examples/loadbalancer_etp_local.yaml")

    for _ in range(5):
        _, output = bash(f"kubectl get {service_with_ip} "
                         "-o custom-columns=EXTERNAL-IP:.status.loadBalancer.ingress[0].ip "
                         "--no-headers")

        lb_external_ip = output[0][1].decode()

        if lb_external_ip == '<pending>':
            print('[INFO] wait for external IP 10 seconds ...')
            time.sleep(10)
            continue

        print(f"[INFO] found external IP: {service_with_ip}")
        print('[INFO] give 5 seconds time ...')

        bash("curl -v "
             "--connect-timeout 5 "
             "--max-time 10 "
             "--retry 5 "
             "--retry-delay 0 "
             "--retry-max-time 40 "  
            f"{lb_external_ip}/hostname")

        break


def main(args: argparse.Namespace) -> None:
    """Initialize Kind cluster"""
    upsert_kind_cluster(args)
    upsert_registry_container(args)
    test_registry_container(args)
    initialize_cloud_provider_kind()
    initialize_load_balancer()


def cli() -> None:
    """Command line interface"""
    parser = argparse.ArgumentParser()

    default_kind_name = os.getenv("ASE_KIND_NAME") or "ada-oraclu-arm"
    default_container_engine = os.getenv("ASE_CONTAINER_ENGINE") or "docker"

    parser.add_argument("--kind-name",
                        default=default_kind_name,
                        help=f"Default: {default_kind_name}")
    parser.add_argument("--container-engine",
                        choices=["docker", "podman", "nerdctl"],
                        default=default_container_engine,
                        help=f"Default: {default_container_engine}")
    parser.add_argument('--apiServerPort', default=6443)
    parser.add_argument('--hostPath', required=True, type=str)
    parser.add_argument('--containerPath', required=True, type=str)

    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli()
