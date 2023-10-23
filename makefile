# Makefile to create a Python virtual environment and install requirements

# Name of the virtual environment
VENV_NAME = venv

# Path to requirements file
REQUIREMENTS = requirements.txt

# Create a virtual environment
venv:
	python3 -m venv $(VENV_NAME)

# Install requirements in the virtual environment
install:
	. $(VENV_NAME)/bin/activate; \
	python3 -m pip install --upgrade pip
	python3 -m pip install -r $(REQUIREMENTS)

# Clean up the virtual environment
clean:
	rm -rf $(VENV_NAME)

.PHONY: venv install clean
