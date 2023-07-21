#!/usr/bin/env python3

import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
from itertools import chain

from matplotlib.ticker import FormatStrFormatter

sys.path.append("../../include")
from draw_simple import *
import numpy as np
import math

job_tag = "final"
job_name = "paw-atm23-" + job_tag
input_path = "data/"
output_path = "draw/"
all_labels = ["name", "nbytes", "input_inject_rate(K/s)", "inject_rate(K/s)", "msg_rate(K/s)", "bandwidth(MB/s)"]

def plot(df, x_key, y_key, tag_key, title,
         filename = None, label_fn=None, with_error=True,
         x_label=None, y_label=None, draw_y_max=False):
    if title is None:
        title = filename
    if x_label is None:
        x_label = x_key
    if y_label is None:
        y_label = y_key

    df = df.sort_values(by=[tag_key, x_key])

    # fig, ax = plt.subplots(figsize=(15, 10))
    fig, ax = plt.subplots()
    lines = parse_tag(df, x_key, y_key, tag_key)
    # update labels
    if label_fn is not None:
        for line in lines:
            line["label"] = label_fn(line["label"])

    # Setup colors
    cmap_tab20=plt.get_cmap('tab20')
    ax.set_prop_cycle(color=[cmap_tab20(i) for i in chain(range(0, 20, 2), range(1, 20, 2))])

    ratio = 0.0
    for line in lines:
        for y, error in zip(line["y"], line["error"]):
            if error / y > ratio:
                ratio = error / y
    max_ratio = 0.6
    if ratio > max_ratio:
        errorbar_ratio = ratio / max_ratio
        for line in lines:
            line["error"] = [error / errorbar_ratio for error in line["error"]]
        ax.text(0.025, 0.95, "Errorbar ratio: %.2f" % errorbar_ratio, transform=ax.transAxes)
    # time
    for line in lines:
        if with_error:
            ax.errorbar(line["x"], line["y"], line["error"],
                        label=line["label"], marker='.',
                        markerfacecolor='white', capsize=3)
        else:
            ax.plot(line["x"], line["y"], label=line["label"], marker='.', markerfacecolor='white')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(title)
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    # ax.legend(bbox_to_anchor=(1.01, 1.01))
    ax.legend()
    ax.tick_params(axis='y', which='both', labelsize="small")
    ax.yaxis.set_minor_formatter(FormatStrFormatter("%.1f"))
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    plt.tight_layout()

    if filename is None:
        filename = title
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    dirname = os.path.join(output_path, job_name)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    output_png_name = os.path.join(dirname, "{}.png".format(filename))
    fig.savefig(output_png_name)
    output_json_name = os.path.join(dirname, "{}.json".format(filename))
    with open(output_json_name, 'w') as outfile:
        json.dump({"Time": lines}, outfile)

    if draw_y_max:
        fig, ax = plt.subplots()
        tags = []
        y_maxs = []
        for line in lines:
            tags.append(line["label"])
            y_maxs.append(max(line["y"]))
        bar = ax.barh(tags, y_maxs, edgecolor="black")
        for i, rect in enumerate(bar):
            text = f'{y_maxs[i]:.2f}'
            ax.text(y_maxs[i], rect.get_y() + rect.get_height() / 2.0,
                    text, ha='left', va='center')
        ax.set_title(title)
        ax.invert_yaxis()  # labels read top-to-bottom
        plt.tight_layout()

        output_png_name = os.path.join(dirname, "{}-bar.png".format(filename))
        fig.savefig(output_png_name)
        output_json_name = os.path.join(dirname, "{}-bar.json".format(filename))
        with open(output_json_name, 'w') as outfile:
            json.dump({"tags": tags, "y_maxs": y_maxs}, outfile)

def batch(df):
    def label_fn(label):
        return label\
            .replace("_putsendrecv", "_psr") \
            .replace("_sendrecv", "_sr") \
            .replace("_sendimm", "_i") \
            .replace("_queue", "_cq") \
            .replace("_sync", "_sy") \
            .replace("_rp", "_pin") \
            .replace("_worker", "_mt")

    def format_inject_rate(row):
        ratio = row["input_inject_rate(1/s)"] / 1e3 / row["inject_rate(K/s)"]
        if abs(1 - ratio) <= 0.05:
            return row["input_inject_rate(1/s)"] / 1e3
        else:
            return row["inject_rate(K/s)"]

    df["inject_rate(K/s)"] = df.apply(format_inject_rate, axis=1)
    draw_all = False
    # message rate
    df1_tmp = df[df.apply(lambda row:
                          row["nbytes"] == 8 and
                          row["nsteps"] == 1 and
                          (draw_all or
                           "sendimm" in row["name"]
                           or "mpi" in row["name"]
                           or row["name"] == "lci_putsendrecv_queue_rp"),
                          # row["input_inject_rate(K/s)"] != 0,
                          axis=1)]
    df1 = df1_tmp.copy()
    plot(df1, "inject_rate(K/s)", "msg_rate(K/s)", "name", "Message Rate (8B)",
         filename="message_rate-8", with_error=True, label_fn=label_fn,
         x_label="Achieved Injection Rate (K/s)", y_label="Achieved Message Rate (K/s)",
         draw_y_max=True)

    df2_tmp = df[df.apply(lambda row:
                          row["nbytes"] == 16384 and
                          row["nsteps"] == 1 and
                          (draw_all or
                           "sendimm" in row["name"]
                           or "mpi" in row["name"]
                           or row["name"] == "lci_putsendrecv_queue_rp"),
                          # row["input_inject_rate(K/s)"] != 0,
                          axis=1)]
    df2 = df2_tmp.copy()
    plot(df2, "inject_rate(K/s)", "msg_rate(K/s)", "name", "Message Rate (16KiB)",
         filename="message_rate-16384", with_error=True, label_fn=label_fn,
         x_label="Achieved Injection Rate (K/s)", y_label="Achieved Message Rate (K/s)",
         draw_y_max=True)

    # latency
    df3_tmp = df[df.apply(lambda row:
                          row["window"] == 1 and
                          row["nsteps"] > 1 and
                          (draw_all or
                           "sendimm" in row["name"]
                           or "mpi" in row["name"]
                           or row["name"] == "lci_putsendrecv_queue_rp"),
                          axis=1)]
    df3 = df3_tmp.copy()
    plot(df3, "nbytes", "latency(us)", "name", "Latency w/ Message Size",
         filename="latency", with_error=True, label_fn=label_fn,
         x_label="Message Size (byte)", y_label="Latency (us)")

    # window - latency
    df3_tmp = df[df.apply(lambda row:
                          row["nbytes"] == 8 and
                          row["nsteps"] > 1 and
                          (draw_all or
                           "sendimm" in row["name"]
                           or "mpi" in row["name"]
                           or row["name"] == "lci_putsendrecv_queue_rp"),
                          axis=1)]
    df3 = df3_tmp.copy()
    plot(df3, "window", "latency(us)", "name", "Latency w/ Window (8B)",
         filename="window-latency-8", with_error=True, label_fn=label_fn,
         x_label="Window Size", y_label="Latency (us)")

    df3_tmp = df[df.apply(lambda row:
                          row["nbytes"] == 16384 and
                          row["nsteps"] > 1 and
                          (draw_all or
                           "sendimm" in row["name"]
                           or "mpi" in row["name"]
                           or row["name"] == "lci_putsendrecv_queue_rp"),
                          axis=1)]
    df3 = df3_tmp.copy()
    plot(df3, "window", "latency(us)", "name", "Latency w/ Window (16KiB)",
         filename="window-latency-16384", with_error=True, label_fn=label_fn,
         x_label="Window Size", y_label="Latency (us)")

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, job_name + ".csv"))
    # interactive(df)
    batch(df)
