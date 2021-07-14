#!/bin/bash

# Open browser
open http://localhost:5000

# Run Docker container
docker run -p 5000:5000 --name pyrate-stocks pyrate-stocks