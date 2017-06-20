#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ensures Pi2 have the correct "overclocking" setting

from ansible.module_utils.basic import *
import re

from ansible.module_utils.common import RASPI_CONFIG_BIN, ConfigFile

CPU_INFO_PATH = "/proc/cpuinfo"

CPU_PI2 = "Pi2"

CPU_TYPES = "cpu_types"

CONFIG_OC_REGEXP = re.compile("set_overclock " + CPU_PI2 + " (?P<arm_freq>\d+) (?P<core_freq>\d+) (?P<sdram_freq>\d+) (?P<over_voltage>\d+)")


def read_oc_params():
    with open(RASPI_CONFIG_BIN) as fp:
        oc_config = CONFIG_OC_REGEXP.search(fp.read()).groupdict()
    return oc_config


def main():
    module = AnsibleModule(argument_spec={
        CPU_TYPES: {"required": True, "type": "dict"}
    }
    )

    pi2_cpu = module.params.get(CPU_TYPES)[CPU_PI2]

    is_pi2 = False

    with open(CPU_INFO_PATH) as fp:
        is_pi2 = any(x.find(pi2_cpu) > -1 for x in fp.readlines())

    if is_pi2:
        oc_config = read_oc_params()
        config_file = ConfigFile()
        for (param, value) in oc_config.iteritems():
            config_file.set(param, value)
        module.exit_json(changed=config_file.is_changed, msg="Is Pi2, ensured optimum CPU params.")
    else:
        module.exit_json(changed=False, msg="CPU chipset does not appear to be a Pi2 (but you can still custom-OC it by setting 'raspi_config_other_options!).")

main()