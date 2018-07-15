# PokePare

## Features
This website let's you search for a pokemon card via its name or image and find the prices for it on a number of selling websites.

# Installation

### Python 3

Install from : https://www.python.org/downloads/  
This app was built with Python 3.6.3

### Virtualenv and VirtualenvWrapper

```sh
pip install --user virtualenv
pip install --user virtualenvwrapper
```

#### Unix
After the installation it's time to add theses lines in ```~/.profile``` (maybe ```~/.bashrc``` or ```~/.bash_profile```)

```sh
export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
export PROJECT_HOME=~/pyprojects
mkdir -p $PROJECT_HOME
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.x
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source .local/bin/virtualenvwrapper.sh
```

And finally reload this file :

```sh 
source ~/.profile
```

# Requirements
## Running the virtual environment
After the virtual environment is setup, you can then work on it:
```sh
workon {your_env_name}
```

## Installing the dependencies
```sh
cd {project_folder_name} // e.g.: pokepare_project
pip install -r requirements.txt
```
or (Unix only) or using make for Windows: http://gnuwin32.sourceforge.net/packages/make.htm
```sh
cd {project_folder_name}
make init
```

# Running the app
```sh
cd {project_folder_name}
python manage.py runserver
```
or (Unix only)
```sh
cd {project_folder_name}
make run
```

# Frontend

> A Vue.js project

## Build Setup

``` bash
# change directory
cd frontend

# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# collect static files
cd .. # project root
make collectstatic
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

# Issues
## MAC OS X Issues
Remember to navigate to Applications/Python x.x (where x.x is your version) and double click on "Install Certificates.command" to install certificates


# TODO

* Add pokémon' names in french
* Add pokémon' names in japanese