import os
import json
import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from pbuster.phantombuster import PhantomBuster
from dotenv import load_dotenv

load_dotenv()

DATEFORMAT = '%Y-%m-%d %H:%M'

console = Console()
pb = PhantomBuster(api_key=os.getenv("PHANTOMBUSTER_API_KEY", ""))


def _args_to_dict(args):
    """Convert a string of key=value pairs to a dictionary."""
    if not args:
        return {}
    return dict(item.split('=') for item in args.split(','))

def _dict_to_default_table(data):
    """Convert a dictionary to a Rich Table.
    
    Args:
        data (dict): The dictionary to convert.
        
    Returns:
        Table: A Rich Table containing the dictionary data.
    """
    table = Table()
    table.add_column("Key", style="white")
    table.add_column("Value", style="magenta", width=80)
    for key, value in data.items():
        if isinstance(value, dict):
            value = json.dumps(value, indent=2)
        elif isinstance(value, list):
            value = json.dumps(value)
        table.add_row(key, str(value))
    return table

@click.group()
def cli():
    pass

# -------------------------- ORG --------------------------
# ----------------------------------------------------------

@cli.group()
def org():
    pass

@org.command()
def info():
    """Display organization information."""
    org_info = pb.org.info()
    console.print(org_info)

@org.command()
def usage():
    """Display organization usage statistics."""
    org_usage = pb.org.usage()
    console.print(org_usage)

# --------------------- AGENT COMMANDS ---------------------
# ----------------------------------------------------------

@cli.group()
def agent():
    pass


@agent.command(name='list')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_list(debug=False):
    agents = pb.agent.list()
    table = Table()
    table.add_column("#", style="white")
    table.add_column("Id", style="white")
    table.add_column("Name", style="magenta")
    table.add_column("Script ID", style="white")
    table.add_column("Creation", style="white")
    table.add_column("Launched", style="white")
    for i, agent in enumerate(agents, start=1):
        table.add_row(
            str(i),
            agent.get("id", ""),
            agent.get("name", ""),
            agent.get("scriptId", ""),
            datetime.fromtimestamp(agent.get("createdAt", 0) / 1000).strftime(DATEFORMAT),
            agent.get("launchType", ""))
        
    console.print(table) if not debug else console.print(agents)


@agent.command(name='show')
@click.argument('agent_id')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_show(agent_id, debug):
    agent = pb.agent.get(agent_id)
    table = _dict_to_default_table(agent)
    console.print(table) if not debug else console.print(agent)


@agent.command(name='status')
@click.argument('agent_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_status(agent_id, debug):
    try:
        status = pb.agent.status(agent_id) # Finished, Running, Error, etc.
        if not debug:
            console.print(f"[+] Agent {agent_id} status: {status}", style="green")
        else:
            console.print({"status": status})
    except Exception as e:
        console.print(f"[X] {e.args[0].get('content').get('error')}", style="red")


@agent.command(name='create')
@click.option('--script', '-s', required=True, help='Script ID to associate with the agent.')
@click.option('--name', '-n', default=None, help='Name of the agent.')
@click.option('--org', '-o', default='phantombuster', help='Organization name to associate with the agent.')
@click.option('--args', '-a', default='', help='Arguments to pass to the agent in key=value format.')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_create(script, name, org, args, debug):
    try:
        agent = pb.agent.create(script, name, org, args)
        if debug:
            console.print(agent)
        else:
            console.print(f"[+] Created agent with ID: {agent.get('id')}", style="green")
    except Exception as e:
        err = e.args[0].get('content', {}).get('error', 'Unknown error')
        if err == 'Could not validate data':
            console.print(f"[X] Script not found. Must include extension name.", style="red")
        else:
            console.print(f"[X] {err}", style="red")

@agent.command(name='stop')
@click.argument('agent_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_stop(agent_id, debug):
    try:
        rsp = pb.agent.stop(agent_id)
        if not debug:
            console.print(f"[+] Stopped agent {agent_id}.", style="green")
        else:
            console.print(rsp)
    except Exception as e:
        console.print(f"[X] {e.args[0].get('content').get('error')}", style="red")

@agent.command(name='delete')
@click.argument('agent_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_delete(agent_id, debug):
    try:
        rsp = pb.agent.delete(agent_id)
        if not debug:
            console.print(f"[+] Deleted.", style="green")
        else:
            console.print(rsp)
    except Exception as e:
        console.print(f"[X] {e.args[0].get('content').get('error')}", style="red")

@agent.command(name='launch')
@click.argument('agent_id')
@click.option('--args', '-a', default='', help='Arguments to pass to the agent. (key1=value1,key2=value2)')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_run(agent_id, args, debug):
    try:
        arguments = _args_to_dict(args)
        if not arguments:
            console.print("[X] No arguments provided. Use --args to pass arguments in key=value format.", style="red")
            return
        
        rsp = pb.agent.launch(agent_id, arguments)
        if not debug:
          console.print(f"[+] Agent {agent_id} launched successfully. (Container {rsp.get('containerId')})", style="green")
        else:
            console.print(rsp)
    except Exception as e:
        console.print(f"[X] {e.args[0].get('content').get('error')}", style="red")

@agent.command(name='launch-and-wait')
@click.argument('agent_id')
@click.option('--args', '-a', default='', help='Arguments to pass to the agent. (key1=value1,key2=value2)')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_launch_and_wait(agent_id, args, debug):
    try:
        arguments = _args_to_dict(args)
        if not arguments:
            console.print("[X] No arguments provided. Use --args to pass arguments in key=value format.", style="red")
            return

        results = pb.agent.launch_and_wait(agent_id, arguments)
        if not debug:
            console.print(f"[+] Agent {agent_id} launched successfully.", style="green")
            table = _dict_to_default_table(results)
            console.print(table)
        else:
            console.print(results)
    except Exception as e:
        console.print(f"[X] {e.args[0]}", style="red")

@agent.command(name='wait')
@click.argument('agent_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def agent_wait(agent_id, debug):
    try:
        agent = pb.agent.wait(agent_id)
        if not debug:
            table = _dict_to_default_table(agent)
            console.print(table)
        else:
            console.print(agent)
    except Exception as e:
        console.print(f"[X] {e.args[0]}", style="red")

# ---------------------- SCRIPT COMMANDS ---------------------
# ------------------------------------------------------------

@cli.group()
def script():
    pass

@script.command(name='list')
@click.option('--filter', '-f', default=None, help='Filter scripts by name.')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def script_list(filter, debug):
    scripts = pb.script.list()

    if filter:
        scripts = [script for script in scripts if filter.lower() in script.get("name", "").lower()]

    # Sort by creation date inverted
    if scripts:
        scripts.sort(key=lambda x: x.get("created_at", 0), reverse=False)

    table = Table()
    table.add_column("#", style="white")
    table.add_column("Id", style="white")
    table.add_column("Name", style="magenta")
    table.add_column("Created At", style="white")
    table.add_column("Updated At", style="white")

    for i, script in enumerate(scripts, start=1):
        table.add_row(
            str(i),
            script.get("id", ""),
            script.get("name", ""),
            datetime.fromtimestamp(script.get("created_at", 0) / 1000).strftime(DATEFORMAT),
            datetime.fromtimestamp(script.get("updated_at", 0) / 1000).strftime(DATEFORMAT),
        )

    if not debug:
        console.print(table)
    else:
        console.print(scripts)

@script.command(name='show')
@click.argument('script_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def script_show(script_id, debug):
    script = pb.script.get(script_id)
    if not debug:
        table = _dict_to_default_table(script)
        console.print(table)
    else:
        console.print(script)


@script.command(name='args')
@click.argument('script_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw agent data.')
def script_args(script_id, debug):
    try:
        args = pb.script.args(script_id)
        if not debug:
            table = _dict_to_default_table(args)
            console.print(table)
        else:
            console.print(args)
    except Exception as e:
        console.print(f"[X] {e.args[0].get('content').get('error')}", style="red")

# ---------------------- CONTAINER COMMANDS -------------------
# ------------------------------------------------------------

@cli.group()
def container():
    pass

@container.command(name='list')
@click.argument('agent_id', required=True)
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw container data.')
def container_list(agent_id, debug):
    containers = pb.container.list(agent_id)
    if not debug:
        table = Table()
        table.add_column("ID", style="white")
        table.add_column("Status", style="white")
        table.add_column("Created", style="white")
        table.add_column("Launched", style="white")
        table.add_column("ExitCode", style="white")
        for container in containers:
            table.add_row(
                container.get("id", ""),
                container.get("status", ""),
                datetime.fromtimestamp(container.get("createdAt", 0) / 1000).strftime(DATEFORMAT),
                container.get("launchType", ""),
                str(container.get("exitCode", "")),
            )
        console.print(table)
    else:
        console.print(containers)

@container.command(name='show')
@click.argument('container_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw container data.')
def container_show(container_id, debug):
    container = pb.container.get(container_id)
    if not debug:
        table = _dict_to_default_table(container)
        console.print(table)
    else:
        console.print(container)

@container.command(name='results')
@click.argument('container_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw container data.')
def container_results(container_id, debug):
    results = pb.container.results(container_id)
    if not debug:
        table = _dict_to_default_table(results)
        console.print(table)
    else:
        console.print(results)


@container.command(name='output')
@click.argument('container_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw container data.')
def container_output(container_id, debug):
    output = pb.container.output(container_id, raw=True)
    if not debug:
        table = Table(show_header=False)
        table.add_column("Output", style="magenta", overflow="fold")
        # Print txt output
        for line in output.splitlines():
            table.add_row(line)
        console.print(table)
    else:
        console.print({output})

@container.command(name='wait')
@click.argument('container_id')
@click.option('--debug', '-d', default=False, is_flag=True, help='Enable debug mode to print raw container data.')
def container_wait(container_id, debug):
    try:
        container = pb.container.wait(container_id)

        if not debug:
            table = _dict_to_default_table(container)
            console.print(table)
        else:
            console.print(container)
    except Exception as e:
        console.print(f"[X] {e.args[0].get('content').get('error')}", style="red")

if __name__ == "__main__":
    cli()