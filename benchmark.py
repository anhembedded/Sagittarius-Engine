import timeit

setup = """
health = {"components": {str(i): "ok" for i in range(100)}}
env = {"os": "Linux", "os_release": "5.15", "python_version": "3.10", "cpu_percent": 10.0, "ram_mb": 1024}
uptime = 12345.6
health_status = "HEALTHY"
health_color = "green"
"""

stmt_concat = """
overview_text = f"[b]Uptime:[/b] {uptime:.1f}s | [b]Status:[/b] [{health_color}][b]{health_status}[/b][/{health_color}]\\n"
overview_text += f"[b]OS:[/b] {env.get('os')} {env.get('os_release')} | [b]Python:[/b] {env.get('python_version')}\\n"
overview_text += (
    f"[b]CPU:[/b] {env.get('cpu_percent')} | [b]RAM:[/b] {env.get('ram_mb')}\\n\\n"
)
for comp, stat in health.get("components", {}).items():
    icon = "✅" if stat == "ok" else "❌"
    overview_text += f"{icon} [b]{comp}[/b]: {stat}\\n"
"""

stmt_list = """
overview_parts = [
    f"[b]Uptime:[/b] {uptime:.1f}s | [b]Status:[/b] [{health_color}][b]{health_status}[/b][/{health_color}]\\n",
    f"[b]OS:[/b] {env.get('os')} {env.get('os_release')} | [b]Python:[/b] {env.get('python_version')}\\n",
    f"[b]CPU:[/b] {env.get('cpu_percent')} | [b]RAM:[/b] {env.get('ram_mb')}\\n\\n"
]
for comp, stat in health.get("components", {}).items():
    icon = "✅" if stat == "ok" else "❌"
    overview_parts.append(f"{icon} [b]{comp}[/b]: {stat}\\n")
overview_text = "".join(overview_parts)
"""

concat_time = timeit.timeit(stmt_concat, setup=setup, number=10000)
list_time = timeit.timeit(stmt_list, setup=setup, number=10000)

print(f"Concat: {concat_time:.4f}s")
print(f"List: {list_time:.4f}s")
print(f"Improvement: {(concat_time - list_time) / concat_time * 100:.2f}%")
