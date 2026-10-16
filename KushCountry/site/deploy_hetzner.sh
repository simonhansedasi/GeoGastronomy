#!/bin/bash
set -e

HETZNER="root@204.168.182.60"

echo "Syncing to Hetzner..."
rsync -av --checksum --delete \
  -e "ssh -i $HOME/.ssh/id_ed25519" \
  --exclude='deploy_hetzner.sh' \
  --exclude='nginx_kushcountry.conf' \
  --exclude='export_suitability_geojson.py' \
  --exclude='CLAUDE.md' \
  --exclude='CONTEXT.md' \
  --exclude='.ipynb_checkpoints' \
  ./ \
  "$HETZNER:/var/www/kushcountry/"

echo "Done. Live at https://kushcountry.simonhansedasi.com"
