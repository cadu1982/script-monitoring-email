import poplib

# Configurações do servidor POP3
pop3_server = "outlook.office365.com"  # Substitua pelo endereço do servidor POP3
port = 995  # Porta segura para POP3 (SSL/TLS)

# Nome de usuário e senha
username = 'example@examplo.com.br'  # Substitua pelo seu endereço de e-mail
password ="your_pwd"  # Substitua pela sua senha

try:
    # Conectar ao servidor POP3 usando SSL/TLS
    pop3 = poplib.POP3_SSL(pop3_server, port)

    # Exibir uma mensagem de boas-vindas do servidor (opcional)
    print(pop3.getwelcome())

    # Autenticar com o servidor
    pop3.user(username)
    pop3.pass_(password)

    # Listar as caixas de correio disponíveis (opcional)
    mailbox_list = pop3.list()
    print("Caixas de correio disponíveis:")
    for mailbox in mailbox_list[1]:
        print(mailbox.decode())

    # Escolher a caixa de correio que você deseja acessar (por padrão, a primeira caixa)
    mailbox_number = 1
    num_messages, mailbox_size = pop3.select(str(mailbox_number))

    print(f"Total de mensagens na caixa: {num_messages}")

    # Obter as mensagens da caixa de correio
    for msg_number in range(1, num_messages + 1):
        msg_data = pop3.retr(msg_number)
        msg_lines = msg_data[1]
        msg_content = b'\n'.join(msg_lines).decode('utf-8')
        print(f"\nMensagem {msg_number}:\n{msg_content}")

    # Sair da caixa de correio
    pop3.quit()

except Exception as e:
    print(f"Erro: {e}")
