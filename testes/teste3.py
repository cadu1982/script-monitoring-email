import msal
import requests

# Defina as informações do aplicativo (obtidas no portal do Azure AD)
client_id = "XXXXXXXXXXXXXXXXXXX"
client_secret = "XXXXXXXXXXXXXXXXXXXXXX"
tenant_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"

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
# if "access_token" in result:
#     print("Access token is " + result["access_token"])

# ...

# if "access_token" in result:
#     userId = "devops.cards@bancoarbi.com.br"
    
#     # Listar todas as pastas na caixa de correio do usuário
#     folders_url = f'https://graph.microsoft.com/v1.0/users/{userId}/mailFolders'
#     folders_response = requests.get(folders_url, headers={'Authorization': 'Bearer ' + result['access_token']})
    
#     if folders_response.ok:
#         folders_data = folders_response.json()
        
#         # Iterar pelas pastas para encontrar a pasta desejada (por exemplo, 'Lidos')
#         for folder in folders_data['value']:
#             if folder['displayName'] == 'Lidos':
#                 folder_id = folder['id']
                
#                 # Agora você tem o ID da pasta 'Lidos'
#                 print(f"ID da pasta 'Lidos': {folder_id}")
                
#                 # Continuar com o código para marcar emails como lidos e movê-los para esta pasta
#                 # ...

#     else:
#         print(f"Não foi possível listar as pastas: {folders_response.json()}")
# else:
#     print(result.get("error"))
#     print(result.get("error_description"))
#     print(result.get("correlation_id"))


if "access_token" in result:
    userId = "devops.cards@bancoarbi.com.br"
    endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/mailFolders/inbox/messages?$select=sender,subject,isRead,body'
    r = requests.get(endpoint,
                     headers={'Authorization': 'Bearer ' + result['access_token']})
    if r.ok:
        print('Retrieved emails successfully')
        data = r.json()
        for email in data['value']:
            email_id = email['id']
            sender_name = email['sender']['emailAddress']['name']
            subject = email['subject']
            is_read = email['isRead']
            body = email['body']['content']
            
            if not is_read:
                # O email não foi lido, você pode processá-lo aqui.
                print(f"Sender: {sender_name}")
                print(f"Subject: {subject}")
                print(f"Body: {body}")
            
                patch_url = f'https://graph.microsoft.com/v1.0/me/messages/{email_id}'
                patch_headers = {
                    'Authorization': 'Bearer ' + result['access_token'],
                    'Content-Type': 'application/json',
                }
                patch_data = {
                    'isRead': True,
                }
                patch_response = requests.patch(patch_url, headers=patch_headers, json=patch_data)
                if patch_response.ok:
                    print("Email marcado como lido com sucesso.")
                else:
                    print("Falha ao marcar o email como lido.")
                
                # Move the email to a different folder (e.g., 'Lidos')
                # move_url = f'https://graph.microsoft.com/v1.0/me/messages/{email_id}/move'
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