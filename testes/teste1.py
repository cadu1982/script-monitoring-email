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

# Use o token de acesso para acessar a caixa de correio de um usuário específico
if access_token:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Defina o endereço de email do usuário cuja caixa de correio você deseja acessar
    user_email = "devops.cards@bancoarbi.com.br"  # Substitua pelo endereço de email real do usuário

    # Exemplo: obter a lista de mensagens na caixa de entrada do usuário específico
    api_url = f"https://outlook.office365.com/api/v2.0/users/{user_email}/messages"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        print(f"Lista de mensagens na caixa de entrada de {user_email}:")
        print(response.json())
    else:
        print(f"Falha ao acessar a caixa de entrada de {user_email}:", response.status_code)
else:
    print("Falha na obtenção do token de acesso")
