Setup debian environment
- install utm https://dev.to/ruanbekker/how-to-run-a-amd64-bit-linux-vm-on-a-mac-m1-51cp
  Multiple shared directories? https://github.com/utmapp/UTM/discussions/5463
  https://docs.getutm.app/guest-support/linux/#fixing-permission-errors

- download debian server mininal
- backup the system with timeshift
  su -
  https://dev.to/rahedmir/how-to-use-timeshift-from-command-line-in-linux-1l9b
  sudo timeshift --create --comments "after curl"
- apt install vim sudo
- sudo usermod -aG sudo username
- nixos https://github.com/nix-community/setup.nix/blob/master/README.rst
nix-env -if 01.cli.platform-all.new.nix
- apt install docker.io podman
  sudo usermod -aG docker ada

  
