import urllib.request
import json
import argparse
import sys
import time

try:
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.console import Console
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def fetch_telemetry(port: int) -> dict:
    try:
        req = urllib.request.Request(f"http://localhost:{port}/")
        with urllib.request.urlopen(req, timeout=1.0) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

def generate_ui(port: int):
    data = fetch_telemetry(port)
    if not data:
        return Panel(
            f"[red]🔴 Connection Error[/red]\nCannot connect to Engine at [b]http://localhost:{port}[/b].\n"
            "Make sure the engine is running and `AuditExtension(enable_dashboard=True)` is registered.",
            title="Sagittarius Engine Audit Dashboard",
            border_style="red",
            box=box.ROUNDED
        )

    # 1. Tasks Table
    tasks = data.get("tasks", [])
    table = Table(title="Background Tasks & Scheduler", box=box.ROUNDED, expand=True, border_style="blue")
    table.add_column("Task ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Status")
    table.add_column("Runtime", justify="right", style="green")

    for t in tasks:
        status = t.get("status", "Unknown")
        if status == "running":
            status_str = f"[bold green]▶ {status}[/bold green]"
        elif status == "completed":
            status_str = f"[bold blue]✓ {status}[/bold blue]"
        elif status == "failed":
            status_str = f"[bold red]✗ {status}[/bold red]"
        else:
            status_str = status
        table.add_row(t.get("id"), t.get("name"), status_str, t.get("runtime"))
        
    if not tasks:
        table.add_row("", "No background tasks", "", "")

    # 2. Overview
    uptime = data.get("uptime", 0.0)
    health = data.get("health", {})
    env = data.get("environment", {})
    health_status = health.get("status", "unknown").upper()
    health_color = "green" if health_status == "HEALTHY" else "red"
    
    overview_text = f"[b]Uptime:[/b] {uptime:.1f}s | [b]Status:[/b] [{health_color}][b]{health_status}[/b][/{health_color}]\n"
    overview_text += f"[b]OS:[/b] {env.get('os')} {env.get('os_release')} | [b]Python:[/b] {env.get('python_version')}\n\n"
    for comp, stat in health.get("components", {}).items():
        icon = "✅" if stat == "ok" else "❌"
        overview_text += f"{icon} [b]{comp}[/b]: {stat}\n"
    
    overview_panel = Panel(overview_text, title="System Overview", border_style="cyan", box=box.ROUNDED)

    # 3. Extensions
    exts = data.get("extensions", [])
    srvs = data.get("services", [])
    ext_text = ""
    for e in exts:
        icon = "✅" if e.get('enabled') else "❌"
        ext_text += f"{icon} [b]{e.get('name')}[/b] (v{e.get('version')})\n"
    
    ext_text += "\n[bold blue]Hosted Services[/bold blue]\n"
    if not srvs:
        ext_text += "*No background hosted services are currently running.*\n"
    for s in srvs:
        ext_text += f"🟢 [b]{s}[/b]\n"
    
    ext_panel = Panel(ext_text, title="Extensions & Services", border_style="yellow", box=box.ROUNDED)

    # 4. Config & Event Bus
    config_bus = data.get("config_bus", {})
    eb_handlers = config_bus.get("event_bus_handlers", {})
    config_keys = config_bus.get("config_keys", [])
    
    cb_text = "[bold blue]Event Bus[/bold blue]\n"
    if not eb_handlers:
        cb_text += "*No events registered.*\n"
    for ev, count in eb_handlers.items():
        cb_text += f"📨 [b]{ev}[/b]: {count} handler(s)\n"
    
    cb_text += "\n[bold blue]Config Keys[/bold blue]\n"
    if not config_keys:
        cb_text += "*No config keys loaded.*\n"
    for k in config_keys:
        cb_text += f"🎛️ {k}\n"
        
    cb_panel = Panel(cb_text, title="Config & Event Bus", border_style="magenta", box=box.ROUNDED)

    # 5. Assemble Layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    
    active_tasks = len([t for t in tasks if t.get("status") == "running"])
    header_text = f"[bold white]🚀 Sagittarius Engine Dashboard[/bold white] | Port: [yellow]{port}[/yellow] | Active Tasks: [green]{active_tasks}[/green]"
    layout["header"].update(Panel(header_text, box=box.ROUNDED, border_style="blue"))
    
    layout["main"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=1)
    )
    layout["left"].update(table)
    
    layout["right"].split_column(
        Layout(name="overview", ratio=1),
        Layout(name="extensions", ratio=1),
        Layout(name="config", ratio=1)
    )
    layout["right"]["overview"].update(overview_panel)
    layout["right"]["extensions"].update(ext_panel)
    layout["right"]["config"].update(cb_panel)
    
    layout["footer"].update(Panel("Press [bold red]Ctrl+C[/bold red] to quit", box=box.ROUNDED, border_style="red"))

    return layout


def main():
    if not RICH_AVAILABLE:
        print("❌ Error: 'rich' is not installed.")
        print("Please run: pip install rich")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Sagittarius Audit Dashboard")
    parser.add_argument("--port", type=int, default=9999, help="Telemetry server port")
    args = parser.parse_args()

    console = Console()
    console.clear()
    
    try:
        with Live(generate_ui(args.port), refresh_per_second=1, screen=True) as live:
            while True:
                time.sleep(1.0)
                live.update(generate_ui(args.port))
    except KeyboardInterrupt:
        console.print("[bold green]Dashboard stopped gracefully.[/bold green]")


if __name__ == "__main__":
    main()
