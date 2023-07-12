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

cmd = f'''
cd {current_path}/run || exit 1
srun {get_srun_pmi_option(config)} {current_path}/profile_wrapper.py '{json.dumps(config)}'
'''
os.system(cmd)
