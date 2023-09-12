from imapclient import IMAPClient

# Configurações IMAP e informações da conta de e-mail
imap_server = "outlook.office365.com" # Substitua pelo endereço do seu servidor IMAP
username = "exemplo@exemplo.com.br"  # Substitua pelo seu endereço de e-mail
password = "XXXXXXXXXX"   

client = IMAPClient(imap_server, ssl=True)
client.login(username, password)

client.select_folder('INBOX', readonly=True)
result = client.search()
print(result)

folder_list = client.list_folder()
print(folder_list)

client.logout()
