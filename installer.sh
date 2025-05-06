#!/bin/bash

set -e
conda create -n quchemenv python=3.9 numpy=1.22.4 scipy=1.9.3 scikit-learn=1.1.3 -c conda-forge -y
source ~/miniconda3/etc/profile.d/conda.sh
conda activate quchemenv
pip install requests psutil cclib Pillow pylatex
conda install -c conda-forge openbabel -y
conda install -c conda-forge mayavi -y
sudo apt update
sudo apt install -y python3-dev cython3 libhdf5-dev gcc g++ git
rm -rf orbkit
git clone https://github.com/orbkit/orbkit.git
cd orbkit/
pip install cython
pip install .
cd ..
python main.py
