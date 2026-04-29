#!/usr/bin/env bash
set -euxo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y \
  build-essential \
  curl \
  git \
  htop \
  libpcap-dev \
  python3 \
  python3-pip \
  python3-venv \
  tmux

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

cd "$ROOT_DIR"
uv sync

git config --global credential.helper store
printf '%s\n' "set -g history-limit 10000000" > "$HOME/.tmux.conf"
tmux source-file "$HOME/.tmux.conf" || true
