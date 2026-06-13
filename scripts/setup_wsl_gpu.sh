#!/usr/bin/env bash
set -euo pipefail

sudo apt update
sudo apt install -y git git-lfs make curl wget build-essential tree unzip rsync openssh-server htop nvtop
sudo service ssh start || true
git lfs install

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi
else
  echo "nvidia-smi not found. Install/update NVIDIA Windows driver with WSL support, then reopen WSL."
fi

echo "WSL base tools installed. Next: install Miniforge and create envs/aidd-gpu.yml."
