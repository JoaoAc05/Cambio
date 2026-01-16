# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def get_exchange_rates(pairs):
    try:
        pairs_str = ",".join(pairs)
        url = f"https://economia.awesomeapi.com.br/last/{pairs_str}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        return None

def send_email(alerts):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not all([sender, password, receiver]):
        return False

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Alerta de Câmbio: Oportunidade de Compra!"
    
    body = "As seguintes moedas atingiram valores favoráveis:\n\n"
    for alert in alerts:
        body += f"- {alert['name']}: R$ {alert['rate']:.4f} (Limite: R$ {alert['threshold']:.4f})\n"
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
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
                    if rate <= threshold:
                        alerts.append({'name': data[key]["name"], 'rate': rate, 'threshold': threshold})
            
            if alerts:
                if send_email(alerts):
                    res_msg = "Alerta enviado com sucesso!"
                else:
                    res_msg = "Falha ao enviar e-mail."
            else:
                res_msg = "Nenhuma moeda abaixo do limite."
        else:
            res_msg = "Falha ao obter cotações."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(res_msg.encode('utf-8'))
        return
