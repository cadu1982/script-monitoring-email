# remetente = "carlos"
# print(f"::set-output name=SOLICITANTE::{'Solicitante:' + remetente}")
# assunto = "criar secrets"
# print(f"::set-output name=TITLE::{assunto}")
# corpo_mensagem = "criar seceets produção"
# print(f"::set-output name=DESCRICAO::{corpo_mensagem}")

remetente = "carlos"
assunto = "criar secrets"
corpo_mensagem = "criar seceets produção"

# Combinar remetente e corpo da mensagem com uma quebra de linha
descricao = f"Solicitante: {remetente}\n{corpo_mensagem}"

# Definir as variáveis de saída
print(f"::set-output name=TITLE::{assunto}")
print(f"::set-output name=DESCRICAO::{descricao}")
print(f"::set-output name=DESCRICAO::{descricao}")

