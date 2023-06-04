#!/usr/bin/env python
import os
import sys

sys.path.append("../../include")
from script_common_hpx import *
import json

# load configuration
config = get_default_config()
if len(sys.argv) > 1:
    config.update(json.loads(sys.argv[1]))
print("Config: " + json.dumps(config))

# set path
current_path = get_current_script_path()
executable = os.path.realpath(os.path.join(os.environ["HOME"], "opt/hpx/local/build/bin/pingpong_performance2"))

os.environ["UCX_WARN_UNUSED_ENV_VARS"] = "n"

# load modules
load_module(config, build_type="release", enable_pcounter=0)
module_list()

# latency
# msg_sizes = [8, 64, 512, 4096, 32768, 262144]
# for msg_size in msg_sizes:
#     run_hpx(executable, config, extra_arguments=f"--window=1 --batch-size=1 --nbytes={int(msg_size)} --nsteps=10000")

# windows = [1, 2, 4, 8, 16, 32, 64]
# for window in windows:
#     run_hpx(executable, config, extra_arguments=f"--window={int(window)} --batch-size=1 --nbytes=8 --nsteps=10000")
#
# for window in windows:
#     run_hpx(executable, config, extra_arguments=f"--window={int(window)} --batch-size=1 --nbytes=16384 --nsteps=10000")

# for window in windows:
#     run_hpx(executable, config, extra_arguments=f"--window={int(window)} --batch-size=1 --nbytes=65536 --nsteps=5000")

# # message rate
# inject_rates = [1e5, 2e5, 4e5, 8e5, 16e5, 0]
# for inject_rate in inject_rates:
#     run_hpx(executable, config, extra_arguments=f"--window=500000 --batch-size=100 --nbytes=8 --inject-rate={int(inject_rate)}")
#
# inject_rates = [1e4, 2e4, 4e4, 8e4, 16e4, 32e4, 64e4, 0]
inject_rates = [5e4, 6e4, 7e4, 9e4, 10e4, 12e4, 14e4]
window = 1e5
# if config["name"] == "mpi_sendimm":
#     window = 1e4
for inject_rate in inject_rates:
    run_hpx(executable, config,
            extra_arguments=f"--window={int(window)} --batch-size=10 --nbytes=16384 --inject-rate={int(inject_rate)}")
