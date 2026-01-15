#!/usr/bin/env bash


function init_apple_container {
  local pkg_url="${1:-https://github.com/apple/container/releases/download/0.2.0/container-0.2.0-installer-signed.pkg}"
  local container_name="${2:-ubuntu}"
  local container_image="${3:-my_ubuntu}"
  local container_arch="${4:-amd64}"


  container --version || true

  # shellcheck disable=SC2181
  if [ $? == 0 ]
  then
      echo 'Apple container is installed'
  else
      echo 'Installing Apple container'
      parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
      curl "${pkg_url}" --output="${parent_path}/container-installer.pkg"
      open container-installer.pkg
  fi

  container system start

  container system dns list | grep -qE "^test$" || sudo container system dns create test
  container system dns default set test
  
  container list -a | grep -qE "^$container_name " || exit_code=$?

  # shellcheck disable=SC2181
  if [ ${exit_code:-0} == 0 ]
    then
        echo 'Container running'
    else
        echo 'Running container'
        container run \
            --name "${container_name}" \
            --detach \
            --rm \
            --cpus 8 \
            --memory 8g \
            --arch=amd64 \
            --volume "${HOME}:/mnt/home" \
            "${container_image}"

    fi

  #container start "${container_name}" || true
}

case $1:

  start ):
     /usr/sbin/sshd -D
    ;;
 init ):
    init_apple_container
    ;;
   
esac    
