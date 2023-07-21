import os, sys

if "CMD_WLM_CLUSTER_NAME" in os.environ and os.environ["CMD_WLM_CLUSTER_NAME"] == "expanse" or \
        "SLURM_CLUSTER_NAME" in os.environ and os.environ["SLURM_CLUSTER_NAME"] == "expanse":
    from platforms.platform_config_expanse import *
elif "HOSTNAME" in os.environ and "rostam" in os.environ["HOSTNAME"] or \
        "SLURM_CLUSTER_NAME" in os.environ and os.environ["SLURM_CLUSTER_NAME"] == "rostam":
    from platforms.platform_config_rostam import *
elif "HOSTNAME" in os.environ and "delta" in os.environ["HOSTNAME"] or \
        "SLURM_CLUSTER_NAME" in os.environ and os.environ["SLURM_CLUSTER_NAME"] == "delta":
    from platforms.platform_config_delta import *
else:
    print("Unknown plaform!")
    exit(1)


def get_platform_config(key, required=False):
    config = get_platform_config_all()
    if key in config:
        ret = config[key]
    else:
        ret = None
    if required and ret is None:
        print("platform_config: key {} is required but got None!".format(key))
        exit(1)
    return ret
