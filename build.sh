#!/bin/bash

echo -e "\033[0;32mBuild new docker image\033[0m"
docker build --tag techtoolsregistry.azurecr.io/aznw-tools:latest .