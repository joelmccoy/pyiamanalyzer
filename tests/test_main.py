from pyiamanalyzer.main import app
from typer.testing import CliRunner
from unittest.mock import patch

runner = CliRunner()


@patch("pyiamanalyzer.core.deployer.deploy_stack")
def test_deploy(m_deploy_stack):
    """
    Test the CLI deploy command
    """
    runner.invoke(app, ["deploy"])
    m_deploy_stack.assert_called_once()


@patch("pyiamanalyzer.core.deployer.destroy_stack")
def test_destroy(m_destroy_stack):
    """
    Test the CLI destroy command
    """
    runner.invoke(app, ["destroy"])
    m_destroy_stack.assert_called_once()
