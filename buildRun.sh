#!/bin/bash

echo -e "\033[0;32mBuild new docker image\033[0m"
docker build --tag techtoolsregistry.azurecr.io/aznw-tools:latest .

echo -e "\033[0;32mRun New Container\033[0m"
docker run -it -d -p 8080:80 --name aznw-tools techtoolsregistry.azurecr.io/aznw-tools:latest