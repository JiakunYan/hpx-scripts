#!/bin/bash

echo "perf record --freq=99 --call-graph dwarf -q -o perf.data.$SLURM_JOB_ID.$SLURM_PROCID ${ROOT_PATH}/init/build/benchmarks/lcitb_pt2pt --op 2m --send-comp-type=sync --recv-comp-type=sync --nthreads 64 --thread-pin 1 --nsteps=1000 --min-msg-size=2048 --max-msg-size=2048"
perf record --freq=99 --call-graph dwarf -q -o perf.data.$SLURM_JOB_ID.$SLURM_PROCID ${ROOT_PATH}/init/build/bin/partitioned_vector_inclusive_scan_test --hpx:ini=hpx.parcel.lci.priority=1000 --hpx:ini=hpx.parcel.lci.enable=1 --hpx:ini=hpx.parcel.bootstrap=lci --hpx:threads=4 --hpx:localities=2