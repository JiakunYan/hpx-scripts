#!/usr/bin/env python3
import os
import sys

sys.path.append("../../include")
from script_common_hpx import *
import json

# # load configuration
# config = get_default_config()
# if len(sys.argv) > 1:
#     config.update(json.loads(sys.argv[1]))
# print("Config: " + json.dumps(config))

baseline = {
    "name": "lci",
    "zc_threshold": 8192,
    "parcelport": "lci",
    "protocol": "putsendrecv",
    "comp_type": "queue",
    "progress_type": "rp",
    "prg_thread_num": "auto",
    "sendimm": 0,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 0,
    "ndevices": 2,
    "ncomps": 2
}

configs = [
    baseline
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

# set path
current_path = get_current_script_path()
# executable = os.path.realpath(os.path.join(os.environ["HOME"], "opt/hpx/local-release-pcounter/build/bin/pingpong_performance2"))

os.environ["UCX_WARN_UNUSED_ENV_VARS"] = "n"
# os.environ["LCI_LOG_LEVEL"] = "trace"
# os.environ["LCT_PCOUNTER_RECORD_INTERVAL"] = "10000" # record every 10 ms

for config in configs:
    # load modules
    load_module(config, build_type="release", enable_pcounter=False)
    module_list()
    print(config)
    executable = os.path.realpath(os.path.join(os.environ["HOME"], "opt/hpx/local/build/bin/pingpong_performance2"))

    # os.environ["LCT_PCOUNTER_AUTO_DUMP"] = "run/pcounter.8b.{}.log.%".format(config["name"])
    run_hpx(executable, config, extra_arguments=f"--window=500000 --batch-size=100 --nbytes=8 --inject-rate=0")
    # os.environ["LCT_PCOUNTER_AUTO_DUMP"] = "run/pcounter.16kb.{}.log.%".format(config["name"])
    # run_hpx(executable, config, extra_arguments=f"--window=100000 --batch-size=10 --nbytes=16384 --inject-rate=0")