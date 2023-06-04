import os
import sys
import shutil
import copy
import glob
import json

def rm(dir):
    try:
        shutil.rmtree(dir)
        print(f"Directory {dir} has been deleted successfully.")
    except OSError as e:
        print(f"Error: {dir} : {e.strerror}")

def mkdir_s(dir):
    if os.path.exists(dir):
        prompt = "{} directory exists. Are you sure to remove it | continue with it | or abort? [r|c|A]".format(dir)
        print(prompt)
        x = input()
        if x == "r":
            print("Remove {}".format(dir))
            rm(dir)
        elif x == "c":
            print("Continue with previous work")
        else:
            print("Abort")
            sys.exit(1)

    if not os.path.exists(dir):
        os.mkdir(dir)

def getenv_or(key, default):
    if key in os.environ:
        return os.environ[key]
    else:
        return default

def get_current_script_path():
    if "CURRENT_SCRIPT_PATH" in os.environ:
        return os.environ["CURRENT_SCRIPT_PATH"]
    else:
        return os.path.realpath(sys.argv[0])

def get_module():
    module_home = os.environ["MODULESHOME"]
    module_init_file_path = os.path.join(module_home, "init", "*.py")
    init_files = glob.glob(module_init_file_path)
    if len(init_files) != 1:
        print("Cannot find init file {}".format(init_files))
    print("Load init file {}".format(init_files[0]))
    dir_name = os.path.dirname(init_files[0])
    file_name = os.path.basename(init_files[0])
    name = os.path.splitext(file_name)[0]
    if dir_name not in sys.path:
        sys.path.insert(0, dir_name)
    module = getattr(__import__(name, fromlist=["module"]), "module")
    return module

def module_list():
    os.system("module list")

def run_slurm(tag, nnodes, config, time="00:05:00"):
    if config is None:
        config = {"name": "default"}
    job_name="n{}-{}".format(nnodes, config["name"])
    output_filename = "./run/slurm_output.{}.%x.j%j.out".format(tag)
    command = f'''
    sbatch --export=ALL \
           --nodes={nnodes} \
           --job-name={job_name} \
           --output={output_filename} \
           --error={output_filename} \
           --account=uic193 \
           --partition=compute \
           --time={time} \
           --ntasks-per-node=1 \
           slurm.py '{json.dumps(config)}'
    '''
    os.system(command)