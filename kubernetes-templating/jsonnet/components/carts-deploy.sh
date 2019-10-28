#!/bin/bash -e
DIR=$(dirname ${BASH_SOURCE[0]})

# Create namespace before anything else
kubectl apply -f ${DIR}/pre-deploy/ | column -t

for SECTION in manifests
do
  echo "## run kubectl apply for ${SECTION}"
  kubectl apply -f ${DIR}/${SECTION}/ | column -t
done
