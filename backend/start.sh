#!/bin/bash

uvicorn api:app --host 0.0.0.0 --port 8080 --workers 4