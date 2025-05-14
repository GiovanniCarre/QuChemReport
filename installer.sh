#!/bin/bash

set -euo pipefail
ENV_NAME="quchemenv"

#Supprime env si existe deja
if conda info --envs | grep -q "^$ENV_NAME"; then
  echo "Suppression environnement existant: $ENV_NAME"
  conda remove -n "$ENV_NAME" --all -y
fi

#creation de l'environnement et priorite strict pour l'installation 
conda config --add channels conda-forge
conda config --set channel_priority strict

conda create -n "$ENV_NAME" \
  python=3.8 \
  numpy=1.21.6 \
  scipy=1.9.3 \
  scikit-learn=0.23.2 \
  openbabel \
  mayavi \
  -c conda-forge -y

#active environnement conda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"


pip install \
  requests==2.25.1 \
  psutil==5.8.0 \
  cclib==1.8.1 \
  Pillow==10.4.0 \
  pylatex==1.4.1 \
  cython==0.29.21 \
  python-dotenv==1.0.1 \
  python-docx==1.1.2


#dependences (pour orbkit et mayavi)
sudo apt update
sudo apt install -y python3-dev cython3 libhdf5-dev gcc g++ git

#clone d'orbkit pour l'installer
cd "$(dirname "$0")"
rm -rf orbkit
git clone https://github.com/orbkit/orbkit.git
cd orbkit
pip install .
cd ..

python3 main.py examples/H2O_TD.log examples/H2O_OPT.log
