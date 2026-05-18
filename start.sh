#!/bin/bash

# Start FastAPI backend in the background
echo "Starting FastAPI backend..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait briefly to let the backend process initialize before frontend tries to connect
echo "Waiting for backend to initialize..."
sleep 3

# Start Next.js frontend in the foreground
# Next.js automatically uses the $PORT environment variable
echo "Starting Next.js frontend..."
cd frontend
npm run build
npm start
