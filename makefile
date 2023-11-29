# Makefile to create a Python virtual environment and install requirements

# Name of the virtual environment
VENV_NAME = venv

# Path to requirements file
REQUIREMENTS = requirements.txt

# Directory containing the .tar.gz files
directory_path="dependencies/"

# install python from source
init_python: 
	tar xvf Python-3.11.6.tgz
	cd Python-3.11.6 && \
	./configure --enable-optimizations --with-ensurepip=install && \
	make -j 8 && \
	sudo make altinstall

# Create a virtual environment
venv:
	python3.11 -m venv $(VENV_NAME)

# Install requirements in the virtual environment
install:
	. $(VENV_NAME)/bin/activate; \
	python3 -m pip install --upgrade pip
	python3 -m pip install -r $(REQUIREMENTS)

install_local:
	. $(VENV_NAME)/bin/activate; \
	if [ ! -d "$(directory_path)" ]; then \
        echo "Directory not found."; \
        exit 1; \
    fi; \
    cd "$(directory_path)" || exit; \
    for f in *.tar.gz; do \
        echo "Installing $$f..."; \
        python3 -m pip install "$$f"; \
    done; \
    echo "Installation complete."

# Clean up the virtual environment
clean:
	rm -rf $(VENV_NAME)

.PHONY: init_python venv install install_local clean
