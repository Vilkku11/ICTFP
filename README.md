# ICTFP

ADS-B -signal tracking software for Radarcape evo device. Docker environments with local installation. 

## Versions and dependencies

### **Docker**

### **Docker-compose**

### **Python 3.11**
    



### [maptiles](https://tuni-my.sharepoint.com/:u:/g/personal/william_reima_tuni_fi/EZVX9gYZpuRMrGKKV-2XzB0B4PmgZY6YKw10YCrodbnlZg?e=eYb2fa)

Extract .zip to ./server/map


## python 
makefile: ``make init_python``

```
tar xvf Python-3.11.6.tgz
cd Python-3.11.6
./configure --enable-optimizations --with-ensurepip=install
make -j 8
sudo make altinstall
```

## python virtual environment
makefile: 
1. ``make venv``

    ```
    python3.11 -m venv $(VENV_NAME)
    ```

2.  install dependencies to virtual environment

    A) ``make install_local``

    ```
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
    ```

    B) ``make install``

    ```
    . $(VENV_NAME)/bin/activate; \
	python3 -m pip install --upgrade pip
	python3 -m pip install -r $(REQUIREMENTS)
    ```




