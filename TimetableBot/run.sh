#!/bin/bash

python ./download_page.py &
python ./polling.py
