#!/bin/bash
#SBATCH --qos=benchmark
#SBATCH --account=xpress_g
#SBATCH --constraint=gpu
#SBATCH --gpus=4
#SBATCH --time=2:00:00
#SBATCH --nodes=2
#SBATCH --job-name=test
#SBATCH --output=slurm_output.%x-o%j
#SBATCH --error=slurm_error.%x-o%j

# setup module environment
export CC=gcc
export CXX=g++

PATH_TO_EXE=$(realpath "${1:-./init/build/}")

cd ${PATH_TO_EXE}
time make tests -j
time ctest --verbose --timeout 300