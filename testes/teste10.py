import imaplib
import msal
import pprint

conf = {
    "authority": "https://login.microsoftonline.com/tenat_ID",
    "client_id": "xxxxxxxxxxxxxxxxxxxxxxxx", #AppID
    "scope": ['https://outlook.office365.com/.default'],
    "secret": "xxxxxxxxxxxxxxxxxxxxxx", #Key-Value
    "secret-id": "xxxxxxxxxxxxxxx", #Key-ID
}
    
def generate_auth_string(user, token):
    return f"user={user}\x01auth=Bearer {token}\x01\x01"    

if __name__ == "__main__":
    app = msal.ConfidentialClientApplication(conf['client_id'], authority=conf['authority'],
                                             client_credential=conf['secret'])

    result = app.acquire_token_silent(conf['scope'], account=None)

    if not result:
        print("No suitable token in cache.  Get new one.")
        result = app.acquire_token_for_client(scopes=conf['scope'])

    if "access_token" in result:
        print(result['token_type'])
        pprint.pprint(result)
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))
        
    imap = imaplib.IMAP4('outlook.office365.com')
    imap.starttls()
    imap.authenticate("XOAUTH2", lambda x: generate_auth_string("example@example.com.br", result['access_token']).encode("utf-8"))