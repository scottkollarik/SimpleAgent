#!/bin/zsh
# Rebuild containers from scratch and bring them up


echo "Tearing down any existing containers..."
docker compose down --volumes --remove-orphans
docker image prune
echo "Rebuilding all containers (no cache)..."
docker compose build --no-cache

echo "Starting containers..."
docker compose up