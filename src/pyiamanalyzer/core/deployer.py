"""
Module to deploy and manage the pyiamanalyzer stack.
"""
import boto3
from botocore.exceptions import ClientError
from pyiamanalyzer.cloudformation.stack import pyiamanalyzerStack
import json
import logging

logger = logging.getLogger(__name__)

PYIAMANALYZER_STACK_NAME = "pyiamanalyzer"


def deploy_stack():
    """
    Deploys/updates the pyiamanalyzer stack.
    """
    logger.info(f"Deploying {PYIAMANALYZER_STACK_NAME} stack.")
    cloudformation = boto3.client("cloudformation")
    stack_exists: bool = False
    stack = pyiamanalyzerStack()
    stack.add_access_analyzer_alerting()

    try:
        cloudformation.describe_stacks(StackName=PYIAMANALYZER_STACK_NAME)
        stack_exists = True
    except ClientError as e:
        # Continue only if the stack doesn't exist.
        if "does not exist" in e.response["Error"]["Message"]:
            logger.info("Stack doesn't exist.  Creating it.")
            pass
        else:
            raise e

    if stack_exists:
        try:
            logger.info("Stack already exists.  Updating it.")
            cloudformation.update_stack(
                StackName=PYIAMANALYZER_STACK_NAME,
                TemplateBody=json.dumps(json.loads(stack.to_json())),
                Capabilities=["CAPABILITY_NAMED_IAM"],
            )
            logger.info(f"Successfully updated {PYIAMANALYZER_STACK_NAME} stack.")

        except ClientError as e:
            if e.response["Error"]["Message"] == "No updates are to be performed.":
                logger.info("Stack is already up to date.  No changes necessary.")
            else:
                raise e

    else:
        cloudformation.create_stack(
            StackName="pyiamanalyzer",
            TemplateBody=json.dumps(json.loads(stack.to_json())),
            Capabilities=["CAPABILITY_NAMED_IAM"],
        )
        logger.info(f"Successfully created {PYIAMANALYZER_STACK_NAME} stack.")


def destroy_stack():
    """
    Destroys the pyiamanalyzer stack.
    """
    logger.info(f"Destroying {PYIAMANALYZER_STACK_NAME} stack.")
    cloudformation = boto3.client("cloudformation")
    cloudformation.delete_stack(StackName=PYIAMANALYZER_STACK_NAME)
    logger.info(f"Successfully destroyed {PYIAMANALYZER_STACK_NAME} stack.")
