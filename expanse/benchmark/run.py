#!/usr/bin/env python

import os
import sys
import shutil
import copy
import json
sys.path.append("../../include")
from script_common import *

baseline = {
    "name": "lci_psr_cq_pin_i",
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
    "reg_mem": 1,
    "ndevices": 2,
    "ncomps": 2,
}

configs = [
    # MPI v.s. LCI
    {**baseline, "name": "lci", "parcelport": "lci"},
    # {**baseline, "name": "mpi", "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi_i", "parcelport": "mpi", "sendimm": 1},
    # other variants
    {**baseline, "name": "lci_wo_i", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv", "protocol": "sendrecv"},
    # {**baseline, "name": "lci_sync", "comp_type": "sync"},
    # {**baseline, "name": "lci_worker_d1", "ndevices": 1, "progress_type": "worker"},
    # {**baseline, "name": "lci_worker_d4", "ndevices": 4, "progress_type": "worker"},
    # {**baseline, "name": "lci_rp_d1", "ndevices": 1, "progress_type": "rp"},
    # {**baseline, "name": "lci_rp_d2", "ndevices": 2, "progress_type": "rp"},
    # {**baseline, "name": "lci_rp_d4", "ndevices": 4, "progress_type": "rp"},
    # old
    # {**baseline, "name": "mpi", "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_sync_worker", "protocol": "sendrecv", "comp_type": "sync",
    #  "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_sync_rp", "protocol": "sendrecv", "comp_type": "sync", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_queue_worker", "protocol": "sendrecv", "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_queue_rp", "protocol": "sendrecv", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_sync_worker", "protocol": "putsendrecv", "comp_type": "sync",
    #  "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_sync_rp", "protocol": "putsendrecv", "comp_type": "sync", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_queue_worker", "protocol": "putsendrecv", "progress_type": "worker",
    #  "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_queue_rp", "protocol": "putsendrecv", "sendimm": 0},
    # {**baseline, "name": "mpi_sendimm", "parcelport": "mpi"},
    # {**baseline, "name": "lci_sendrecv_sync_worker_sendimm", "protocol": "sendrecv", "comp_type": "sync",
    #  "progress_type": "worker"},
    # {**baseline, "name": "lci_sendrecv_sync_rp_sendimm", "protocol": "sendrecv", "comp_type": "sync"},
    # {**baseline, "name": "lci_sendrecv_queue_worker_sendimm", "protocol": "sendrecv", "progress_type": "worker"},
    # {**baseline, "name": "lci_sendrecv_queue_rp_sendimm", "protocol": "sendrecv"},
    # {**baseline, "name": "lci_putsendrecv_sync_worker_sendimm", "protocol": "putsendrecv", "comp_type": "sync",
    #  "progress_type": "worker"},
    # {**baseline, "name": "lci_putsendrecv_sync_rp_sendimm", "protocol": "putsendrecv", "comp_type": "sync"},
    # {**baseline, "name": "lci_putsendrecv_queue_worker_sendimm", "protocol": "putsendrecv", "progress_type": "worker"},
    # {**baseline, "name": "lci_putsendrecv_queue_rp_sendimm", "protocol": "putsendrecv"},
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
            run_slurm(tag, 2, config, time = "10:00")