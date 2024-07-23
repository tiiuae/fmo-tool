import typer

import apps.vms_apps as vms_apps
import apps.dci_apps as dci_apps
import apps.system_apps as system_apps
import apps.portforwarding_apps as dpf_apps
import apps.devicepassthrough_apps as ddp_apps

from utils.ssh import ssh_vm_helper

from typing_extensions import Annotated

app = typer.Typer()
app.add_typer(vms_apps.app, name="vms", help="Manage VMs")
app.add_typer(system_apps.app, name="system", help="Manage system")
app.add_typer(dci_apps.app, name="dci",
              help="Manage Docker Compose Infrastructure (DCI)")
app.add_typer(dpf_apps.app, name="dpf",
              help="Manage Dynamic PortForwarding (DPF)")
app.add_typer(ddp_apps.app, name="ddp",
              help="Manage Dynamic Devices Passthrough (DDP)")


@app.command("ssh")
def ssh_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to ssh")],
    cmd: Annotated[str, typer.Argument(
        help="command to run remotly, "
             "commands with params need to be quoted: `ls -l`")] = None,
) -> None:
    """
    SSH to vm
    """
    ssh_vm_helper(vmname, cmd)
