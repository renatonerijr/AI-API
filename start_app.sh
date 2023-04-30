#!/bin/bash
echo alias shell="'ipython'" >> ~/.bashrc

python -m debugpy --listen 0.0.0.0:5678 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 5000
