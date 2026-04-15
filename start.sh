#!/bin/bash

# Start FastAPI backend in the background
echo "Starting FastAPI backend..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait briefly to let the backend process initialize before frontend tries to connect
echo "Waiting for backend to initialize..."
sleep 3

# Start Streamlit frontend in the foreground
# Render uses the $PORT environment variable for web services
echo "Starting Streamlit frontend..."
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
