import requests
import os


# Configurações da API do Azure DevOps
organization = "your_organization"
project = "your_project"
personal_access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"

            
# Extrair remetente, assunto e corpo da mensagem
remetente = "carlos"
assunto = "nova tarefa"
corpo_mensagem = "nova mensagem"

# Enviar os dados para o Azure DevOps Boards usando a API
url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$task?api-version=7.0"
headers = {
    "Content-Type": "application/json-patch+json; charset=utf-8",
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

