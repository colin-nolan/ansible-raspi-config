#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ensures the given config value is set.

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.common import ConfigFile

CONFIG_VALS = "config_vals"


def main():
    module = AnsibleModule(argument_spec={
        CONFIG_VALS: {"required": True, "type": "dict"}
    })

    config_vals = module.params.get(CONFIG_VALS)

    config = ConfigFile()

    out = ""
    err = ""

    # sanitize from auto-typing in YAML
    config_vals = dict((str(key), str(val)) for (key, val) in config_vals.items())

    for key, val in config_vals.items():
        try:
            modified = config.set(key, val)
            if modified:
                out += "\nModified "+key+" to "+val
            else:
                out += "\n"+key+" was already set to "+val
        except Exception as e:
            err = "Error when writing config: "+str(e)
            module.fail_json(changed=config.is_changed, msg=err, stdout=out, stderr=err)

    module.exit_json(changed=config.is_changed, stdout=out, stderr=err)


main()