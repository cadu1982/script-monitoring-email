import imaplib
import email
import requests

# Configurações IMAP e informações da conta de e-mail
imap_server = "outlook.office365.com" # Substitua pelo endereço do seu servidor IMAP
username = "example@example.com.br"  # Substitua pelo seu endereço de e-mail
password = "pwd"             # Substitua pela sua senha

# Configurações da API do Azure DevOps
organization = "your_organization"
project = "your_project"
personal_access_token = "your_token"

# Conecte-se ao servidor IMAP
mail = imaplib.IMAP4_SSL(imap_server, port=993)
mail.login(username, password)
mail.select("inbox")

# Pesquise por e-mails não lidos
status, email_ids = mail.search(None, "UNSEEN")

if status == "OK":
    email_id_list = email_ids[0].split()
    
    for email_id in email_id_list:
        # Busque o e-mail pelo ID
        status, email_data = mail.fetch(email_id, "(RFC822)")
        
        if status == "OK":
            raw_email = email_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extrair remetente, assunto e corpo da mensagem
            remetente = msg["From"]
            assunto = msg["Subject"]
            corpo_mensagem = msg.get_payload()
            
            # Enviar os dados para o Azure DevOps Boards usando a API
            url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$task?api-version=7.0"
            headers = {
                "Content-Type": "application/json-patch+json",
                "Authorization": f"Basic {personal_access_token}"
            }
            data = [
                {
                    "op": "add",
                    "path": "/fields/System.Title",
                    "value": assunto
                },
                {
                    "op": "add",
                    "path": "/fields/System.Description",
                    "value": corpo_mensagem
                }
            ]
            
            response = requests.patch(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"Nova tarefa criada no Azure DevOps Boards com assunto: {assunto}")
            else:
                print(f"Erro ao criar a tarefa no Azure DevOps Boards: {response.text}")
        else:
            print("Erro ao buscar e-mail:", status)

# Fechar a conexão com o servidor IMAP
mail.logout()
