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

executable = os.path.realpath(os.path.join(os.environ["HOME"], "opt/hpx/local-release-pcounter/build/bin/pingpong_performance2"))

# load modules
load_module(config, build_type="release")
module_list()

perf_output = f'perf.data.{os.environ["SLURM_JOB_ID"]}.{os.environ["SLURM_PROCID"]}'
cmd = f'''
perf record --freq=10 --call-graph dwarf -q -o {perf_output} \
      numactl --interleave=all {get_hpx_cmd(executable, config)} \
      --window=500000 --batch-size=100 --nbytes=8 --inject-rate=0 \
'''
print(cmd)
sys.stdout.flush()
sys.stderr.flush()
os.system(cmd)
# os.rename(f"{root_path}/data/{perf_output}", f"{current_path}/run/{perf_output}")