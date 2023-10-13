'''
This is a sample Lambda function that is triggered by a GitHub webhook.
The code is not runnable as is, credentails need to be filled in.
A better approach would be using AWS Secrets Manager, but it's not free.
For the purpose of this example, the credentials are hardcoded in the code.
Use requests==2.27.0
'''
import requests

def lambda_handler(event, context):
    # can get workflow id from https://api.github.com/repos/<username>/<repository>/actions/workflows
    url = "https://api.github.com/repos/<username>/<repository>/actions/workflows/<workflow-id>/dispatches"
    # 
    headers = {
        "Authorization": "Bearer YOUR_GITHUB_PERSONAL_ACCESS_TOKEN",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.post(url, headers=headers)
   
    if response.status_code == 204:
        return {
            'statusCode': 200,
            'body': 'Workflow triggered successfully!'
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': 'Failed to trigger workflow!'
        }
