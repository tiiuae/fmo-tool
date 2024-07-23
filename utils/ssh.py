import typer

from typing_extensions import Annotated
from utils.utils import get_ctx_if_vm_exist


app = typer.Typer()


@app.command("ssh")
def ssh_cmd(
    vmname: Annotated[str, typer.Argument(help="VM name to ssh")],
    cmd: Annotated[str, typer.Argument(
        help="command to run remotly, "
             "commands with params need to be quoted: `ls -l`")],
) -> None:
    """
    SSH to vm
    """
    ssh_vm_helper(vmname, cmd)


def ssh_vm_helper(vmname: str, cmd: str = None) -> None:
    """
    SSH to vm
    """
    ctx = get_ctx_if_vm_exist(vmname)

    ip = ctx.get_vm_ip(vmname)
    ssh(ip, cmd=cmd)


def ssh(ip: str, port: int = 22, cmd: str = None, system: bool = True) -> None:
    if system:
        ssh_system(ip, port, cmd)
    else:
        ssh_paramiko(ip, port, cmd)


def ssh_system(ip: str, port: int = 22, cmd: str = None) -> None:
    import os
    if not cmd:
        # TODO: need to get the name from config?
        os.system(f"ssh -p {port} ghaf@{ip}")
    else:
        # TODO: need to get the name from config?
        os.system(f"ssh -p {port} ghaf@{ip} {cmd}")


def ssh_paramiko(ip: str, port: int = 22, cmd: str = None) -> None:
    import paramiko
    from utils import interactive

    client = paramiko.SSHClient()
    # TODO: need to be reworked and removed
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # TODO: get username and auth data from external source
    client.connect(ip, username='test', password='123')
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.invoke_shell()
    interactive.interactive_shell(channel)
    client.close()
