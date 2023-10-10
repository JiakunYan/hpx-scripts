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
    "in_buffer_assembly": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 1,
    "ndevices": 4,
    "ncomps": 1,
    "run_all": 0
}

configs = [
    # # MPI v.s. LCI
    # {**baseline, "name": "lci", "run_all": 1, "parcelport": "lci"},
    # # {**baseline, "name": "mpi", "run_all": 1, "parcelport": "mpi", "sendimm": 0},
    # # {**baseline, "name": "mpi_i", "run_all": 1, "parcelport": "mpi", "sendimm": 1},
    # # other variants
    # {**baseline, "name": "lci_sendrecv", "protocol": "sendrecv"},
    # {**baseline, "name": "lci_sync", "comp_type": "sync"},
    # # ndevices + progress_type
    # # {**baseline, "name": "lci_mt_d1_c1", "ndevices": 1, "progress_type": "worker", "ncomps": 1},
    # # {**baseline, "name": "lci_mt_d2_c1", "ndevices": 2, "progress_type": "worker", "ncomps": 1},
    # # {**baseline, "name": "lci_mt_d4_c1", "ndevices": 4, "progress_type": "worker", "ncomps": 1},
    # {**baseline, "name": "lci_mt_d8_c1", "ndevices": 8, "progress_type": "worker", "ncomps": 1},
    # # {**baseline, "name": "lci_pin_d1_c1", "ndevices": 1, "progress_type": "rp", "ncomps": 1},
    # # {**baseline, "name": "lci_pin_d2_c1", "ndevices": 2, "progress_type": "rp", "ncomps": 1},
    # # {**baseline, "name": "lci_pin_d4_c1", "ndevices": 4, "progress_type": "rp", "ncomps": 1},
    # {**baseline, "name": "lci_pin_d8_c1", "ndevices": 8, "progress_type": "rp", "ncomps": 1},
    # # # ncomps
    # # {**baseline, "name": "lci_mt_d4_c2", "ndevices": 4, "progress_type": "worker", "ncomps": 2},
    # # {**baseline, "name": "lci_mt_d4_c4", "ndevices": 4, "progress_type": "worker", "ncomps": 4},
    # # {**baseline, "name": "lci_pin_d4_c2", "ndevices": 4, "progress_type": "rp", "ncomps": 2},
    # # {**baseline, "name": "lci_pin_d4_c4", "ndevices": 4, "progress_type": "rp", "ncomps": 4},
    # # # Upper-layer
    # {**baseline, "name": "lci_wo_i", "sendimm": 0},
    {**baseline, "name": "lci_alock_wo_i", "special_branch": "ipdps_nohack1", "sendimm": 0},
    # {**baseline, "name": "lci", "parcelport": "lci"},
    # {**baseline, "name": "lci_alock", "special_branch": "ipdps_nohack1"},
    # # {**baseline, "name": "lci_tlock", "special_branch": "ipdps_nohack2"},
    # # {**baseline, "name": "lci_atlock", "special_branch": "ipdps_nohack12"},
    # {**baseline, "name": "lci_agas_caching", "agas_caching": 1},
    # # Memory Registration
    # # {**baseline, "name": "lci_worker_cache", "ndevices": 1, "progress_type": "rp", "reg_mem": 1, "mem_reg_cache": 1},
    # # {**baseline, "name": "lci_prg_cache", "ndevices": 1, "progress_type": "rp", "reg_mem": 0, "mem_reg_cache": 1},
    # # {**baseline, "name": "lci_worker_nocache", "ndevices": 1, "progress_type": "rp", "reg_mem": 1, "mem_reg_cache": 0},
    # # {**baseline, "name": "lci_prg_nocache", "ndevices": 1, "progress_type": "rp", "reg_mem": 0, "mem_reg_cache": 0},
    # # Memory Copy
    # {**baseline, "name": "lci_wo_in_buffer", "parcelport": "lci", "in_buffer_assembly": 0},
    # {**baseline, "name": "lci_wo_zc_recv", "parcelport": "lci", "zero_copy_recv": 0},
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