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


# The following only concerns this branch of the project

## User installation (Linux)
### Installation
To get started, clone the repository and set the proper permissions:

```bash
git clone https://github.com/GiovanniCarre/QuChemReport.git
chmod 777 QuChemReport
cd QuChemReport
```

Then, run the installer

```bash
./installer
```

You can then run the application

```bash
./launch
```



## Configuration

The main configuration file is located in the config/ directory.

To create or edit a configuration file, use the provided HTML-based configuration generator:
"Generateur fichier configuration YAML.html"

This generator helps you easily build valid YAML files tailored for your report generation needs.

### File Structure

- config/: Contains YAML configuration files.
- "Generateur fichier configuration YAML.html": A tool to generate new YAML config files.
- installer: Installs required dependencies and sets up the environment.
- launch: Launches the main application with the default.yaml file in config/ as parameter.