#!/usr/bin/env python3

import os
import sys
import shutil
import copy
import json
sys.path.append("../../include")
from script_common import *

baseline = {
    "name": "lci",
    "zc_threshold": 8192,
    "parcelport": "lci",
    "protocol": "putsendrecv",
    "comp_type": "queue",
    "progress_type": "rp",
    "prg_thread_num": "auto",
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 0,
    "ndevices": 2,
    "ncomps": 2,
}

configs = [
    {**baseline, "name": "lci", "parcelport": "lci"},
    {**baseline, "name": "mpi", "parcelport": "mpi", "sendimm": 0},
    {**baseline, "name": "mpi_i", "parcelport": "mpi", "sendimm": 1},
    {**baseline, "name": "lci_wo_i", "sendimm": 0},
    {**baseline, "name": "lci_sendrecv", "protocol": "sendrecv"},
    {**baseline, "name": "lci_sync", "comp_type": "sync"},
    # {**baseline, "name": "lci_worker_d1", "ndevices": 1, "progress_type": "worker"},
    # {**baseline, "name": "lci_worker_d4", "ndevices": 4, "progress_type": "worker"},
    # {**baseline, "name": "lci_rp_d1", "ndevices": 1, "progress_type": "rp"},
    # {**baseline, "name": "lci_rp_d2", "ndevices": 2, "progress_type": "rp"},
    # {**baseline, "name": "lci_rp_d4", "ndevices": 4, "progress_type": "rp"},
    # {**baseline, "name": "mpi", "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "lci_sr_sy_mt", "protocol": "sendrecv", "comp_type": "sync",
    #  "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_sr_sy_pin", "protocol": "sendrecv", "comp_type": "sync", "sendimm": 0},
    # {**baseline, "name": "lci_sr_cq_mt", "protocol": "sendrecv", "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_sr_cq_pin", "protocol": "sendrecv", "sendimm": 0},
    # {**baseline, "name": "lci_psr_sy_mt", "protocol": "putsendrecv", "comp_type": "sync",
    #  "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_psr_sy_pin", "protocol": "putsendrecv", "comp_type": "sync", "sendimm": 0},
    # {**baseline, "name": "lci_psr_cq_mt", "protocol": "putsendrecv", "progress_type": "worker",
    #  "sendimm": 0},
    # {**baseline, "name": "lci_psr_cq_pin", "protocol": "putsendrecv", "sendimm": 0},
    # {**baseline, "name": "mpi_i", "parcelport": "mpi"},
    # {**baseline, "name": "lci_sr_sy_mt_i", "protocol": "sendrecv", "comp_type": "sync",
    #  "progress_type": "worker"},
    # {**baseline, "name": "lci_sr_sy_pin_i", "protocol": "sendrecv", "comp_type": "sync"},
    # {**baseline, "name": "lci_sr_cq_mt_i", "protocol": "sendrecv", "progress_type": "worker"},
    # {**baseline, "name": "lci_sr_cq_pin_i", "protocol": "sendrecv"},
    # {**baseline, "name": "lci_psr_sy_mt_i", "protocol": "putsendrecv", "comp_type": "sync",
    #  "progress_type": "worker"},
    # {**baseline, "name": "lci_psr_sy_pin_i", "protocol": "putsendrecv", "comp_type": "sync"},
    # {**baseline, "name": "lci_psr_cq_mt_i", "protocol": "putsendrecv", "progress_type": "worker"},
    # {**baseline, "name": "lci_psr_cq_pin_i", "protocol": "putsendrecv"},
]

if __name__ == "__main__":
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    mkdir_s("./run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    for i in range(n):
        for config in configs:
            run_slurm(tag, 2, config, time = "5:00")