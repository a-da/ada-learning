#!/usr/bin/env python
# pylint: disable=line-too-long
"""
$ ./config_template.py \
  --hostPath=$HOME/github.com/asta-s-eu/teams/scraping-dev/scraping-kleinanzeigen.de/tests/KLEINANZEIGEN_DE_CONFIG_FOLDER \
  --containerPath=/mnt/github.com/asta-s-eu/teams/scraping-dev/scraping-kleinanzeigen/KLEINANZEIGEN_DE_CONFIG_FOLDER
"""
# pylint: enable=line-too-long
from pathlib import Path
import argparse


def cli() -> None:
    """
    Command line interface
    """
    parser = argparse.ArgumentParser(
        prog='kind.config.template',
        description='Generate the Kind config.yaml'
    )
    parser.add_argument('--apiServerPort', default=6443)
    parser.add_argument('--hostPath', required=True, type=str)
    parser.add_argument('--containerPath', required=True, type=str)

    args = parser.parse_args()

    main(
        api_server_port=args.apiServerPort,
        host_path=args.hostPath,
        container_path=args.containerPath
    )


def main(api_server_port: str, host_path: str, container_path: str) -> None:
    """Render new config"""
    template = Path(__file__).parent.joinpath("config.template.yaml").read_bytes().decode()

    content = template.format(
        apiServerPort=api_server_port,
        hostPath=host_path,
        containerPath=container_path
    )
    to_file = Path(__file__).parent.joinpath("config.yaml")
    to_file.write_bytes(content.encode())
    print(f"[DONE] {to_file}")



if __name__ == "__main__":
    cli()
