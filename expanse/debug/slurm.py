#!/usr/bin/env python
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
    "prg_thread_num": 1,
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "match_table_type": "hashqueue",
}

configs = [
    baseline,
    {**baseline, "progress_type": "worker"}
]

# set path
current_path = get_current_script_path()
executable = os.path.realpath(os.path.join(os.environ["HOME"], "opt/hpx/local/build/bin/pingpong_performance2"))

os.environ["UCX_WARN_UNUSED_ENV_VARS"] = "n"

for config in configs:
    # load modules
    load_module(config, build_type="release", enable_pcounter=0)
    # module_list()
    print(config)

    # inject_rates = [1e5, 2e5, 4e5, 8e5, 16e5, 0]
    inject_rates = [0]
    for inject_rate in inject_rates:
        run_hpx(executable, config, extra_arguments=f"--window=500000 --batch-size=100 --nbytes=8 --inject-rate={int(inject_rate)}")

    # inject_rates = [1e4, 2e4, 4e4, 8e4, 16e4, 32e4, 0]
    # # inject_rates = [16e4, 32e4]
    # window = 1e5
    # # if config["name"] == "mpi_sendimm":
    # #     window = 1e4
    # for inject_rate in inject_rates:
    #     run_hpx(executable, config,
    #             extra_arguments=f"--window={int(window)} --batch-size=10 --nbytes=16384 --inject-rate={int(inject_rate)}")
