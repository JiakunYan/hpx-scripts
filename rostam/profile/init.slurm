#!/bin/bash
#SBATCH --partition=jenkins-compute
#SBATCH --time=2:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --job-name=hpx-init
#SBATCH --output=init/slurm_output.%x-o%j
#SBATCH --error=init/slurm_error.%x-o%j

# exit when any command fails
set -e
# import the the script containing common functions
source ../../include/scripts.sh

# get the HPX source path via environment variable or default value
HPX_SOURCE_PATH=$(realpath "${HPX_SOURCE_PATH:-../../../hpx}")
LCI_SOURCE_PATH=$(realpath "${LCI_SOURCE_PATH:-../../../LC}")
# autofetch LCI, no need to export LCI_ROOT
# LCI_ROOT=$(realpath "${LCI_ROOT:-../../external/lci-install-dbg}")
# export LCI_ROOT=${LCI_ROOT}

if [[ -f "${HPX_SOURCE_PATH}/libs/full/include/include/hpx/hpx.hpp" ]]; then
  echo "Found HPX at ${HPX_SOURCE_PATH}"
else
  echo "Did not find HPX at ${HPX_SOURCE_PATH}!"
  exit 1
fi

# create the ./init directory
mkdir -p ./init
# move to ./init directory
cd init

# setup module environment
module purge
module load gcc
module load cmake
module load boost
module load hwloc
module load openmpi
module load papi
module load python
export CC=gcc
export CXX=g++

# record build status
record_env

mkdir -p log
mv *.log log

# build HPX
mkdir -p build
cd build
echo "Running cmake..."
HPX_INSTALL_PATH=$(realpath "../install")
cmake -GNinja \
      -DCMAKE_INSTALL_PREFIX=${HPX_INSTALL_PATH} \
      -DHPX_WITH_PARALLEL_TESTS_BIND_NONE=ON \
      -DCMAKE_BUILD_TYPE=Debug \
      -DHPX_WITH_CHECK_MODULE_DEPENDENCIES=ON \
      -DHPX_WITH_CXX_STANDARD=17 \
      -DHPX_WITH_MALLOC=system \
      -DHPX_WITH_FETCH_ASIO=ON \
      -DHPX_WITH_COMPILER_WARNINGS=ON \
      -DHPX_WITH_COMPILER_WARNINGS_AS_ERRORS=ON \
      -DHPX_WITH_PARCELPORT_MPI=ON \
      -DHPX_WITH_PARCELPORT_LCI=ON \
      -DHPX_WITH_FETCH_LCI=ON \
      -DHPX_WITH_PARCELPORT_LCI_BACKEND=ibv \
      -L \
      ${HPX_SOURCE_PATH} | tee init-cmake.log 2>&1 || { echo "cmake error!"; exit 1; }
#      -DHPX_WITH_FETCH_ASIO=ON \
#      -DFETCHCONTENT_SOURCE_DIR_LCI=${LCI_SOURCE_PATH} \
cmake -LAH . >> init-cmake.log
echo "Running make..."
ninja partitioned_vector_inclusive_scan_test | tee init-make.log 2>&1 || { echo "make error!"; exit 1; }
echo "Installing HPX to ${HPX_INSTALL_PATH}"
mkdir -p ${HPX_INSTALL_PATH}
ninja install > init-install.log 2>&1 || { echo "install error!"; exit 1; }
mv *.log ../log