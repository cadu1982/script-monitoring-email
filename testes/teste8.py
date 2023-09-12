import msal
import requests

# Defina as informações do aplicativo (obtidas no portal do Azure AD)
client_id = "XXXXXXXXXXXXXXXXXXX"
client_secret = "XXXXXXXXXXXXXXXXXXXXXX"
tenant_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Inicialize o objeto MSAL para autenticação
authority = f"https://login.microsoftonline.com/{tenant_id}"
app = msal.ConfidentialClientApplication(client_id, client_credential=client_secret, authority=authority)

# Obtenha um token de acesso
result = app.acquire_token_for_client(scopes=["https://outlook.office365.com/.default"])
access_token = result.get("access_token")

# Use o token de acesso para acessar a caixa de correio
if access_token:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    user_email = "devops.cards@bancoarbi.com.br"  # Substitua pelo endereço de email real do usuário
    # Exemplo: obter a lista de mensagens na caixa de entrada
    response = requests.get("https://outlook.office365.com/api/v2.0/{user_email}/messages", headers=headers)
    
    if response.status_code == 200:
        print("Lista de mensagens na caixa de entrada:")
        print(response.json())
    else:
        print("Falha ao acessar a caixa de entrada:", response.status_code)
else:
    print("Falha na obtenção do token de acesso")
