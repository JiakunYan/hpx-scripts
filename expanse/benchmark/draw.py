import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
sys.path.append("../../include")
from draw_simple import *
import numpy as np
import math

job_tag = "paper"
job_name = "20230712-" + job_tag
input_path = "data/"
all_labels = ["name", "nbytes", "input_inject_rate(K/s)", "inject_rate(K/s)", "msg_rate(K/s)", "bandwidth(MB/s)"]

def plot(df, x_key, y_key, tag_key, title, filename = None, label_fn=None, with_error=True):
    if title is None:
        title = filename

    df = df.sort_values(by=[tag_key, x_key])

    # fig, ax = plt.subplots(figsize=(15, 10))
    fig, ax = plt.subplots()
    lines = parse_tag(df, x_key, y_key, tag_key)
    # update labels
    if label_fn is not None:
        for line in lines:
            line["label"] = label_fn(line["label"])

    # time
    for line in lines:
        if with_error:
            line["error"] = [0 if math.isnan(x) else x for x in line["error"]]
            ax.errorbar(line["x"], line["y"], line["error"], label=line["label"], marker='.', markerfacecolor='white', capsize=3)
        else:
            ax.plot(line["x"], line["y"], label=line["label"], marker='.', markerfacecolor='white')
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(title)
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    # ax.legend(bbox_to_anchor=(1.01, 1.01))
    ax.legend()
    plt.tight_layout()

    if filename is None:
        filename = title
    dirname = os.path.join("draw", job_name)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    output_png_name = os.path.join(dirname, "{}.png".format(filename))
    fig.savefig(output_png_name)
    output_json_name = os.path.join(dirname, "{}.json".format(filename))
    with open(output_json_name, 'w') as outfile:
        json.dump({"Time": lines}, outfile)

def draw_bar(df, x_key, y_keys, title, x_include=None, color_map=None, filename=None, label_fn=None):
    if type(y_keys) != list:
        y_keys = [y_keys]

    if x_include:
        xs = list(x_include)
    else:
        xs = list(df[x_key].unique())

    ys_dict = {}
    # errors_dict = {}
    colors_dict = {}
    for y_key in y_keys:
        ys = []
        # errors = []
        colors = []
        for x in xs:
            y = df[df[x_key] == x].max(numeric_only=True)[y_key]
            # error = df[df[x_key] == x].std(numeric_only=True)[y_key]
            if y is np.nan:
                continue
            if y == 0:
                continue
            ys.append(float(y))
            # errors.append(float(error))
            if color_map:
                colors.append(color_map[x])
        ys_dict[y_key] = ys
        # errors_dict[y_key] = errors
        colors_dict[y_key] = colors

    # update labels
    if label_fn is not None:
        xs = list(map(label_fn, xs))

    fig, ax = plt.subplots()
    # fig, ax = plt.subplots(figsize=(10, len(xs) * 0.3 + 1))
    bottom = np.zeros(len(xs))

    bar = None
    for y_key in y_keys:
        if colors_dict[y_key]:
            bar = ax.barh(xs, ys_dict[y_key], color=colors_dict[y_key], edgecolor="black", left=bottom)
        else:
            bar = ax.barh(xs, ys_dict[y_key], edgecolor="black", left=bottom)
        bottom += ys_dict[y_key]

    # Add actual number to the bar
    for i, rect in enumerate(bar):
        text = []
        total = 0
        for y_key in y_keys:
            total += ys_dict[y_key][i]
            text.append(f'{ys_dict[y_key][i]:.2f}')
        if len(text) > 1:
            text.append(f'{total:.2f}')
        text = "/".join(text)
        ax.text(bottom[i], rect.get_y() + rect.get_height() / 2.0,
                text, ha='left', va='center')
    ax.set_title(title)
    ax.invert_yaxis()  # labels read top-to-bottom
    plt.tight_layout()

    if filename is None:
        filename = title
    dirname = os.path.join("draw", job_name)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    output_png_name = os.path.join(dirname, "{}.png".format(filename))
    fig.savefig(output_png_name)
    output_json_name = os.path.join(dirname, "{}.json".format(filename))
    with open(output_json_name, 'w') as outfile:
        # json.dump({"xs": xs, "ys": ys_dict, "errors": errors_dict}, outfile)
        json.dump({"xs": xs, "ys": ys_dict}, outfile)

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
    # df["tag"] = np.where((df["parcelport"] == "lci") & (df["tag"] == "default"), "default-numa", df["tag"])
    # df["tag"] = np.where((df["parcelport"] == "lci") & (df["tag"] == "numalocal"), "default", df["tag"])
    df["inject_rate(K/s)"] = df["inject_rate(K/s)"].apply(int)
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
    plot(df1, "inject_rate(K/s)", "msg_rate(K/s)", "name", "message_rate-8", with_error=True, label_fn=label_fn)
    draw_bar(df1, "name", "msg_rate(K/s)", "message_rate-8-bar", label_fn=label_fn)

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
    plot(df2, "inject_rate(K/s)", "msg_rate(K/s)", "name", "message_rate-16384", with_error=True, label_fn=label_fn)
    draw_bar(df2, "name", "msg_rate(K/s)", "message_rate-16384-bar", label_fn=label_fn)

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
    plot(df3, "nbytes", "latency(us)", "name", "latency", with_error=True, label_fn=label_fn)

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
    plot(df3, "window", "latency(us)", "name", "window-latency-8", with_error=True, label_fn=label_fn)

    df3_tmp = df[df.apply(lambda row:
                          row["nbytes"] == 16384 and
                          row["nsteps"] > 1 and
                          (draw_all or
                           "sendimm" in row["name"]
                           or "mpi" in row["name"]
                           or row["name"] == "lci_putsendrecv_queue_rp"),
                          axis=1)]
    df3 = df3_tmp.copy()
    plot(df3, "window", "latency(us)", "name", "window-latency-16384", with_error=True, label_fn=label_fn)

    # df3_tmp = df[df.apply(lambda row:
    #                       row["nbytes"] == 65536 and
    #                       row["nsteps"] > 1 and
    #                       ("sendimm" in row["name"] or "mpi" in row["name"]),
    #                       axis=1)]
    # df3 = df3_tmp.copy()
    # plot(df3, "window", "latency(us)", "name", "window-latency-65536", with_error=True)

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, job_name + ".csv"))
    # interactive(df)
    batch(df)
