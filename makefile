# Makefile to create a Python virtual environment and install requirements

# Name of the virtual environment
VENV_NAME = venv

# Name of used Python Version
PYTHON_VERSION = Python-3.11.6

# Path to requirements file
PYTHON_REQUIREMENTS = dependencies/python/requirements_versions.txt

# Directory containing the .tar.gz files
PYTHON_DEPENDENCIES = dependencies/python/dep

# Directory containing extracted dependecies
DEPENDENCY_FOLDER = dependencies/python/dep/lib/

load_docker_image:
	gzip -dk dependencies/docker/docker-python:3.11-slim.tar.gz
	docker load -i dependencies/docker/docker-python:3.11-slim.tar

# install python from source
init_python: 
	tar xvf dependencies/python/Python-3.11.6.tgz
	cd Python-3.11.6 && \
	./configure --enable-optimizations --with-ensurepip=install && \
	make -j 8 && \
	make altinstall

# Create a virtual environment
venv:
	python3.11 -m venv $(VENV_NAME)

# Install requirements to the virtual environment from local packages
install_dep:
	. $(VENV_NAME)/bin/activate; \
	python3.11 -m pip install --upgrade dependencies/python/pip-23.3.1.tar.gz
	. $(VENV_NAME)/bin/activate; \
	python3.11 -m pip install dependencies/python/dep/whl/*.whl

# NEEDS CONNECTION - dowload wheels for every python dependency
download_packages:
	@while read -r line || [[ -n "$$line" ]]; do \
		echo "$$line"; \
        pip download --only-binary :all: "$$line" --force-reinstall --dest $(PYTHON_DEPENDENCIES)/whl; \
    done < $(PYTHON_REQUIREMENTS);

# Clean up the virtual environment
clean:
	rm -rf $(VENV_NAME)

.PHONY: init_python venv install_dep install_local_dep download_packages clean
