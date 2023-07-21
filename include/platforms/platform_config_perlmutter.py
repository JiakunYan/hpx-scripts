def get_platform_config_all():
    return {
        "name": "perlmutter",
        "core_num": 64,
        "numa_policy": "default",
    }

def get_srun_pmi_option(config):
    srun_pmi_option = "--mpi=pmix"
    return srun_pmi_option