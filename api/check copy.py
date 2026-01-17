# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import os
import requests
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def log(message ):
    print(message, file=sys.stderr)

def get_exchange_rates(pairs):
    try:
        pairs_str = ",".join(pairs)
        url = f"https://economia.awesomeapi.com.br/last/{pairs_str}"
        log(f"Consultando API: {url}" )
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log(f"Erro na API: {e}")
        return None

def send_email(alerts):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")
    
    if not all([sender, password, receiver]):
        log("Erro: Variáveis de e-mail não configuradas.")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Alerta de Cambio: Oportunidade!"
    
    body = "Moedas em baixa:\n\n"
    for alert in alerts:
        body += f"- {alert['name']}: R$ {alert['rate']:.4f} (Limite: {alert['threshold']:.4f})\n"
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        log("E-mail enviado com sucesso!")
        return True
    except Exception as e:
        log(f"Erro ao enviar e-mail: {e}")
        return False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        log("Iniciando verificação de câmbio...")
        
        pairs = os.getenv("CURRENCY_PAIRS", "USD-BRL,EUR-BRL").split(",")
        thresholds = [float(v) for v in os.getenv("THRESHOLD_VALUES", "5.00,6.00").split(",")]
        
        data = get_exchange_rates(pairs)
        alerts = []
        
        if data:
            for i, pair in enumerate(pairs):
                key = pair.replace("-", "")
                threshold = thresholds[i] if i < len(thresholds) else thresholds[-1]
                if key in data:
                    rate = float(data[key]["bid"])
                    log(f"Moeda: {key} | Atual: {rate} | Limite: {threshold}")
                    if rate <= threshold:
                        alerts.append({'name': data[key]["name"], 'rate': rate, 'threshold': threshold})
            
            if alerts:
                send_email(alerts)
                res_msg = f"Alerta enviado para {len(alerts)} moedas."
            else:
                res_msg = "Nenhuma moeda abaixo do limite."
        else:
            res_msg = "Falha ao obter dados da API."

        log(f"Resultado: {res_msg}")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(res_msg.encode('utf-8'))
        return
