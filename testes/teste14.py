import msal
import requests
import os
import html
import subprocess

client_id = os.getenv('APP_ID')
client_secret = os.getenv('APP_SECRET')
tenant_id = os.getenv('TENANT_ID')
userId = os.getenv('ACCOUNT_EMAIL')

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
                            "https://dev.azure.com/<organization>/",
                            "--type",
                            "issue",
                            "--project",
                            "Geral",
                            "--title",
                            subject,
                            "--description",
                            body + sender_name + sender_address
                        ]
                resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                # subprocess.run(["az boards work-item create --org https://dev.azure.com/<organization>/ --type 'issue' --project 'Geral' --title 'carlos' --description 'este + Solicitante: + aquele, Email: + alguem"])
                # O email não foi lido, você pode processá-lo aqui.
                # print(f"Sender: {sender_name, sender_address}")
                # print(f"::set-output name=SOLICITANTE::{'Solicitante:' + sender_name, 'Email:' + sender_address}")
                # # # print(f"Subject: {subject}")
                # print(f"::set-output name=TITLE::{subject}")
                # # # print(f"Body: {body}")
                # # print(f"::set-env name=DESCRICAO::{body}")
                # with open("descricao.txt", "w") as file:
                #     file.write(body)
                # print("::set-output name=DESCRICAO::descricao.txt")
                # # env_file = os.getenv('GITHUB_ENV')
                # # with open(env_file, 'a') as myfile:
                #     myfile.write(f"DESCRICAO={body}\n")
                

                                            
                # Move the email to a different folder (e.g., 'Lidos')
                move_url = f'https://graph.microsoft.com/v1.0/users/{userId}/mailFolders/inbox/messages/{email_id}/move'
                move_headers = {
                    'Authorization': 'Bearer ' + result['access_token'],
                    'Content-Type': 'application/json',
                }
                move_data = {
                    'destinationId': 'AQMkADlmNWZlNTdkLTJmYzEtNDg0Zi05MWE1LTRhNDg3ZWYwNWRjOQAuAAADrUKxg2WySkStZgk825emlgEAuX0IEpx1tEqBI4NcJ2OtewAAAc16VwAAAA==',  # Replace with the actual folder ID
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