#!/bin/bash

# Start FastAPI backend in the background
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend in the foreground
# Render uses the $PORT environment variable for web services
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
