import os, sys

if os.environ["CMD_WLM_CLUSTER_NAME"] == "expanse":
    from platforms.platform_config_expanse import *
else:
    print("Unknown plaform!")
    exit(1)