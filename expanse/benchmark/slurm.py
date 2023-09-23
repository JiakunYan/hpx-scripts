#!/usr/bin/env python
import os
import sys

sys.path.append("../../include")
from script_common_hpx import *
import json
import time

start_time = time.time()
# load configuration
config = get_default_config()
if len(sys.argv) > 1:
    config.update(json.loads(sys.argv[1]))
print("Config: " + json.dumps(config))

# set path
current_path = get_current_script_path()
hpx_master_branch = "local"
if "special_branch" in config:
    hpx_master_branch = config["special_branch"]
executable = os.path.realpath(os.path.join(os.environ["HOME"], f"opt/hpx/{hpx_master_branch}/build/bin/pingpong_performance2"))

os.environ["UCX_WARN_UNUSED_ENV_VARS"] = "n"

# load modules
load_module(config, build_type="release", enable_pcounter=0)
module_list()

run_all = False
if "run_all" in config and config["run_all"]:
    run_all = True

# latency
# msg_sizes = [8, 64, 512, 4096, 32768, 262144]
# for msg_size in msg_sizes:
#     run_hpx(executable, config, extra_arguments=f"--window=1 --batch-size=1 --nbytes={int(msg_size)} --nsteps=10000")

if run_all:
    windows = [1, 2, 4, 8, 16, 32, 64, 128]
else:
    windows = [128]
for window in windows:
    run_hpx(executable, config, extra_arguments=f"--window={int(window)} --batch-size=1 --nbytes=8 --nsteps=10000")

for window in windows:
    run_hpx(executable, config, extra_arguments=f"--window={int(window)} --batch-size=1 --nbytes=16384 --nsteps=10000")

# # message rate
if run_all:
    inject_rates = [1e5, 2e5, 4e5, 8e5, 16e5, 32e5, 0]
else:
    inject_rates = [0]
for inject_rate in inject_rates:
    run_hpx(executable, config, extra_arguments=f"--window=500000 --batch-size=100 --nbytes=8 --inject-rate={int(inject_rate)}")

if run_all:
    inject_rates = [2e4, 4e4, 8e4, 16e4, 32e4, 64e4, 0]
else:
    inject_rates = [0]
# inject_rates = [5e4, 6e4, 7e4, 9e4, 10e4, 12e4, 14e4]
window = 1e5
for inject_rate in inject_rates:
    run_hpx(executable, config,
            extra_arguments=f"--window={int(window)} --batch-size=10 --nbytes=16384 --inject-rate={int(inject_rate)}")

end_time = time.time()
print("Executed 1 configs. Total time is {}s.".format(end_time - start_time))
