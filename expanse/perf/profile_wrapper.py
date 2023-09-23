#!/usr/bin/env python
import os
import sys
sys.path.append(f'{os.environ["HOME"]}/workspace/hpx-scripts/include')
from script_common_hpx import *
import json

# load configuration
config = get_default_config()
if len(sys.argv) > 1:
    config.update(json.loads(sys.argv[1]))
print("Config: " + json.dumps(config))

# set path
current_path = get_current_script_path()
root_path = os.path.realpath(os.path.join(current_path, "../.."))
os.environ["UCX_WARN_UNUSED_ENV_VARS"] = "n"

executable = os.path.realpath(os.path.join(os.environ["HOME"], "opt/hpx/local/build/bin/pingpong_performance2"))

# load modules
load_module(config, build_type="release")
module_list()

os.environ.update(get_environ_setting(config))
platform_config = get_platform_config_all()
numactl_cmd = ""
if platform_config["numa_policy"] == "interleave":
    numactl_cmd = "numactl --interleave=all"
perf_output = f'perf.data.{os.environ["SLURM_JOB_ID"]}.{os.environ["SLURM_PROCID"]}'
# pingpong_cmd = "--window=500000 --batch-size=100 --nbytes=8 --inject-rate=0"
pingpong_cmd = "--window=100000 --batch-size=10 --nbytes=16384 --inject-rate=0"
cmd = f'''
perf record --freq=10 --call-graph dwarf -q -o {perf_output} \
      {numactl_cmd} {get_hpx_cmd(executable, config)} \
      {pingpong_cmd} \
'''
print(cmd)
sys.stdout.flush()
sys.stderr.flush()
os.system(cmd)
# os.rename(f"{root_path}/data/{perf_output}", f"{current_path}/run/{perf_output}")