#!/bin/bash
#SBATCH --partition=jenkins-compute
#SBATCH --time=15:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=profile
#SBATCH --output=slurm_output.%x-o%j
#SBATCH --error=slurm_error.%x-o%j

srun --mpi=pmi2 bash ${ROOT_PATH}/profile_wrapper.sh