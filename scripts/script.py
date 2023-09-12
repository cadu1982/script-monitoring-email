import msal
import requests
import os
import subprocess

client_id = os.getenv('APP_ID')
client_secret = os.getenv('APP_SECRET')
tenant_id = os.getenv('TENANT_ID')
userId = os.getenv('ACCOUNT_EMAIL')
project = os.getenv('PROJECT')
url_azure_devops = os.getenv('URL_AZURE_DEVOPS')

authority = f"https://login.microsoftonline.com/{tenant_id}"

app = msal.ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority)

scopes = ["https://graph.microsoft.com/.default"]
result = None
result = app.acquire_token_silent(scopes, account=None)

if not result:
    print(
        "No suitable token exists in cache. Let's get a new one from Azure Active Directory.")
    result = app.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/mailFolders/inbox/messages?$select=sender,subject,isRead,body'
    r = requests.get(endpoint,
                     headers={'Authorization': 'Bearer ' + result['access_token']})
    if r.ok:
        print('loged successfully')
        data = r.json()
        for email in data['value']:
            email_id = email['id']
            sender_info = email['sender']['emailAddress']
            sender_name = sender_info['name']
            sender_address = sender_info['address']
            subject = email['subject']
            is_read = email['isRead']
            body = email['body']['content']
                        
            if not is_read:
                comando = [
                            "az",
                            "boards",
                            "work-item",
                            "create",
                            "--org",
                            url_azure_devops,
                            "--type",
                            "issue",
                            "--project",
                            project,
                            "--title",
                            subject,
                            "--description",
                            body + ' Solicitante: ' + sender_name + ' E-mail: ' + sender_address
                        ]
                resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                                           
                # Move the email to a different folder (e.g., 'Lidos')
                move_url = f'https://graph.microsoft.com/v1.0/users/{userId}/mailFolders/inbox/messages/{email_id}/move'
                move_headers = {
                    'Authorization': 'Bearer ' + result['access_token'],
                    'Content-Type': 'application/json',
                }
                move_data = {
                    'destinationId': 'AQMkADlmNWZlNTdkLTJmYzEtNDg0Zi05MWE1LTRhNDg3ZWYwNWRjOQAuAAADrUKxg2WySkStZgk825emlgEAuX0IEpx1tEqBI4NcJ2OtewAAAc16VwAAAA==',  
                }
                move_response = requests.post(move_url, headers=move_headers, json=move_data)
                if move_response.ok:
                    print("Email moved to 'Lidos' folder successfully.")
                else:
                    print("Failed to move the email to 'Lidos' folder.")
    else:
        print(r.json())
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))