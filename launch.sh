#!/bin/bash

set -euo pipefail

ENV_NAME="quchemenv"
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"

#vertifie que l'env existe
if ! conda env list | grep -q "^$ENV_NAME\s"; then
  echo "Conda environment '$ENV_NAME' does not exist."
  echo "Please run the install script first."
  exit 1
fi

conda activate "$ENV_NAME"

#message si mal appele
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <TD_LOG_FILE> <OPT_LOG_FILE>"
  echo "Example: $0 examples/H2O_TD.log examples/H2O_OPT.log"
  exit 1
fi

TD_LOG="$1"
OPT_LOG="$2"


python3 main.py "$TD_LOG" "$OPT_LOG"
