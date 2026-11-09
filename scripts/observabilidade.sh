#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose -f observabilidade/compose.yaml up -d
container=$(docker compose -f observabilidade/compose.yaml ps -q elasticsearch)
ip=$(docker inspect -f '{{(index .NetworkSettings.Networks "kind").IPAddress}}' "$container")
test -n "$ip"
kubectl --context kind-devops create namespace devops --dry-run=client -o yaml | kubectl --context kind-devops apply -f -
sed "s/ELASTICSEARCH_IP/$ip/g" observabilidade/filebeat.yaml | kubectl --context kind-devops apply -f -
kubectl --context kind-devops -n devops rollout restart daemonset/filebeat
kubectl --context kind-devops -n devops rollout status daemonset/filebeat --timeout=180s
