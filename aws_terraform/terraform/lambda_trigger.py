"""
This is a sample Lambda function that is triggered by a GitHub webhook.
The code is not runnable as is, credentails need to be filled in.
A better approach would be using AWS Secrets Manager, but it's not free.
For the purpose of this example, the credentials are hardcoded in the code.
"""
import requests


def lambda_handler(event, context):
    url = "https://api.github.com/repos/anyangml/mlops_projects/actions/workflows/72577098/dispatches"
    #
    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = '{"ref": "main","inputs": {}}'
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 204:
        return {"statusCode": 200, "body": "Workflow triggered successfully!"}
    else:
        return {"statusCode": response.status_code, "body": "Failed to trigger workflow!"}
