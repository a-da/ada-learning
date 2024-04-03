#!/usr/bin/env bash
: 'usage bash -x -eu -o pipefail build_docker_image.sh
See https://medium.com/oracledevs/building-multi-architecture-containers-on-oci-with-podman-67d49a8b965e
'
#
echo -n "${HARBOR_PASSWORD}" | podman login -u "${HARBOR_USERNAME}" --password-stdin "${HARBOR_HOST}"

# collect supported platform to build the image
platforms=$(podman run --privileged --rm docker.io/tonistiigi/binfmt --install all | grep -Eo 'linux[^"]+')

cd ./deployment/Jenkins/podman/ || exit 1

echo '[INFO] starting build...'

manifests=() # list of manifests
platform_succeeded=()
platform_failed=()

for platform in $platforms
do
  echo "platform: ${platform}"
  image_name="${PYTHON_WITH_PODMAN_IMAGE}-$(echo "${platform}" | tr '/' '-')"
  if podman build -t "${image_name}" --platform="${platform}" .
    then
      echo "add ${platform}"
      	# append built platform to the list of manifest
      	manifests+=("${image_name}")
      	platform_succeeded+=("${platform}")
    else
      platform_failed+=("${platform}")
  fi
done

echo "[INFO] platform_succeeded ${platform_succeeded[*]}"
echo "[WARN] platform_failed ${platform_failed[*]}"

exit 1

echo '[INFO] starting push images ...' &&
for manifest in ${manifests[*]}
do
  podman push "${manifest}"
done

echo '[INFO] Creating Manifests...' && \
podman manifest create "$(PYTHON_WITH_PODMAN_IMAGE)" "${manifests[*]}"
echo '[INFO] Pushing manifest...'

podman manifest push "$(PYTHON_WITH_PODMAN_IMAGE)" "docker://$(PYTHON_WITH_PODMAN_IMAGE)"

podman manifest rm "$(PYTHON_WITH_PODMAN_IMAGE)"

podman logout "${HARBOR_HOST}"
