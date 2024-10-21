import typer
import getpass

from typing import Optional
from typing_extensions import Annotated
from utils.misc import require_root
from utils.utils import get_ctx_if_vm_exist

def ssh_vm_helper_with_sudo(vmname: str, cmd: Optional[str]=None, prompt: str="Type remote sudo password: ") -> None:
    password = getpass.getpass(prompt)
    if not password:
        eprint("No password entered!")
    new_cmd = f"'echo {password} | sudo -S {cmd}'"
    ssh_vm_helper(vmname, new_cmd)

@require_root
def ssh_vm_helper(vmname: str, cmd: Optional[str]=None) -> None:
    """
    SSH to vm
    """
    ctx = get_ctx_if_vm_exist(vmname)

    # TODO: this one need to be read from fmo-config.yaml
    ssh_configs = {
        'netvm': '-i /run/ssh-keys/id_ed25519 -o StrictHostKeyChecking=no',
        'dockervm': '-i /run/ssh-keys/id_ed25519 -o StrictHostKeyChecking=no'
    }

    ip = ctx.get_vm_ip(vmname)
    ssh(ip, cmd=cmd, args=ssh_configs.get(vmname, ""))


def ssh(ip: str, port: int=22, cmd: Optional[str]=None, system: bool=True, args: Optional[str]=None) -> None:
    if system:
        ssh_system(ip, port, cmd, args)
    else:
        ssh_paramiko(ip, port, cmd)


def ssh_system(ip: str, port: int=22, cmd: Optional[str]=None, args: Optional[str]=None) -> None:
    import os
    args = args if args is not None else ""

    if not cmd:
        # TODO: need to get the name from config?
        cmd = f"ssh -p {port} {args} ghaf@{ip}"
    else:
        # TODO: need to get the name from config?
        cmd = f"ssh -p {port} {args} ghaf@{ip} {cmd}"

    os.system(cmd)


def ssh_paramiko(ip: str, port: int=22, cmd: Optional[str]=None) -> None:
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
