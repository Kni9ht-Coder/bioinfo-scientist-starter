#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST=${1:-wslgpu}
REMOTE_PATH=${2:-~/projects/bioinfo-scientist-starter}

rsync -avP "${REMOTE_HOST}:${REMOTE_PATH}/results/" ./results/
rsync -avP "${REMOTE_HOST}:${REMOTE_PATH}/manuscript/figures/" ./manuscript/figures/
