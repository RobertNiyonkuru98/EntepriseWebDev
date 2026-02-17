#!/bin/bash

# Test the API
echo "Testing Standard Trips Endpoint..."
curl "http://127.0.0.1:5001/api/trips?borough=Manhattan&limit=10"
echo -e "\n\nTesting Manual Algorithm (Top Fares)..."
curl "http://127.0.0.1:5001/api/top_fares?borough=Queens"