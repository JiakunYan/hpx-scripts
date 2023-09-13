import json
import re
import glob
import numpy as np
import ast
import pandas as pd
import os,sys

name = "20230909-basic"
input_path = "run-{}/slurm_output.*".format(name)
output_path = "data/"
line_patterns = [
{
    "format": "Config: (.+)",
    "label": ["config"],
},
{
    "format": ".*--window=(\d+).*",
    "label": ["window"]
},
{
    "format": ".*--inject-rate=(\d+).*",
    "label": ["input_inject_rate(K/s)"]
},
{
    "format": "nbytes=(\S+)",
    "label": ["nbytes"]
},
{
    "format": "latency\(us\)=(\S+)",
    "label": ["latency(us)"]
},
{
    "format": "inject_rate\(K/s\)=(\S+)",
    "label": ["inject_rate(K/s)"]
},
{
    "format": "msg_rate\(K/s\)=(\S+)",
    "label": ["msg_rate(K/s)"]
},
{
    "format": "bandwidth\(MB/s\)=(\S+)",
    "label": ["bandwidth(MB/s)"]
},
{
    "format": "nsteps=(\d+)",
    "label": ["nsteps"]
},]
all_labels = [y for x in line_patterns for y in x["label"]]

def get_typed_value(value):
    if value == '-nan':
        return np.nan
    try:
        typed_value = ast.literal_eval(value)
    except:
        typed_value = value
    return typed_value

if __name__ == "__main__":
    filenames = glob.glob(input_path)

    df = None
    state = "init"
    current_entry = dict()
    print("{} files in total".format(len(filenames)))
    for filename in filenames:
        current_entry = dict()

        with open(filename) as f:
            for line in f.readlines():
                line = line.strip()
                for i, pattern in enumerate(line_patterns):
                    m = re.match(pattern["format"], line)
                    if m:
                        if i == 0:
                            current_entry = {}

                        current_data = [get_typed_value(x) for x in m.groups()]
                        current_label = pattern["label"]
                        for label, data in zip(current_label, current_data):
                            if label == "config":
                                current_entry.update(data)
                            else:
                                current_entry[label] = data

                        if i == len(line_patterns) - 1:
                            print(current_entry)
                            new_df = pd.DataFrame(current_entry, columns=list(current_entry.keys()), index=[1])
                            if df is None:
                                df = new_df
                            else:
                                df = pd.concat([df, new_df], ignore_index=True)

    # df = df[all_labels]
    # df = df.sort_values(by=all_labels)
    # Sort dataframe
    name_ordering = [
        # new
        "lci",
        "mpi",
        "mpi_i",
        "lci_wo_i",
        "lci_sendrecv",
        "lci_sync",
        "lci_worker_d1",
        "lci_worker_d4",
        "lci_rp_d1",
        "lci_rp_d2",
        "lci_rp_d4",
        # baseline,
        # "lci",
        # "mpi",
        # "mpi_i",
        # "lci_sr_sy_mt",
        # "lci_sr_sy_pin",
        # "lci_sr_cq_mt",
        # "lci_sr_cq_pin",
        # "lci_psr_sy_mt",
        # "lci_psr_sy_pin",
        # "lci_psr_cq_mt",
        # "lci_psr_cq_pin",
        # "lci_sr_sy_mt_i",
        # "lci_sr_sy_pin_i",
        # "lci_sr_cq_mt_i",
        # "lci_sr_cq_pin_i",
        # "lci_psr_sy_mt_i",
        # "lci_psr_sy_pin_i",
        # "lci_psr_cq_mt_i",
        # "lci_psr_cq_pin_i",
        # # pthread
        # "lci_sr_sy_pthread",
        # "lci_sr_cq_pthread",
        # "lci_sr_sy_pthread_i",
        # "lci_sr_cq_pthread_i",
        # "lci_psr_sy_pthread",
        # "lci_psr_sy_pthread_i",
        # "lci_psr_cq_pthread",
        # "lci_psr_cq_pthread_i",
        # # putva
        # "lci_putva_sy_mt",
        # "lci_putva_sy_mt_i",
        # "lci_putva_cq_mt_i",
        # "lci_putva_cq_pin_i",
        # # backlog queue
        # "lci_sr_sy_mt_bq",
        # "lci_sr_sy_mt_i_bq",
        # "lci_psr_cq_pin_i_bq",
        # # 2 devices
        # "lci_putva_cq_mt_i_2dev",
        # "lci_putva_cq_pin_i_2dev",
        # # prepost receives
        # "lci_sr_sy_mt_post8",
        # "lci_sr_cq_mt_post8",
        # "lci_sr_sy_mt_i_post8",
        # "lci_sr_cq_mt_i_post8",
        # # No zero-copy receives
        # "mpi_nozcr",
        # "lci_psr_cq_pin_i_nozcr",
        # # Match table
        # "lci_sr_sy_mt_i_hash",
        # "lci_psr_cq_mt_i_hash",
        # "lci_sr_sy_mt_i_mqueue",
        # "lci_psr_cq_mt_i_mqueue",
        # "lci_sr_sy_pin_i_hash",
        # "lci_psr_cq_pin_i_hash",
        # "lci_sr_sy_pin_i_mqueue",
        # "lci_psr_cq_pin_i_mqueue",
        # # Others
        # "lci_putva_sy_pthread",
        # "lci_putva_sy_pin",
        # "lci_putva_sy_pthread_i",
        # "lci_putva_sy_pin_i",
        # "lci_putva_cq_mt",
        # "lci_putva_cq_pthread",
        # "lci_putva_cq_pin",
        # "lci_putva_cq_pthread_i",
    ]
    df["name"] = pd.Categorical(df["name"], name_ordering)
    df = df.sort_values(by=["name", "inject_rate(K/s)"])

    if df.shape[0] == 0:
        print("Error! Get 0 entries!")
        exit(1)
    else:
        print("get {} entries".format(df.shape[0]))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    df.to_csv(os.path.join(output_path, "{}.csv".format(name)))