# QuChemReport

QuChemReport is a Python module for molecular quantum chemistry calculations results. 

The project was started in 2010 by Thomas CAUCHY, assistant professor in the MOLTECH-Anjou laboratory of the University of Angers (FRANCE).
At first a computational chemist program maintained by Thomas CAUCHY and Yohann MORILLE, the project boomed with the involvment of Benoit DA MOTA. 
Benoit DA MOTA is a computer scientist assistant professor of the LERIA laboratory of the University of Angers.

Installation
Dependencies
QuChemReport works with:

Python (>= 3.5)
NumPy
SciPy

For the parsing process:
requests
Openbabel (>= 2.4.1) (apt install openbabel-dev and pip3 install openbabel)
Cclib (>= 1.5)
Scikit-learn
scanlog (pip3 install scanlog)

For  the discretization process:
cython3
python3-h5py
Orbkit (git clone https://github.com/orbkit/orbkit.git, beware to export ORBKITPATH)

For the vizualization process:
latex (pdflatex)
pylatex (pip3 install pylatex)
PIL or on conda pillow
Matplotlib (>3.1)
Mayavi (pip3 install : beware of pyface install ! problem with Qt4, Qt5 in profile : export QT_API=pyqt, export ETS_TOOLKIT=qt4)

User installation

git clone https://github.com/BenoitDamota/QuChemReport.git


# Using Profiles (.env or .json)

QuChemReport supports reusable configuration profiles to simplify repeated runs.
Profiles can be stored as .env or .json files in the profiles/ directory.
Example of a .env profile

# profiles/default.env
```
mode=full
restart=0
nproc=4
mem=8
MEP=false
noMO=false
noEDD=false
verbose=true
```

The .env format is human-readable and editable with any text editor.
Example of a .json profile

// profiles/default.json
```
{
  "mode": "full",
  "restart": 0,
  "nproc": 4,
  "mem": 8,
  "MEP": false,
  "noMO": false,
  "noEDD": false,
  "verbose": true
}
```

The .json format is ideal for scripting or automated generation of configuration files.
Running with a Profile

To launch QuChemReport using a profile:

```
python main.py file1.log file2.log --profile default
```

This will automatically load `profiles/default.env` or `profiles/default.json`, whichever exists.

### Available Profile Parameters

- **mode**: Report verbosity. Can be `full`, `si`, or `text`.
- **restart**: Restart mode. Use `1` to skip image regeneration if already available, or `0` to force reprocessing.
- **nproc**: Number of CPU cores used during the discretization process.
- **mem**: Amount of RAM allocated for processing (in GB).
- **MEP**: Set to `true` to generate Molecular Electrostatic Potential (MEP) images.
- **noMO**: Set to `true` to disable the generation of Molecular Orbital images.
- **noEDD**: Set to `true` to disable the Electronic Density Difference images.
- **verbose**: Set to `true` to print execution details.

Project History

Help and Support
Documentation

Communication

Citation



