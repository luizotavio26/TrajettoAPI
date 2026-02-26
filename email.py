import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    print("⏳ Aguarde... seu e-mail está sendo preparado e enviado.")

    # Configurações do servidor SMTP
    servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_email.starttls()
    servidor_email.login('Seu_email@gmail.com', 'sua_senha_APP')

    # Montagem do e-mail
    remetente = 'Seu_email@gmail.com'
    destinatarios = ['destinatarios@gmail.com']

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = ", ".join(destinatarios)
    mensagem['Subject'] = "Teste de envio com Python"

    corpo = "Olá, este é um e-mail de teste enviado com sucesso via Python!"
    mensagem.attach(MIMEText(corpo, 'plain'))

    # Envio
    servidor_email.sendmail(remetente, destinatarios, mensagem.as_string())

    print("✅ E-mail enviado com sucesso!")

except Exception as e:
    print(f"❌ Erro ao enviar e-mail: {e}")

#finally:
    #servidor_email.quit()


#==================================
'''import smtplib
try:
    servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_email.starttls()
    servidor_email.login('professorvandersonbossi@gmail.com', 'sdlxtrpxgokbegss')
    
    remetente = 'professorvandersonbossi@gmail.com'
    destinatarios = ['vanderson.bossi@hotmail.com']
    conteudo = 'Ola, este e um email de teste.'
    
    servidor_email.sendmail(remetente, destinatarios, conteudo)
except Exception as e:
    print(f"Erro ao enviar email: {e}")
finally:
    servidor_email.quit()'''



#=============================================
'''import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

remetente = "professorvandersonbossi@gmail.com"
senha = "sdlxtrpxgokbegss"
destinatario = "vanderson.bossi@hotmail.com"

msg = MIMEMultipart()
msg['From'] = remetente
msg['To'] = destinatario
msg['Subject'] = "Confirmação de Envio"

corpo = "Olá, este é um e-mail de teste com acentuação."

msg.attach(MIMEText(corpo, 'plain', 'utf-8'))

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(remetente, senha)
    server.send_message(msg)'''
