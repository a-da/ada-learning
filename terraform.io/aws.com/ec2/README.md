The deployment will be based on https://spacelift.io/blog/terraform-ec2-instance with some updates.

# Prerequisites

## 2. Terraform installed.

Install it with NixOS (see [nixos](../../../nixos.org/README.md#install-package)).

```bash
export NIXPKGS_ALLOW_UNFREE=1  # accept license
nix-env -iA nixpkgs.terraform
```

## 3. AWS CLI installed.

Install it with NixOS (see [nixos](../../../nixos.org/README.md#install-package)).

```bash
nix-env -iA nixpkgs.awscli2
```

Check if we can at least query EC2 with the existing default profile.

```bash
export AWS_DEFAULT_PROFILE=digitalcloud2
> aws ec2 describe-instances
{
    "Reservations": []
}
```

# Terraform script

## Update 1

Since we are using a default profile, we will remove the profile
``provider "aws"`` in [main.tf](main.tf).

## Update 2

To lower the cost, we will use the ARM image
(Amazon Linux 2 Kernel 5.10 AMI 2.0.20240329.0 x86_64 HVM gp2)
instead of AMD.
