from flask import Flask
from AEYE import create_aeye_opticnet_framework
import click

framework = create_aeye_opticnet_framework()

@framework.cli.command("run")
@click.option('--host', default='0.0.0.0', help='DO NOT TOUCH')
@click.option('--port', default=6000, help='DO NOT TOUCH')
@click.option('--debug', is_flag=False, help='Enable or Disable debug mode')
def start_framework(host, port, debug):
    click.echo(f"[AI - Opticnet] Initialize Framework on host {host} and port {port}...")

    framework.run(host=host, port=port, debug=debug)



if __name__ == "__main__":
    framework.run(host='0.0.0.0', port=2000, debug=True)
