#!/usr/bin/env bash

set -eu

KIND_NAME=${1:?ada-oraclu-amd}
DOCKER_ENGINE=${2:?docker podman nerdctl}

if kind get clusters | grep "${KIND_NAME}"
then
	echo '[INFO] cluster already exists'
else
	echo '[INFO] creating cluster'
	kind create cluster --name="${KIND_NAME}" --config=config.yml
fi

./kind-with-registry.sh "${DOCKER_ENGINE}" "${KIND_NAME}"

"${DOCKER_ENGINE}" pull gcr.io/google-samples/hello-app:1.0
"${DOCKER_ENGINE}" tag gcr.io/google-samples/hello-app:1.0 localhost:5001/hello-app:1.0
"${DOCKER_ENGINE}" push localhost:5001/hello-app:1.0
if kubectl get deployment/hello-server
then
    echo '[INFO] deployment exists'
else
    kubectl create deployment hello-server --image=localhost:5001/hello-app:1.0
fi

if pgrep -af cloud-provider-kind
then
    echo '[INFO] cloud-provider-kind is up'
else
    echo '[INFO] starting cloud-provider-kind ...'
    mkdir -p "${HOME}/logs"
    nohup cloud-provider-kind &>> "${HOME}/logs/cloud-provider-kind.log" &
fi

SERVICE_WITH_IP=service/lb-service-local
kubectl apply -f examples/loadbalancer_etp_local.yaml
kubectl get $SERVICE_WITH_IP
LB_EXTERNAL_IP=$(kubectl get $SERVICE_WITH_IP | head -n 2 | tail -n 1 | awk '{ print $4 }')
if [ "${LB_EXTERNAL_IP}" = '<pending>' ]
then
    echo '[INFO] wait for external IP 60 seconds ...'
    sleep 60	
    LB_EXTERNAL_IP=$(kubectl get $SERVICE_WITH_IP | head -n 2 | tail -n 1 | awk '{ print $4 }')
fi
curl -v --max-time 60 "${LB_EXTERNAL_IP}/hostname"
echo
