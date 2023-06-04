#!/bin/bash
#SBATCH --partition=jenkins-compute
#SBATCH --time=00:00:30
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --job-name=hpx-test
#SBATCH --output=slurm_output.%x-o%j
#SBATCH --error=slurm_output.%x-o%j

# setup module environment
module purge
module load gcc

PATH_TO_EXE=${1:-./init/build}

cd ${PATH_TO_EXE}/bin
time ./hpxrun.py ./hello_world_distributed -l 2 -t 2 -p lci -r mpi