#!/bin/bash

set -e
conda create -n quchemenv python=3.8.0 numpy=1.19.5 scipy=1.9.3 scikit-learn=0.23.2 -c conda-forge -y
source ~/miniconda3/etc/profile.d/conda.sh
conda activate quchemenv
pip install requests==2.25.1 psutil==5.8.0 cclib==1.8.1 Pillow==8.1.2 pylatex==1.4.1
conda install -c conda-forge openbabel -y
conda install -c conda-forge mayavi -y
sudo apt update
sudo apt install -y python3-dev cython3 libhdf5-dev gcc g++ git
rm -rf orbkit
git clone https://github.com/orbkit/orbkit.git
cd orbkit/
pip install cython==0.29.21
pip install .
cd ..
python3 main.py examples/H2O_TD.log examples/H2O_OPT.log