#!/usr/bin/env bash
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
  echo "Install Homebrew first: https://brew.sh/"
  exit 1
fi

brew install git git-lfs wget tree rsync openssh
brew install --cask visual-studio-code zotero

git lfs install

echo "Mac base tools installed. Next: install Miniforge and Codex CLI."
