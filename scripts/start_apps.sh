#!/bin/bash

# Kill specific Python processes related to your Flask apps using pkill with specific patterns
echo # blank line
echo "Stopping specific python flask applications..."

echo "Stopping: 3000 - Hello world app..."
pkill -f 'flask run --host=0.0.0.0 -p 3000'  # Kill the Flask app on port 3000
sleep 1  # Wait for 1 second to receive the "terminate" signal

echo "Stopping: 4000 - Second app..."
pkill -f 'flask run --host=0.0.0.0 -p 4000'  # Kill the second app on port 4000
sleep 1  # Wait for 1 second to receive the "terminate" signal

echo "Stopping: 5000 - Third app..."
pkill -f 'flask run --host=0.0.0.0 -p 5000'  # Kill the Flask app on port 5000 - third app
sleep 1  # Wait for 1 second to receive the "terminate" signal

echo "Stopping: 7000 - API..."
pkill -f 'flask run --host=0.0.0.0 -p 7000'  # Kill the Flask app on port 7000 - api
sleep 1  # Wait for 1 second to receive the "terminate" signal

echo "Stopping: 9000 - Manager App..."
pkill -f 'flask run --host=0.0.0.0 -p 9000'
sleep 1  # Wait for 1 second to receive the "terminate" signal

# Restart the Flask apps
echo # blank line
echo "Starting Flask applications..."

echo "Starting: 3000 - first app..."
cd ~/flask_app && nohup flask run --host=0.0.0.0 -p 3000 > flask_app_nohup.out 2>&1 &
sleep 1  # Optional wait after starting each app for stability

echo "Starting: 4000 - second app..."
cd ~/decode_me && nohup flask run --host=0.0.0.0 -p 4000 > second_app.out 2>&1 &
sleep 1  # Optional wait after starting each app for stability


echo "Starting: 5000 - third app..."
cd ~/ibama-web && nohup flask run --host=0.0.0.0 -p 5000 > third_app_nohup.out 2>&1 &
sleep 1

echo "Starting: 7000 - API..."
cd ~/my-api && nohup flask run --host=0.0.0.0 -p 7000 > manager_nohup.out 2>&1 &
sleep 1

echo "Starting: 9000 - Manager App..."
cd ~/manager && nohup flask run --host=0.0.0.0 -p 9000 > manager_nohup.out 2>&1 &
sleep 1

# Return to the home directory
cd ~

echo # blank line
echo "======================================================================================="
echo "Started flask_app:3000, second:5000, api:7000, manager:9000"
echo "======================================================================================="
echo # blank line

