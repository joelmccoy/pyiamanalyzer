from troposphere import Template, GetAtt
from troposphere.awslambda import Function, Code
from troposphere.iam import Role, Policy
import inspect
import pyiamanalyzer.lambdas.access_analyzer_alerting


class pyiamanalyzerStack(Template):
    """
    The pyiamanalyzer cloudformation stack.
    """

    def __init__(self):
        super(pyiamanalyzerStack, self).__init__()
        self.access_analyzer_lambda_execution_role = None
        self.access_analyzer_lambda_function = None

        self.set_description("The pyiamanalyzer stack")

    def add_access_analyzer_alerting(self, external_access_alerts: bool = True):
        """
        Adds the resources for access analyzer alerting.

        This includes:
        - The eventbridge rule that pushes onto the sqs queue
        - The sqs queue that triggers the lambda function
        - The lambda function that generates the alerts

        Args:
            external_access_alerts (bool): Whether to enable alerts for external access IAM access analyzer findings.
        """

        # TODO : Add the eventbridge rule that pushes onto the sqs queue

        # TODO: Add the sqs queue that triggers the lambda function

        # IAM role for lambda function
        self.access_analyzer_lambda_execution_role = self.add_resource(
            Role(
                "LambdaExecutionRole",
                Path="/",
                Policies=[
                    Policy(
                        PolicyName="root",
                        PolicyDocument={
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Action": ["logs:*"],
                                    "Resource": "arn:aws:logs:*:*:*",
                                    "Effect": "Allow",
                                },
                                {
                                    "Action": ["lambda:*"],
                                    "Resource": "*",
                                    "Effect": "Allow",
                                },
                            ],
                        },
                    )
                ],
                AssumeRolePolicyDocument={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Action": ["sts:AssumeRole"],
                            "Effect": "Allow",
                            "Principal": {"Service": ["lambda.amazonaws.com"]},
                        }
                    ],
                },
            )
        )

        # Lambda function
        self.access_analyzer_lambda_function = self.add_resource(
            Function(
                "AccessAnalyzerLambdaFunction",
                Handler="index.lambda_handler",
                # grabs the lambda source code from the module
                Code=Code(
                    ZipFile=inspect.getsource(
                        pyiamanalyzer.lambdas.access_analyzer_alerting
                    )
                ),
                FunctionName="pyiamanalyzer-access-analyzer-alerting",
                Role=GetAtt(self.access_analyzer_lambda_execution_role, "Arn"),
                Runtime="python3.11",
                MemorySize=128,
                Timeout=900,
            )
        )
