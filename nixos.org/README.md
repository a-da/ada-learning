Nix can partially replace the package managers on Linux (e.g. apt) and macOS (e.g. brew).
Instead of multiple package managers, we can use just one.

# Instruction

## How to Install It on Linux and macOS

https://nixos.org/manual/nix/stable/installation/#multi-user

```bash
bash <(curl -L https://nixos.org/nix/install) --daemon
```

## Activate

Add this into bash

```bash
source /nix/var/nix/profiles/default/etc/profile.d/nix.sh
```

## Install package

TODO: Automate installments with [Ansible](../ansible.com/README.md) or
[nixos configurations](https://nixos.org/manual/nixpkgs/stable/#sec-building-environment)

```bash
/nix/var/nix/profiles/default/bin/nix-env \
    -iA nixpkgs.firefox

# for package with licence
export NIXPKGS_ALLOW_UNFREE=1
/nix/var/nix/profiles/default/bin/nix-env \
    -iA nixpkgs.vscode

```

List of packages succcefully installed on MacOS:

- meld
- git
- openssh
- zip
- unzip
- ansible
- ansible-lint
- tree
- python312Full
- htop
- curl
- wget
- gnugrep
- bash
- xonsh
- sshfs
- screenfetch
- jq
- procps (pgrep, pkill and pfind for OpenBSD and Darwin (Mac OS X), see https://github.com/NixOS/nixpkgs/issues/141157)
- vscode
- awscli2

List of packages that have broken for macOS but may work, for example inn Ubuntu :
- firefox
- chromium
- thunderbird
- atop
- postfix
- wine
- sublime
- brave
