#!/bin/bash

# start redis-vector-db
# python load_data.py

uvicorn api:app --host 0.0.0.0 --port 8080 --workers 4