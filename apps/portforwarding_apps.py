import typer

from enum import Enum
from utils.ssh import ssh_vm_helper, ssh_vm_helper_with_sudo
from utils.misc import print_config, eprint
from utils.utils import get_ctx_if_vm_exist, get_ctx_if_dpf_enabled

from typing_extensions import Annotated


SEVICE_NAME = "fmo-dynamic-portforwarding-service"


class PF_Proto(str, Enum):
    tcp = "tcp"
    udp = "udp"


app = typer.Typer()


@app.command("config")
def get_pf_config(
    vmname: Annotated[str, typer.Argument(help="VM name to print config")],
) -> None:
    """
    Print VM DPF config
    """
    ctx = get_ctx_if_vm_exist(vmname)
    pfconfig = ctx.get_vmportforwarding(vmname)

    if not pfconfig:
        eprint(f"vm portforwarding config: '{vmname}' not found")
        raise typer.Exit(code=-1)

    print(print_config(pfconfig))


@app.command("add")
def add_pf_rules(
    vmname: Annotated[str, typer.Argument(help="VM name to print rules")],

    dip: Annotated[str, typer.Option("--dip")],
    sport: Annotated[str, typer.Option("--sport")],
    dport: Annotated[str, typer.Option("--dport")],
    sip: Annotated[str, typer.Option("--sip")] = None,
    proto: Annotated[PF_Proto, typer.Option("--proto", "-p")] = "tcp",
) -> None:
    """
    Add a new VM DPF rule
    """
    ctx = get_ctx_if_vm_exist(vmname)
    pfconfig = ctx.get_vmportforwarding(vmname)
    configuration = pfconfig.get("configuration", [])

    # TODO: here we cannot add a new rule if no rules
    if False and not pfconfig:
        eprint(f"vm portforwarding config: '{vmname}' not found")
        raise typer.Exit(code=-1)

    eprint("Add a new rule")
    newrule = {'dip': dip, 'dport': dport,
               'proto': 'tcp' if proto == 'tcp' else 'udp',
               'sport': sport}
    if sip is not None:
        newrule["sip"] = sip
    configuration.append(newrule)
    pfconfig['configuration'] = configuration
    ctx.set_vmportforwarding(vmname, pfconfig)
    ctx.save_config()
    ctx.write_vmpf_config(vmname, configuration)
    raise typer.Exit(code=0)


@app.command("delete")
def delete_pf_rules(
    vmname: Annotated[str, typer.Argument(help="VM name to print rules")],

    delete: Annotated[int, typer.Argument(help="Rule number to delete")],
) -> None:
    """
    Delete the VM DPF rule
    """
    ctx = get_ctx_if_vm_exist(vmname)
    pfconfig = ctx.get_vmportforwarding(vmname)
    configuration = pfconfig.get("configuration", [])

    eprint(f"Delete rule: {delete}")
    if delete < 0 or delete >= len(configuration):
        eprint(f"No rule with number: {delete}")
        raise typer.Exit(code=-1)
    _ = configuration.pop(delete)
    eprint(f"Delete rule: {_}")
    ctx.set_vmportforwarding(vmname, pfconfig)
    ctx.save_config()
    ctx.write_vmpf_config(vmname, configuration)
    raise typer.Exit(code=0)


@app.command("rules")
def get_pf_rules(
    vmname: Annotated[str, typer.Argument(help="VM name to print rules")],

    rules: Annotated[bool, typer.Option("--rules", "-r")] = False,
    hreadable: Annotated[bool, typer.Option("--human-readable", "-v")] = False,
) -> None:
    """
    Print VM DPF rules
    """
    ctx = get_ctx_if_vm_exist(vmname)
    pfconfig = ctx.get_vmportforwarding(vmname)
    configuration = pfconfig.get("configuration", [])

    if not pfconfig:
        eprint(f"vm portforwarding config: '{vmname}' not found")
        raise typer.Exit(code=-1)

    if hreadable:
        for n, config in enumerate(configuration):
            sip = config.get("sip", "NA")
            dip = config.get("dip")
            sport = config.get("sport")
            dport = config.get("dport")
            proto = config.get("proto")
            print(
                f"iptables -I INPUT -p {proto} --dport {sport} -j ACCEPT")
            print(f"iptables -t nat -I PREROUTING -p {proto} -d {dip} "
                  f"--dport {sport} -j DNAT --to-destination {sip}:{dport}")
        raise typer.Exit(code=0)

    if rules:
        for n, config in enumerate(configuration):
            sip = config.get("sip", "NA")
            dip = config.get("dip")
            sport = config.get("sport")
            dport = config.get("dport")
            proto = config.get("proto")
            print(f"{sip} {sport} {dport} {dip} {proto}")
        raise typer.Exit(code=0)

    for n, config in enumerate(configuration):
        if config.get("sip") is None:
            config["sip"] = "NA"
        print(n, config)
    raise typer.Exit(code=0)


@app.command("restart")
def dpf_service_restart_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to dpf restart")],
) -> None:
    """
    Request DPF restart
    """
    _ = get_ctx_if_dpf_enabled(vmname)
    ssh_vm_helper_with_sudo(vmname, f"systemctl restart {SEVICE_NAME}.service")


@app.command("start")
def dpf_service_start_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to dpf start")],
) -> None:
    """
    Request DPF start
    """
    _ = get_ctx_if_dpf_enabled(vmname)
    ssh_vm_helper_with_sudo(vmname, f"systemctl start {SEVICE_NAME}.service")


@app.command("stop")
def dpf_service_stop_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to dpf stop")],
) -> None:
    """
    Request DPF stop
    """
    _ = get_ctx_if_dpf_enabled(vmname)
    ssh_vm_helper_with_sudo(vmname, f"systemctl stop {SEVICE_NAME}.service")


@app.command("status")
def dpf_service_status_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to get dpf status")],
) -> None:
    """
    Request DPF status
    """
    _ = get_ctx_if_dpf_enabled(vmname)
    ssh_vm_helper(vmname, f"systemctl status {SEVICE_NAME}.service")


@app.command("enabled")
def dpf_service_enabled_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to get dpf status")],

    enable: Annotated[bool, typer.Option("--enable", "-e")] = False,
    disable: Annotated[bool, typer.Option("--disable", "-d")] = False,
) -> None:
    """
    Check or set/reset DPF enabled status for VM
    """
    ctx = get_ctx_if_vm_exist(vmname)

    if enable and disable:
        eprint("Can't set and unset enabled option toghether")
        raise typer.Exit(code=-1)

    if enable or disable:
        ctx.set_vmportforwarding_enabled(vmname, enable)
        ctx.save_config()

    print(ctx.get_vmportforwarding_enabled(vmname))
