import os
import requests
import smtplib
import time
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações de E-mail
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Configurações de Moedas (Pares separados por vírgula e limites correspondentes)
# Exemplo: USD-BRL,EUR-BRL
CURRENCY_PAIRS = os.getenv("CURRENCY_PAIRS", "USD-BRL,EUR-BRL").split(",")
# Exemplo: 5.25,6.05
THRESHOLD_VALUES = [float(v) for v in os.getenv("THRESHOLD_VALUES", "5.20,6.00").split(",")]

def get_exchange_rates():
    try:
        pairs_str = ",".join(CURRENCY_PAIRS)
        url = f"https://economia.awesomeapi.com.br/last/{pairs_str}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao buscar cotações: {e}")
        return None

def send_email(alerts):
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        print("Configurações de e-mail incompletas.")
        return

    subject = "Alerta de Câmbio💸: Oportunidade de Compra!"
    
    body = "As seguintes moedas atingiram valores favoráveis:\n\n"
    for alert in alerts:
        body += (f"- {alert['name']}\n"
                 f"  Valor Atual: R$ {alert['rate']:.4f}\n"
                 f"  Minimo Definido: R$ {alert['threshold']:.4f}\n\n")
    
    body += f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    body += "Este é um aviso automático do Bot de Câmbio."

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"E-mail de alerta enviado para {EMAIL_RECEIVER}!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def check_and_notify():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Verificando cotações...")
    data = get_exchange_rates()
    if not data:
        return

    alerts = []
    for i, pair in enumerate(CURRENCY_PAIRS):
        key = pair.replace("-", "")
        threshold = THRESHOLD_VALUES[i] if i < len(THRESHOLD_VALUES) else THRESHOLD_VALUES[-1]
        
        if key in data:
            rate = float(data[key]["bid"])
            name = data[key]["name"]
            print(f"{name}: {rate:.4f} (Limite: {threshold:.4f})")
            if rate <= threshold:
                alerts.append({'name': name, 'rate': rate, 'threshold': threshold})
    
    if alerts:
        send_email(alerts)
    else:
        print("Nenhuma moeda abaixo da faixa.")

def run_scheduler():
    # Agendamento
    schedule.every().day.at("09:00").do(check_and_notify)
    schedule.every().day.at("16:00").do(check_and_notify)
    
    print(f"Bot iniciado. Monitorando: {', '.join(CURRENCY_PAIRS)}")
    check_and_notify() # Teste imediato

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
