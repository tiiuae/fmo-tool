import typer
from utils.misc import eprint
from utils.fmoconfig import get_fmoconfig_manager, FMOConfig_Manager


def get_ctx_if_vm_exist(
    vmname: str,
    ctx: FMOConfig_Manager = None
) -> FMOConfig_Manager:
    if ctx is None:
        ctx = get_fmoconfig_manager()

    if not ctx.is_vm_exist(vmname):
        eprint(f"vm: {vmname} not found")
        raise typer.Exit(code=-1)

    return ctx


def get_ctx_if_dci_enabled(
    vmname: str,
    ctx: FMOConfig_Manager = None
) -> FMOConfig_Manager:
    if ctx is None:
        ctx = get_ctx_if_vm_exist(vmname)

    enabled = ctx.get_vmdci_enabled(vmname)

    if enabled is False:
        eprint(f"{vmname} dci is not enabled")
        raise typer.Exit(code=-1)

    return ctx


def get_ctx_if_dpf_enabled(
    vmname: str,
    ctx: FMOConfig_Manager = None
) -> FMOConfig_Manager:
    if ctx is None:
        ctx = get_ctx_if_vm_exist(vmname)

    enabled = ctx.get_vmportforwarding_enabled(vmname)

    if enabled is False:
        eprint(f"{vmname} dpf is not enabled")
        raise typer.Exit(code=-1)

    return ctx
