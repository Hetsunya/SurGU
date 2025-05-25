#!/bin/bash

# Запуск backend
echo "Starting Backend..."
cd backend || exit
nohup go run main.go > backend.log 2>&1 &
cd ..

# Запуск frontend
echo "Starting Frontend..."
cd frontend || exit
nohup npm start > frontend.log 2>&1 &
cd ..

echo "All services started."
