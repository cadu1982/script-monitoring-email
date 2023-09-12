import imapclient

# Configurações do servidor IMAP (para o Gmail)
imap_server = "imap.gmail.com"
username = "seu_email@gmail.com"  # Substitua pelo seu endereço de e-mail
oauth2_token = "seu_token_oauth2"  # Substitua pelo seu token OAuth2

# Conecte-se ao servidor IMAP usando XOAUTH2
with imapclient.IMAPClient(imap_server) as client:
    # Use XOAUTH2 para autenticação
    client.oauth2_login(username, oauth2_token)
    
    # Selecionar a caixa de entrada (inbox)
    client.select_folder("inbox")
    
    # Pesquisar por e-mails não lidos
    message_ids = client.search(["UNSEEN"])
    
    for message_id in message_ids:
        # Buscar o e-mail pelo ID
        email_data = client.fetch([message_id], ["ENVELOPE"])
        
        envelope_data = email_data[message_id][b"ENVELOPE"]
        
        # Extrair o assunto do e-mail
        subject = envelope_data.subject.decode("utf-8")
        
        print("Assunto do E-mail:", subject)
