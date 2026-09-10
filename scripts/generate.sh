#!/usr/bin/env bash
# Regenerate both SDKs from openapi/api.yaml + fern/overrides.yml.
# Requires Docker. Usage: scripts/generate.sh [typescript|python]...
set -euo pipefail

cd "$(dirname "$0")/.."
FERN_VERSION=$(python3 -c 'import json; print(json.load(open("fern/fern.config.json"))["version"])')
export FERN_NO_VERSION_REDIRECTION=true

groups=("$@")
[ ${#groups[@]} -eq 0 ] && groups=(typescript python)

for group in "${groups[@]}"; do
  # Fern's CLI can report success even when the generator container crashes,
  # so check the log for failures ourselves.
  log=$(npx -y "fern-api@${FERN_VERSION}" generate --local --force --group "$group" 2>&1) || { echo "$log"; exit 1; }
  echo "$log" | tail -1
  if echo "$log" | grep -q "Failed"; then echo "$log"; exit 1; fi
done

if [[ " ${groups[*]} " == *" typescript "* ]]; then
  python3 scripts/postprocess_typescript.py
fi
if [[ " ${groups[*]} " == *" python "* ]]; then
  python3 scripts/postprocess_python.py
fi
python3 scripts/naming_map.py

for dir in sdks/typescript/src sdks/python/src/t212; do
  if [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then echo "error: $dir is empty after generation" >&2; exit 1; fi
done
