"""
The cli tool for pyiamanalyzer.
"""
import typer
import pyiamanalyzer.core.deployer as deployer
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def deploy():
    """
    Deploys the cloudformation stack for pyiamanalyzer.
    """
    logger.info("Running deploy...")
    print("Running deploy...")
    deployer.deploy_stack()


@app.command()
def destroy():
    """
    Destroys the cloudformation stack for pyiamanalyzer.
    """
    logger.info("Running destroy...")
    deployer.destroy_stack()


def main():
    """
    Entrypoint for the cli tool.
    """
    app()


if __name__ == "__main__":
    main()
