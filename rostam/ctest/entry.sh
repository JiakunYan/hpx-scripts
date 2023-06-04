#!/bin/bash -l

# Copyright (c) 2020 ETH Zurich
#
# SPDX-License-Identifier: BSL-1.0
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

# Make undefined variables errors, print each command
set -eux

# Clean up old artifacts
rm -f ./jenkins-hpx* ./*-Testing

configuration_name=gcc-10
build_type=debug
GIT_BRANCH=tmp
HPX_SOURCE_PATH=$(realpath "${HPX_SOURCE_PATH:-../../../hpx-lci-pool}")
LCI_SOURCE_PATH=$(realpath "${LCI_SOURCE_PATH:-../../../LC}")
export configuration_name build_type GIT_BRANCH HPX_SOURCE_PATH LCI_SOURCE_PATH
mkdir -p log

export configuration_name_with_build_type="${configuration_name}-${build_type,,}"

source ${HPX_SOURCE_PATH}/.jenkins/lsu/slurm-configuration-${configuration_name}.sh

if [[ -z "${ghprbPullId:-}" ]]; then
    # Set name of branch if not building a pull request
    export git_local_branch=$(echo ${GIT_BRANCH} | cut -f2 -d'/')
    job_name="jenkins-hpx-${git_local_branch}-${configuration_name_with_build_type}"

    if [[ "${git_local_branch}" == "master" ]]; then
        export install_hpx=1
    else
        export install_hpx=0
    fi
else
    job_name="jenkins-hpx-${ghprbPullId}-${configuration_name_with_build_type}"

    # Cancel currently running builds on the same branch, but only for pull
    # requests
    scancel --verbose --verbose --verbose --verbose --jobname="${job_name}"

    export install_hpx=0
fi

# delay things for a random amount of time
#sleep $[(RANDOM % 10) + 1].$[(RANDOM % 10)]s

# Start the actual build
set +e
sbatch \
    --verbose --verbose --verbose --verbose \
    --job-name="${job_name}" \
    --nodes="${configuration_slurm_num_nodes}" \
    --partition="${configuration_slurm_partition}" \
    --time="03:00:00" \
    --output="log/jenkins-hpx-${configuration_name_with_build_type}.out" \
    --error="log/jenkins-hpx-${configuration_name_with_build_type}.err" \
    ./batch.sh

## Print slurm logs
#echo "= stdout =================================================="
#cat jenkins-hpx-${configuration_name_with_build_type}.out
#
#echo "= stderr =================================================="
#cat jenkins-hpx-${configuration_name_with_build_type}.err
