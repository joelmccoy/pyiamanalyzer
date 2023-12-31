import json


# TODO: Implement actual functionality
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "ok",
            }
        ),
    }
