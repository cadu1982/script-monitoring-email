import imaplib
import email
import os

# Configurações IMAP e informações da conta de e-mail
imap_server = os.getenv('IMAP_SERVER') # Substitua pelo endereço do seu servidor IMAP
username = os.getenv('ACCOUNT_EMAIL')  # Substitua pelo seu endereço de e-mail
password = os.getenv('PWD')    # Substitua pela sua senha

mail = imaplib.IMAP4_SSL(imap_server, port=995)
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
            print(f"::set-output name=SOLICITANTE::{'Solicitante:' + remetente}")
            assunto = msg["Subject"]
            print(f"::set-output name=TITLE::{assunto}")
            corpo_mensagem = msg.get_payload()
            print(f"::set-output name=DESCRICAO::{corpo_mensagem}")
        else:
            print("Erro ao buscar e-mail:", status)

# Fechar a conexão com o servidor IMAP
mail.logout()
