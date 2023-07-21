def get_platform_config_all():
    return {
        "name": "rostam",
        "core_num": 40,
        "numa_policy": "default",
        "account": None,
        "partition": "medusa",
        "octotiger_major": "master",
        "module_init_file": "/usr/share/lmod/lmod/init/env_modules_python.py"
    }

def get_srun_pmi_option(config):
    return "--mpi=pmix"