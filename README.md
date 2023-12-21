# ICTFP

ADS-B -signal tracking software for Radarcape evo device. Docker environments with local installation. 

## Environment setup



### **Python 3.11 and [modules](./dependencies/python/requirements_versions.txt)**

#### <ins>**setting up python from source**</ins>
project has provided python source for project initialization. 
    
makefile: ``sudo make init_python``

    tar xvf Python-3.11.6.tgz
    cd Python-3.11.6
    ./configure --enable-optimizations --with-ensurepip=install
    make -j 8
    sudo make altinstall
    
#### <ins>**initializing virtual environment**</ins>
docker container uses python virtual environment for its bed to run python scripts. Dependencies will be installed to the virtual environment.

1) initialize virtual environment: **venv**

    ``make venv``
        
        VENV_NAME = venv
        python3.11 -m venv $(VENV_NAME)
    
2. install dependencies from local folder

    ``make install_dep``

        . $(VENV_NAME)/bin/activate; \
	    python3.11 -m pip install --upgrade dependencies/python/pip-23.3.2-py3-none-any.whl
	    . $(VENV_NAME)/bin/activate; \
	    python3.11 -m pip install dependencies/python/dep/whl/*.whl
    
note: after installation to check dependencies on virtual environment, You can check them via:

    # check installed dependencies
    source venv/bin/activate
    pip freeze > requirements.ts    

### **Docker & Docker-Compose**
* Docker - version: 24.0.7
* Docker-Compose - version : v2.23.3-desktop.2 

#### <ins>**install docker image from local file**</ins>

project provides zipped docker image for project.

1. install docker image

    ``make load_docker_image``

        gzip -dk dependencies/docker/docker-python:3.11-slim.tar.gz
	    docker load -i dependencies/docker/docker-python:3.11-slim.tar

2. build project into docker via docker-compose`

    ``docker-compose build``

3. start project via docker-compose up -d

    ``docker-compose up -d``


### [maptiles](https://tuni-my.sharepoint.com/:u:/g/personal/william_reima_tuni_fi/EZVX9gYZpuRMrGKKV-2XzB0B4PmgZY6YKw10YCrodbnlZg?e=eYb2fa)

Extract .zip to ./server/map

