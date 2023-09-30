#!/bin/bash

echo "start setup"

pip install -r ./requirements.txt

python3 ./setup.py

echo "setup complete"
