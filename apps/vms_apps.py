import typer

from utils.ssh import ssh_vm_helper
from utils.misc import print_config, eprint
from utils.utils import get_ctx_if_vm_exist

from typing_extensions import Annotated
from utils.fmoconfig import get_fmoconfig_manager

from rich.console import Console
from rich.table import Table


console = Console()
app = typer.Typer()


@app.command()
def config(
    vmname: Annotated[str, typer.Argument(help="VM name to print config")],
) -> None:
    """
    Print VM config
    """
    ctx = get_ctx_if_vm_exist(vmname)
    vmconfig = ctx.get_vmconfig(vmname)

    if not vmconfig:
        eprint(f"vm config: {vmname} not found")
        raise typer.Exit(code=-1)

    print(print_config(vmconfig))


@app.command()
def ip(
    vmname: Annotated[str, typer.Argument(help="VM name to get IP")],
) -> None:
    """
    Get VM IP address
    """
    ctx = get_ctx_if_vm_exist(vmname)
    ip = ctx.get_vm_ip(vmname)

    print(f"{ip}")


@app.command()
def list(
    list_only: Annotated[bool, typer.Option(
        "--list", "-l", help="list vm names only")] = False,
    names_only: Annotated[bool, typer.Option(
        "--no-ip", help="don't print IP address")] = False,
) -> None:
    """
    Get VM list
    """
    ctx = get_fmoconfig_manager()
    vmlist = ctx.get_vms_names_list()
    iplist = [ctx.get_vm_ip(vm) for vm in vmlist]

    if list_only:
        print("[", ", ".join(vmlist), "]")
        return

    table_names = ["VM name",] if names_only else ["VM name", "IP address"]
    table = Table(*table_names, show_lines=True, box=None)

    for vm, ip in zip(vmlist, iplist):
        table.add_row(vm) if names_only else table.add_row(vm, ip)

    console.print(table)


@app.command()
def restart(
        vmname: Annotated[str, typer.Argument(help="VM name to restart")],
        delay: Annotated[int, typer.Argument(help="restart delay")] = 0
) -> None:
    """
    Restart VM
    """
    _ = get_ctx_if_vm_exist(vmname)

    import os
    os.system(f"sudo systemctl restart microvm@{vmname}.service")


@app.command()
def stop(
        vmname: Annotated[str, typer.Argument(help="VM name to stop")],
        delay: Annotated[int, typer.Argument(help="restart delay")] = 0
) -> None:
    """
    Stop VM
    """
    _ = get_ctx_if_vm_exist(vmname)

    import os
    os.system(f"sudo systemctl stop microvm@{vmname}.service")


@app.command()
def start(
        vmname: Annotated[str, typer.Argument(help="VM name to start")],
        delay: Annotated[int, typer.Argument(help="restart delay")] = 0
) -> None:
    """
    Start VM
    """
    _ = get_ctx_if_vm_exist(vmname)

    import os
    os.system(f"sudo systemctl start microvm@{vmname}.service")


@app.command()
def status(
        vmname: Annotated[str, typer.Argument(help="VM name to stop")],
        delay: Annotated[int, typer.Argument(help="restart delay")] = 0
) -> None:
    """
    Get VM status
    """
    _ = get_ctx_if_vm_exist(vmname)

    import os
    os.system(f"sudo systemctl status microvm@{vmname}.service")


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
