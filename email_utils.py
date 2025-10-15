# email_utils.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_contact_email(name, email, message):
    """
    Envia email quando alguém preenche o formulário de contato
    """
    try:
        # Configurações do servidor SMTP
        smtp_server = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        port = int(os.getenv('EMAIL_PORT', 587))
        username = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_PASSWORD')
        from_email = os.getenv('EMAIL_FROM', username)
        
        # Se email não está configurado, retorna False
        if not username or not password:
            print("⚠️ Email não configurado - variáveis de ambiente faltando")
            return False
        
        # Destinatário (você mesmo)
        to_email = from_email
        
        # Criar mensagem de email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f"📨 Novo contato do site - {name}"
        
        # Corpo do email
        body = f"""
        🎨 **Novo contato do portfólio AKIRA UMEDA**
        
        **Nome:** {name}
        **Email:** {email}
        
        **Mensagem:**
        {message}
        
        ---
        Enviado automaticamente pelo sistema do portfólio.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Enviar email
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Segurança
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        
        print("✅ Email enviado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False
