#!/bin/bash
set -e

echo "Starting backend..."
uvicorn backend.main:app --reload &
BACKEND_PID=$!

echo "Starting frontend..."

# if [ ! -d "node_modules" ]; then
#  echo "Installing frontend dependencies..."
#  npm install
# fi

npm --prefix frontend run dev &
FRONTEND_PID=$!

# Trap exit signals to clean up
cleanup() {
    echo "Stopping backend and frontend..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    sleep 1s
    exit
}

trap cleanup SIGINT SIGTERM EXIT

sleep 2s

open -a "Safari" http://localhost:5173

wait $BACKEND_PID $FRONTEND_PID