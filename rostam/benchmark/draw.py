import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
sys.path.append("../../include")
from draw_simple import *
import numpy as np
import math
from itertools import chain

job_name = "20230916-all"
input_path = "data/"
output_path = "draw/"
all_labels = ["name", "nbytes", "input_inject_rate(K/s)", "inject_rate(K/s)", "msg_rate(K/s)", "bandwidth(MB/s)"]

def plot(df, x_key, y_key, tag_key, title,
         filename = None, base = None, smaller_is_better = True, label_fn=None,
         with_error=True, x_label=None, y_label=None):
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

    # time
    for line in lines:
        if with_error:
            line["error"] = [0 if math.isnan(x) else x for x in line["error"]]
            ax.errorbar(line["x"], line["y"], line["error"], label=line["label"], marker='.', markerfacecolor='white', capsize=3)
        else:
            ax.plot(line["x"], line["y"], label=line["label"], marker='.', markerfacecolor='white')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(title)
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    # ax.legend(bbox_to_anchor=(1.01, 1.01))

    # speedup
    baseline = None
    ax2 = None
    speedup_lines = None
    for line in lines:
        if base == line["label"]:
            baseline = line
            break
    if baseline:
        ax2 = ax.twinx()
        speedup_lines = []
        for line in lines:
            if line['label'] == baseline['label']:
                ax2.plot(line["x"], [1 for x in range(len(line["x"]))], linestyle='dashed')
                continue
            if smaller_is_better:
                speedup = [float(x) / float(b) for x, b in zip(line["y"], baseline["y"])]
                label = "{} / {}".format(line['label'], baseline['label'])
            else:
                speedup = [float(b) / float(x) for x, b in zip(line["y"], baseline["y"])]
                label = "{} / {}".format(baseline['label'], line['label'])
            speedup_lines.append({"label": line["label"], "x": line["x"], "y": speedup})
            ax2.plot(line["x"], speedup, label=label, marker='.', markerfacecolor='white', linestyle='dashed')
        ax2.set_ylabel("Speedup")
    # ax2.legend()

    # ask matplotlib for the plotted objects and their labels
    if ax2:
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc=0)
    else:
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
    fig.savefig(output_png_name, bbox_inches='tight')
    output_json_name = os.path.join(dirname, "{}.json".format(filename))
    with open(output_json_name, 'w') as outfile:
        json.dump({"Time": lines, "Speedup": speedup_lines}, outfile)

def batch(df):
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
                           row["name"] in ["mpi", "mpi_i", "lci"]),
                          axis=1)]
    df1 = df1_tmp.copy()
    plot(df1, "inject_rate(K/s)", "msg_rate(K/s)", "name", "Message Rate (8B)",
         filename="message_rate-8", base="lci", smaller_is_better=False, with_error=True,
         x_label="Achieved Injection Rate (K/s)", y_label="Achieved Message Rate (K/s)")
    # draw_bar(df1, "name", "msg_rate(K/s)", "Maximum Message Rate (8B)", filename="message_rate-8-bar", label_fn=label_fn)

    df2_tmp = df[df.apply(lambda row:
                          row["nbytes"] == 16384 and
                          row["nsteps"] == 1 and
                          (draw_all or
                           row["name"] in ["mpi", "mpi_i", "lci"]),
                          axis=1)]
    df2 = df2_tmp.copy()
    plot(df2, "inject_rate(K/s)", "msg_rate(K/s)", "name", "Message Rate (16KiB)",
         filename="message_rate-16384", base="lci", smaller_is_better=False, with_error=True,
         x_label="Achieved Injection Rate (K/s)", y_label="Achieved Message Rate (K/s)")
    # draw_bar(df2, "name", "msg_rate(K/s)", "Maximum Message Rate (16KiB)", filename="message_rate-16384-bar", label_fn=label_fn)

    # window - latency
    df3_tmp = df[df.apply(lambda row:
                          row["nbytes"] == 8 and
                          row["nsteps"] > 1 and
                          (draw_all or
                           row["name"] in ["mpi", "mpi_i", "lci"]),
                          axis=1)]
    df3 = df3_tmp.copy()
    plot(df3, "window", "latency(us)", "name", "Latency w/ Window (8B)",
         filename="window-latency-8", base="lci", with_error=True,
         x_label="Window Size", y_label="Latency (us)")

    df3_tmp = df[df.apply(lambda row:
                          row["nbytes"] == 16384 and
                          row["nsteps"] > 1 and
                          (draw_all or
                           row["name"] in ["mpi", "mpi_i", "lci"]),
                          axis=1)]
    df3 = df3_tmp.copy()
    plot(df3, "window", "latency(us)", "name", "Latency w/ Window (16KiB)",
         filename="window-latency-16384", base="lci", with_error=True,
         x_label="Window Size", y_label="Latency (us)")

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, job_name + ".csv"))
    # interactive(df)
    batch(df)
