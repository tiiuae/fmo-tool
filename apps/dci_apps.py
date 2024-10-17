import typer

from utils.ssh import ssh_vm_helper
from utils.utils import get_ctx_if_vm_exist, get_ctx_if_dci_enabled

from typing_extensions import Annotated

SERVICE_NAME = "fmo-dci"

app = typer.Typer()


@app.command("restart")
def docker_service_restart_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to dci restart")],
) -> None:
    """
    Request DCI restart
    """
    _ = get_ctx_if_dci_enabled(vmname)
    ssh_vm_helper(vmname, f"sudo -S systemctl restart {SERVICE_NAME}.service")


@app.command("start")
def docker_service_start_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to dci start")],
) -> None:
    """
    Request DCI start
    """
    _ = get_ctx_if_dci_enabled(vmname)
    ssh_vm_helper(vmname, f"sudo -S systemctl start {SERVICE_NAME}.service")


@app.command("stop")
def docker_service_stop_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to dci stop")],
) -> None:
    """
    Request DCI stop
    """
    _ = get_ctx_if_dci_enabled(vmname)
    ssh_vm_helper(vmname, f"sudo -S systemctl stop {SERVICE_NAME}.service")


@app.command("status")
def docker_service_status_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to get dci status")],
) -> None:
    """
    Request DCI status
    """
    _ = get_ctx_if_dci_enabled(vmname)
    ssh_vm_helper(vmname, f"systemctl status {SERVICE_NAME}.service")


@app.command("enabled")
def docker_service_enabled_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to get dci status")],
) -> None:
    """
    Check DCI enabled status for VM
    """
    ctx = get_ctx_if_vm_exist(vmname)
    print(ctx.get_vmdci_enabled(vmname))
