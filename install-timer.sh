#!/usr/bin/env bash
# Install the daily collector timer as a systemd *user* unit (Linux).
set -euo pipefail
VAULT="$(cd "$(dirname "$0")" && pwd)"
UNIT_DIR="$HOME/.config/systemd/user"
mkdir -p "$UNIT_DIR"
sed "s|__VAULT__|$VAULT|" "$VAULT/Machine/Collectors/systemd/maquina.service.in" > "$UNIT_DIR/vault-collectors.service"
cp "$VAULT/Machine/Collectors/systemd/maquina.timer" "$UNIT_DIR/vault-collectors.timer"
systemctl --user daemon-reload
systemctl --user enable --now vault-collectors.timer
systemctl --user list-timers vault-collectors.timer
