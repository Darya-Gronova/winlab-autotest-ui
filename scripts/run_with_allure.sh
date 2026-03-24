#!/usr/bin/env bash
# Helper to run pytest and generate/serve Allure report.
# Usage:
#   bash scripts/run_with_allure.sh
# Requirements:
#   - Python deps from requirements.txt installed
#   - Allure Commandline installed and available in PATH (https://docs.qameta.io/allure/)

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Use timestamped results and report directories so CI artifacts don't collide
TIMESTAMP=$(date -u +"%Y%m%d-%H%M%S")
RESULTS_DIR="allure-results-$TIMESTAMP"
REPORT_DIR="allure-report-$TIMESTAMP"

echo "Running pytest -> results: $RESULTS_DIR"
python -m pytest --alluredir="$RESULTS_DIR" "$@"

# Generate report (if allure CLI present)
if command -v allure >/dev/null 2>&1; then
  echo "Generating Allure report from $RESULTS_DIR..."
  allure generate --clean "$RESULTS_DIR" -o "$REPORT_DIR"
  echo "Allure report generated at: $ROOT_DIR/$REPORT_DIR"
  echo "To serve the report locally run: allure open $REPORT_DIR"
else
  echo "Allure CLI not found in PATH. Install it to generate/serve reports: https://docs.qameta.io/allure/"
  echo "Test results are in: $ROOT_DIR/$RESULTS_DIR"
fi
