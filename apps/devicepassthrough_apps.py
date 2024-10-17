import typer
import os

from enum import Enum
from utils.ssh import ssh_vm_helper
from utils.misc import print_config, eprint
from utils.utils import get_ctx_if_vm_exist
from utils.fmoconfig import get_fmoconfig_manager

from typing_extensions import Annotated


app = typer.Typer()

SEVICE_NAME = "fmo-dynamic-device-passthrough-service"

class DP_Proto(str, Enum):
    usb = "usb"
    pcie = "pcie"


@app.command("config")
def get_dp_config(
    vmname: Annotated[str, typer.Argument(help="VM name to print config")],
) -> None:
    """
    Print VM DDP config
    """
    ctx = get_ctx_if_vm_exist(vmname)
    pfconfig = ctx.get_vmddp_config(vmname)

    if not pfconfig:
        eprint(f"vm ddp config: '{vmname}' not found")
        raise typer.Exit(code=-1)

    print(print_config(pfconfig))

@app.command("generate")
def generate_dp_config(
) -> None:
    """
    Generate VM DDP config
    """
    ctx = get_fmoconfig_manager()
    ctx.write_vmddp_config()

@app.command("add")
def add_dp_rules(
    vmname: Annotated[str, typer.Argument(help="VM name to print rules")],

    productid: Annotated[str, typer.Option("--productid", "-p")],
    vendorid: Annotated[str, typer.Option("--vendorid", "-v")],
    bus: Annotated[DP_Proto, typer.Option("--bus", "-b")] = "usb",
) -> None:
    """
    Add a new VM DDP rule
    """
    ctx = get_ctx_if_vm_exist(vmname)
    dpconfig = ctx.get_vmddp_config(vmname)
    configuration = dpconfig.get("devices", [])
    enabled = dpconfig.get("enable", None)

    if bus == 'pcie':
        eprint("PCIe dynamic device passthroug not implemented yet")
        raise typer.Exit(code=-1)

    # TODO: here we cannot add a new rule if no rules
    if False and not dpconfig:
        eprint(f"vm ddp config: '{vmname}' not found")
        raise typer.Exit(code=-1)

    eprint("Add a new rule")
    newrule = {'bus': "usb" if bus == "usb" else "pcie",
               'productid': productid, 'vendorid': vendorid}
    configuration.append(newrule)
    dpconfig['devices'] = configuration
    # If "enable" key not found, set default false
    if enabled == None:
        dpconfig['enable'] = False
        eprint('Set enable status using: sudo fmo-tool ddp enabled ' +vmname+ ' --enable')
    # If "enable" key is False, print guideline to enable
    if enabled == False:
        eprint('Set enable status using: sudo fmo-tool ddp enabled ' +vmname+ ' --enable')
    ctx.set_vmddp_config(vmname, dpconfig)
    ctx.save_config()
    os.system(f"sudo systemctl restart {SEVICE_NAME}.service")
    raise typer.Exit(code=0)


@app.command("delete")
def delete_dp_rules(
    vmname: Annotated[str, typer.Argument(help="VM name to print rules")],

    delete: Annotated[int, typer.Argument(help="Rule number to delete")],
) -> None:
    """
    Delete the VM DDP rule
    """
    ctx = get_ctx_if_vm_exist(vmname)
    dpconfig = ctx.get_vmddp_config(vmname)
    configuration = dpconfig.get("devices", [])

    eprint(f"Delete rule: {delete}")
    if delete < 0 or delete >= len(configuration):
        eprint(f"No rule with number: {delete}")
        raise typer.Exit(code=-1)
    _ = configuration.pop(delete)
    eprint(f"Delete rule: {_}")
    ctx.set_vmddp_config(vmname, dpconfig)
    ctx.save_config()
    os.system(f"sudo systemctl restart {SEVICE_NAME}.service")
    # TODO: Can this be done automatically? Instead of asking user to physically unplug device
    eprint('Please unplug the device for rules to take effect!')
    raise typer.Exit(code=0)


@app.command("rules")
def get_dp_rules(
    vmname: Annotated[str, typer.Argument(help="VM name to print rules")],

    rules: Annotated[bool, typer.Option("--rules", "-r")] = None,
) -> None:
    """
    Print VM DDP rules
    """
    ctx = get_ctx_if_vm_exist(vmname)
    pfconfig = ctx.get_vmddp_config(vmname)
    configuration = pfconfig.get("devices", [])

    if not pfconfig:
        eprint(f"vm ddp config: '{vmname}' not found")
        raise typer.Exit(code=-1)

    if rules:
        for n, config in enumerate(configuration):
            bus = config['bus']
            pid = config['productid']
            vid = config['vendorid']
            print(f"{bus} {pid} {vid}")
        raise typer.Exit(code=0)

    for n, config in enumerate(configuration):
        print(n, config)
    raise typer.Exit(code=0)


@app.command("enabled")
def ddp_service_enabled_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to get ddp status")],

    enable: Annotated[bool, typer.Option("--enable", "-e")] = False,
    disable: Annotated[bool, typer.Option("--disable", "-d")] = False,
) -> None:
    """
    Check or set/reset DDP enabled status for VM
    """
    ctx = get_ctx_if_vm_exist(vmname)

    if enable and disable:
        eprint("Can't set and unset enabled option toghether")
        raise typer.Exit(code=-1)

    if enable or disable:
        ctx.set_vmddp_enabled(vmname, enable)
        ctx.save_config()

    os.system(f"sudo systemctl restart {SEVICE_NAME}.service")
    print(ctx.get_vmddp_enabled(vmname))
