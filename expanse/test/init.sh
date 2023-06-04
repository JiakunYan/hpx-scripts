#!/bin/bash

# exit when any command fails
set -e
# import the the script containing common functions
source ../../include/scripts.sh

mkdir_s ./init
sbatch ./init.slurm