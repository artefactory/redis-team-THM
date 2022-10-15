#!/bin/bash

# start redis-vector-db
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4