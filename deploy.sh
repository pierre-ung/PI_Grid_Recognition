#!/bin/bash

# Pull the repository
git pull

# stop / rm the old running docker
echo -e $1 | sudo -S docker stop grid_reco_ctn
echo -e $1 | sudo -S docker rm grid_reco_ctn

# Generate the new docker image
echo -e $1 | sudo -S docker build --network=host . -t grid_reco_img

# Run the docker
echo -e $1 | sudo -S docker run -dp 50001:50001 --name grid_reco_ctn grid_reco_img
