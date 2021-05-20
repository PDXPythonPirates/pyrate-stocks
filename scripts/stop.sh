#!/bin/bash

echo "Stopping Docker container ..." 
docker stop $(docker ps -q)
