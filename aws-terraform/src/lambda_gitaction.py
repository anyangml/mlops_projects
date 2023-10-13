'''
This is a sample Lambda function that is triggered by a GitHub webhook.
The code is not runnable as is, credentails need to be filled in.
A better approach would be using AWS Secrets Manager, but it's not free.
For the purpose of this example, the credentials are hardcoded in the code.
'''
import requests

def lambda_handler(event, context):
    url = "https://api.github.com/repos/<username>/<repository>/actions/workflows/<workflow-file-name>/dispatches"
    # 
    headers = {
        "Authorization": "Bearer YOUR_GITHUB_PERSONAL_ACCESS_TOKEN",
        "Accept": "application/vnd.github.v3+json"
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
