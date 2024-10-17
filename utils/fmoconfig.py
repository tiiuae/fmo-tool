import os
import yaml
import json

from typing import Dict, List
from utils.misc import eprint
from utils.fmoconfig_schema import FMO_Schema


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FMOConfig_Manager(object, metaclass=Singleton):
    __schema = None
    __valid = False
    __config_path_rw = ""
    __config_path_ro = ""
    __ddp_path_wo = ""

    __DPF = "dynamic-portforwarding-service"
    __DDP = "fmo-dynamic-device-passthrough"
    __MON = "monitoring-service"

    def __init__(self, config_path_ro: str, config_path_rw: str, __ddp_path_wo: str):
        self.__valid = False
        self.__schema = None
        self.__config_path_rw = config_path_rw
        self.__config_path_ro = config_path_ro
        self.__ddp_path_wo = __ddp_path_wo

        try:
            with open(config_path_rw) as yaml_conifg:
                config = yaml.load(yaml_conifg, Loader=yaml.SafeLoader)
                self.__valid, self.__schema = self.__verify_config(config)
                return
        except Exception as e:
            eprint("Can't open store file due to error: ", e.args)

        eprint("Trying to open original one")
        with open(config_path_ro) as yaml_conifg:
            config = yaml.load(yaml_conifg, Loader=yaml.SafeLoader)
            self.__valid, self.__schema = self.__verify_config(config)

    def __verify_config(self, config: Dict):
        # if empty
        if not config:
            return False, None

        try:
            schema = FMO_Schema(config)
        except Exception as e:
            eprint("Validation error, log: ", e)
            return False, None

        return True, schema

    def is_valid(self) -> bool:
        return self.__valid

    def get_config(self) -> Dict:
        return self.__schema.get_config()

    def save_config(self) -> None:
        config = self.__schema.get_config()
        os.makedirs(os.path.dirname(self.__config_path_rw), exist_ok=True)
        with open(self.__config_path_rw, "w") as yaml_config:
            yaml.dump(config, yaml_config)
        # Whenever fmo-config changed, rewrite ddp config
        self.write_vmddp_config()

    def write_vmpf_config(self, vmname: str, pfconfig: List[Dict]) -> None:
        # TODO: this one need to be read from fmo-config.yaml
        vms_pf_configs = {
            'netvm': '/var/netvm/netconf/dpf.config',
        }
        if vmname not in vms_pf_configs:
            eprint(f"no valid dpf.config paths for {vmname}")
            return

        rules = []
        for n, config in enumerate(pfconfig):
            sip = config.get("sip", self.get_system_ip())
            dip = config.get("dip")
            sport = config.get("sport")
            dport = config.get("dport")
            proto = config.get("proto")
            rules.append(f"{sip} {sport} {dport} {dip} {proto}")

        with open(vms_pf_configs[vmname], "w") as f:
            f.write("\n".join(rules))
            f.flush()
            os.fsync(f)

    def restore_config(self) -> None:
        import shutil
        shutil.copy(self.__config_path_ro, self.__config_path_rw)

    def get_system_ip(self) -> str:
        return self._get_system_config().get("ipaddr", "")

    def set_system_ip(self, ip: str) -> str:
        self._get_system_config()["ipaddr"] = ip

    def get_system_alias(self) -> str:
        return self._get_system_config().get("alias", "")

    def set_system_alias(self, alias: str) -> None:
        self._get_system_config()["alias"] = alias

    def get_system_RAversion(self) -> str:
        return self._get_system_config().get("RAversion", "")

    def get_system_defaultGW(self) -> str:
        return self._get_system_config().get("defaultGW", "")

    def set_system_defaultGW(self, gw: str) -> None:
        self._get_system_config()["defaultGW"] = gw

    def get_system_dockerCR(self) -> str:
        return self._get_system_config().get("dockerCR", "")

    def set_system_dockerCR(self, cr: str) -> None:
        self._get_system_config()["dockerCR"] = cr

    def get_system_release(self) -> str:
        return self.__schema.get("release", "")

    def get_system_name(self) -> str:
        return self.__schema.get("name", "")

    def get_vms_names_list(self) -> List[str]:
        return list(self._get_vms())

    def get_vmdci_enabled(self, vmname: str) -> bool:
        return self._get_vmdci(vmname).get("enable", False)

    def get_vmportforwarding_enabled(self, vmname: str) -> bool:
        return self._get_vmportforwarding(vmname).get("enable", False)

    def set_vmportforwarding_enabled(self, vmname: str, enable: bool):
        self._get_vmportforwarding(vmname)["enable"] = enable

    def get_vmddp_enabled(self, vmname: str) -> bool:
        return self._get_vmddp_config(vmname).get("enable", False)

    def set_vmddp_enabled(self, vmname: str, enable: bool):
        self._get_vmddp_config(vmname)["enable"] = enable

    def get_vm_ip(self, vmname: str) -> str:
        return self._get_vmconfig(vmname).get("ipaddr", "NA")

    def is_vm_exist(self, vmname: str) -> bool:
        vms_list = self.get_vms_names_list()
        if vms_list is None:
            return False
        return vmname in self.get_vms_names_list()

    def get_vmconfig(self, vmname: str) -> Dict:
        return self._get_vmconfig(vmname).get_config()

    # TODO: hormonize names: vmdpf_conif
    def get_vmportforwarding(self, vmname: str) -> Dict:
        return self._get_vmportforwarding(vmname).get_config()

    def set_vmportforwarding(self, vmname: str, newconf: Dict):
        config = self._get_vmportforwarding(vmname)

        for k in newconf.keys():
            config[k] = newconf[k]

    def get_vmddp_config(self, vmname: str) -> Dict:
        return self._get_vmddp_config(vmname).get_config()

    def set_vmddp_config(self, vmname: str, newconf: Dict):
        config = self._get_vmddp_config(vmname)

        for k in newconf.keys():
            config[k] = newconf[k]

    def write_vmddp_config(self) -> None:
        vmlist = self.get_vms_names_list()
        vmddplist = []
        for vmname in vmlist:
            dpconfig = self._get_vmddp_config(vmname).get_config()
            try:
                if (dpconfig.get("enable",False)):
                    devicelist = dpconfig.get("devices", [])
                    for device in devicelist:
                        device["vendorId"]=device.pop("vendorid")
                        device["productId"]=device.pop("productid")
                    vmddplist.append({'name': vmname, 'qmpSocket': '/var/lib/microvms/'+vmname+'/'+vmname+'.sock', 'usbPassthrough': devicelist})
            except Exception as e:
                continue
        vhotplugconf = {"vms": vmddplist }
        os.makedirs(os.path.dirname(self.__ddp_path_wo), exist_ok=True)
        with open(self.__ddp_path_wo, "w") as ddp_config:
            json.dump(vhotplugconf, ddp_config)

# ############################
# # Internal usage functions #
# ############################

    def _get_system_config(self) -> FMO_Schema:
        return self.__schema["fmo-system"]

    def _get_vms(self) -> FMO_Schema:
        return self.__schema["vms"]

    def _get_vmconfig(self, vmname: str) -> FMO_Schema:
        return self._get_vms()[vmname]

    def _get_vmextramodules(self, vmname: str) -> FMO_Schema:
        return self._get_vmconfig(vmname)["extraModules"]

    def _get_vmextramodules_services(self, vmname: str) -> FMO_Schema:
        return self._get_vmextramodules(vmname)["services"]

    def _get_vmportforwarding(self, vmname: str) -> FMO_Schema:
        return self._get_vmextramodules_services(vmname)[self.__DPF]

    def _get_vmddp_config(self, vmname: str) -> FMO_Schema:
        return self._get_vmextramodules_services(vmname)[self.__DDP]

    def _get_vmdci(self, vmname: str) -> FMO_Schema:
        return self._get_vmextramodules_services(vmname)["fmo-dci"]


def get_fmoconfig_manager() -> FMOConfig_Manager:
    manager = FMOConfig_Manager("/etc/fmo-config.yaml",
                                "/var/host/fmo-config.yaml",
                                "/var/host/vmddp.conf")
    if not manager.is_valid():
        eprint("Config is not valid")
        raise Exception("Config is not valid")
    return manager
