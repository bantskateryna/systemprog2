#!/bin/bash

docker build -t text-tools .
docker run -it --rm -v "$(pwd)":/app text-tools
