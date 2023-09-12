import msal
import requests

c# Defina as informações do aplicativo (obtidas no portal do Azure AD)
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

if "access_token" in result:
    userId = "devops.cards@bancoarbi.com.br"
    endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/messages?$select=sender,subject'
    r = requests.get(endpoint,
                     headers={'Authorization': 'Bearer ' + result['access_token']})
    if r.ok:
        print('Retrieved emails successfully')
        data = r.json()
        print(data)
        # for email in data['value']:
        #     print(email['subject'] + ' (' + email['sender']
        #           ['emailAddress']['name'] + ')')
    else:
        print(r.json())
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))