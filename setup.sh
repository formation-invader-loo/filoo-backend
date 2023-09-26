#!/bin/bash

echo "start setup"

pip install -r ./requirements.txt

python ./setup.py

echo "setup complete"
