from script_common import *
from platform_config_common import *
import subprocess

def get_default_config():
    default_config = {
        "griddim": 8,
        "zc_threshold": 8192,
        "name": "lci",
        "task": "rs",
        "parcelport": "lci",
        "max_level": 6,
        "protocol": "putva",
        "comp_type": "queue",
        "progress_type": "rp",
        "prg_thread_num": 1,
        "sendimm": 1,
        "backlog_queue": 0,
        "prepost_recv_num": 1,
        "zero_copy_recv": 1,
        "match_table_type": "hashqueue",
        "cq_type": "array_atomic_faa",
        "reg_mem": 1
    }
    return default_config


def get_theta(config):
    griddim = config["griddim"]
    if griddim >= 5:
        theta = 0.34
    elif 3 <= griddim <= 4:
        theta = 0.51
    elif griddim == 2:
        theta = 1.01
    else:
        print("invalid griddim {}!".format(griddim))
        exit(1)
    return theta


def get_nthreads(config):
    platform_config = get_platform_config()
    if config["parcelport"] == "lci" and "pthread" in config["progress_type"]:
        nthreads = platform_config["core_num"] - 1
    else:
        nthreads = platform_config["core_num"]
    return nthreads


def get_environ_setting(config):
    ret = {
        "LCI_SERVER_MAX_SENDS": "1024",
        "LCI_SERVER_MAX_RECVS": "4096",
        "LCI_SERVER_NUM_PKTS": "65536",
        "LCI_SERVER_MAX_CQES": "65536",
        "LCI_PACKET_SIZE": "12288",
    }
    if "match_table_type" in config:
        ret["LCI_MT_BACKEND"] = config["match_table_type"]
    if "cq_type" in config:
        ret["LCI_CQ_TYPE"] = config["cq_type"]
    if "reg_mem" in config and config["reg_mem"] or config["progress_type"] == "worker":
        ret["LCI_USE_DREG"] = "0"
    return ret


def load_module(config, build_type = "release", enable_pcounter = False, extra=None):
    module = get_module()
    module("purge")
    # Build type
    lci_to_load = "lci/local" + "-" + build_type
    # Performance counter
    if enable_pcounter:
        lci_to_load += "-pcounter"
    # Thread-safe progress function
    if config["parcelport"] == "lci" and \
       ("worker" in config["progress_type"] or
        config["progress_type"] == "rp" and config["prg_thread_num"] > 1):
        lci_to_load += "-safeprog"
    if lci_to_load == "lci/local-release":
        lci_to_load = "lci/local"
    module("load", "jemalloc")
    module("load", lci_to_load)
    if extra:
        for t in extra:
            module("load", t)


def get_hpx_cmd(executable, config):
    cmd = f'''{executable} \
--hpx:ini=hpx.stacks.use_guard_pages=0 \
--hpx:ini=hpx.parcel.{config["parcelport"]}.priority=1000 \
--hpx:ini=hpx.parcel.{config["parcelport"]}.zero_copy_serialization_threshold={config["zc_threshold"]} \
--hpx:threads={get_nthreads(config)} \
--hpx:ini=hpx.parcel.lci.protocol={config["protocol"]} \
--hpx:ini=hpx.parcel.lci.comp_type={config["comp_type"]} \
--hpx:ini=hpx.parcel.lci.progress_type={config["progress_type"]} \
--hpx:ini=hpx.parcel.lci.prg_thread_num={config["prg_thread_num"]} \
--hpx:ini=hpx.parcel.{config["parcelport"]}.sendimm={config["sendimm"]} \
--hpx:ini=hpx.parcel.lci.backlog_queue={config["backlog_queue"]} \
--hpx:ini=hpx.parcel.lci.prepost_recv_num={config["prepost_recv_num"]} \
--hpx:ini=hpx.parcel.zero_copy_receive_optimization={config["zero_copy_recv"]} \
--hpx:ini=hpx.parcel.lci.reg_mem={config["reg_mem"]}'''
    return cmd


def run_hpx(executable, config, extra_arguments="", timeout=None):
    os.environ.update(get_environ_setting(config))

    cmd = f'''
srun {get_srun_pmi_option(config)} numactl --interleave=all {get_hpx_cmd(executable, config)} {extra_arguments}
'''
    print(cmd)
    sys.stdout.flush()
    sys.stderr.flush()
    p = subprocess.Popen(cmd.split())
    try:
        p.wait(timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        print("Kill process due to timeout ({}s)".format(timeout))