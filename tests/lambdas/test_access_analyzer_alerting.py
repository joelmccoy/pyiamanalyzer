import pyiamanalyzer.lambdas.access_analyzer_alerting as access_analyzer_alerting


def test_lambda_handler():
    """
    Tests the lambda_handler function.
    """
    response = access_analyzer_alerting.lambda_handler({}, {})
    assert response["statusCode"] == 200
    assert response["body"] == '{"message": "ok"}'
