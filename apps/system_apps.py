import typer

from utils.misc import print_config, eprint
from utils.fmoconfig import get_fmoconfig_manager
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def config():
    """
    Get full system config
    """
    ctx = get_fmoconfig_manager()
    print(print_config(ctx.get_config()))


@app.command()
def ip(ip: Annotated[str, typer.Argument(help="New IP")] = None):
    """
    Get/Set system ip address
    """
    ctx = get_fmoconfig_manager()

    if ip is None:
        print(ctx.get_system_ip())
    else:
        #TODO: system IP needs to be managment by fmo-tool
        eprint("Storing the system's IP has not been implemented yet")
        return
        ctx.set_system_ip(ip)
        ctx.save_config()


@app.command()
def alias(alias: Annotated[str, typer.Argument(help="New alias")] = None):
    """
    Get/Set system alias
    """
    ctx = get_fmoconfig_manager()

    if alias is None:
        print(ctx.get_system_alias())
    else:
        ctx.set_system_alias(alias)
        ctx.save_config()


@app.command("ra")
def RAversion():
    """
    Get system RegistrationAgent version
    """
    ctx = get_fmoconfig_manager()
    print(ctx.get_system_RAversion())


@app.command("gw")
def defaultGW(gw: Annotated[str, typer.Argument(help="New GW")] = None):
    """
    Get/Set system default gateway
    """
    ctx = get_fmoconfig_manager()

    if gw is None:
        print(ctx.get_system_defaultGW())
    else:
        ctx.set_system_defaultGW(gw)
        ctx.save_config()


@app.command("cr")
def dockerCR(cr: Annotated[str, typer.Argument(help="New CR")] = None):
    """
    Get/Set system docker Container Repository
    """
    ctx = get_fmoconfig_manager()

    if cr is None:
        print(ctx.get_system_dockerCR())
    else:
        ctx.set_system_dockerCR(cr)
        ctx.save_config()


@app.command()
def release():
    """
    Get system release version
    """
    ctx = get_fmoconfig_manager()
    print(ctx.get_system_release())


@app.command()
def name():
    """
    Get system iso name
    """
    ctx = get_fmoconfig_manager()
    print(ctx.get_system_name())


@app.command()
def restore():
    """
    Restore default config
    """
    ctx = get_fmoconfig_manager()
    ctx.restore_config()
