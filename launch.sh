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

# rm -f temp/*

conda activate "$ENV_NAME"

python3 main.py
