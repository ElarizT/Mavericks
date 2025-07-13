import json
from rich import print


def render_error(msg: str):
    print(f"[bold red]Error: {msg}[/bold red]")
    return


def render_warning(msg: str):
    print(f"[yellow]:warning: {msg}[/yellow]")
    return


def render_success(msg: str):
    print(f"[green]{msg}[/green]")
    return


def render_info(msg: str):
    print(f"[grey100]{msg}[/grey100]")


def prettify_json(httpx_json: dict):
    return json.dumps(httpx_json, indent=4)
