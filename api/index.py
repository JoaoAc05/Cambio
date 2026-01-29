import os
from dotenv import load_dotenv
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

load_dotenv() 

# Configurações
AWESOME_API_KEY = os.environ.get("KEY_AWESOMEAPI")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TARGET = EMAIL_USER

LIMIT_USD = 5.20
LIMIT_EUR = 6.00


def get_exchange_rates_awesome():
    if not AWESOME_API_KEY:
        print("[WARN] AWESOME_API_KEY não configurada.")
        return None, None

    print("[INFO] Tentando AwesomeAPI...")
    url = f"https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL?token={AWESOME_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        usd = float(data['USDBRL']['bid'])
        eur = float(data['EURBRL']['bid'])
        return usd, eur
    except Exception as e:
        print(f"[WARN] Erro na AwesomeAPI: {e}")
        return None, None

def get_exchange_rates_fallback():
    print("[INFO] Tentando Fallback...")
    url = "https://api.frankfurter.app/latest?from=USD,EUR&to=BRL"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # USD to BRL
        res_usd = requests.get("https://api.frankfurter.app/latest?from=USD&to=BRL", timeout=10)
        usd = res_usd.json()['rates']['BRL']
        
        # EUR to BRL
        res_eur = requests.get("https://api.frankfurter.app/latest?from=EUR&to=BRL", timeout=10)
        eur = res_eur.json()['rates']['BRL']
        
        return float(usd), float(eur)
    except Exception as e:
        print(f"[WARN] Erro no Fallback: {e}")
        return None, None

def send_email(usd, eur):
    if not EMAIL_USER or not EMAIL_PASS:
        print("[WARN] Credenciais de e-mail não configuradas. Pulando envio.")
        return

    subject = "❗ALERTA: Câmbio abaixo do limite❗"
    body = f"""
    Olá,
    
    O bot de verificação de câmbio detectou valores abaixo do limite estabelecido:
    
    - Dólar (USD): R$ {usd:.2f} (Limite: R$ {LIMIT_USD:.2f})
    - Euro (EUR): R$ {eur:.2f} (Limite: R$ {LIMIT_EUR:.2f})
    
    Data da consulta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    """
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TARGET
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Configuração para Gmail (pode ser alterada conforme o provedor)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("[INFO] E-mail enviado com sucesso!")
    except Exception as e:
        print(f"[WARN] Erro ao enviar e-mail: {e}")

def handler(request, response):
    print("[INFO] Iniciando consulta.")
    usd, eur = get_exchange_rates_awesome()
    
    if usd is None or eur is None:
        usd, eur = get_exchange_rates_fallback()

    email_sent: False
        
    if usd is not None or eur is not None:
        print(f"[INFO] Cotações obtidas - USD: {usd}, EUR: {eur}")
        if usd < LIMIT_USD or eur < LIMIT_EUR:
            send_email(usd, eur)
            email_sent = True
        else:
            print("[INFO] Valores acima do limite.")
    else:
        print("[WARN] Não foi possível obter as cotações.")

    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response.write(json.dumps({
        "usd": usd,
        "eur": eur,
        "email_sent": email_sent
    }))

# if __name__ == "__main__":
#     # Para execução local
#     handler(None)
