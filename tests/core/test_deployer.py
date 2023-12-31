from moto import mock_cloudformation
import pyiamanalyzer.core.deployer as deployer
import boto3
import logging
import pytest
from botocore.exceptions import ClientError


@pytest.fixture(autouse=True)
def configure_logging(level=logging.INFO):
    """
    Sets up the expected logging format.
    """
    logging.basicConfig(level=level, format="%(message)s")


def test_deploy_stack():
    """
    Tests the deploy_stack when the stack doesn't exist.
    """
    with mock_cloudformation():
        deployer.deploy_stack()

        client = boto3.client("cloudformation")
        response = client.describe_stacks(StackName="pyiamanalyzer")
        assert len(response["Stacks"]) == 1


def test_deploy_stack_already_exists(caplog):
    """
    Tests the deploy_stack when the stack already exists.
    """
    caplog.set_level(logging.INFO)
    with mock_cloudformation():
        deployer.deploy_stack()
        deployer.deploy_stack()
        log_messages = [record.message for record in caplog.records]
        assert "Stack already exists.  Updating it." in log_messages

        client = boto3.client("cloudformation")
        response = client.describe_stacks(StackName="pyiamanalyzer")
        assert len(response["Stacks"]) == 1


def test_destroy_stack():
    """
    Tests the destroy_stack function.
    """
    with mock_cloudformation():
        deployer.deploy_stack()

        client = boto3.client("cloudformation")
        response = client.describe_stacks(StackName="pyiamanalyzer")
        assert len(response["Stacks"]) == 1

        deployer.destroy_stack()
        with pytest.raises(ClientError):
            client.describe_stacks(StackName="pyiamanalyzer")
