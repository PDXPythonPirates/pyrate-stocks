#!/bin/bash

# Stop running Docker container
docker stop $(docker ps -q)
