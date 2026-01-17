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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Configurações
        pairs_raw = os.getenv("CURRENCY_PAIRS", "USD-BRL,EUR-BRL")
        thresholds_raw = os.getenv("THRESHOLD_VALUES", "5.20,6.00")
        
        pairs = pairs_raw.split(",")
        thresholds = [float(v) for v in thresholds_raw.split(",")]
        
        # 2. Consulta API
        url = f"https://economia.awesomeapi.com.br/last/{pairs_raw}"
        log(f"Consultando: {url}" )
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                alerts = []
                
                for i, pair in enumerate(pairs):
                    key = pair.replace("-", "")
                    threshold = thresholds[i] if i < len(thresholds) else thresholds[-1]
                    
                    if key in data:
                        rate = float(data[key]["bid"])
                        name = data[key]["name"]
                        log(f"{name}: {rate} (Limite: {threshold})")
                        if rate <= threshold:
                            alerts.append({'name': name, 'rate': rate, 'threshold': threshold})
                
                # 3. Envio de E-mail
                if alerts:
                    self.send_alert_email(alerts)
                    res_msg = f"Sucesso! Alerta enviado para {len(alerts)} moedas."
                else:
                    res_msg = "Consulta OK. Nenhuma moeda abaixo do limite."
            else:
                res_msg = f"Erro na API: Status {response.status_code}"
                
        except Exception as e:
            res_msg = f"Erro no processamento: {str(e)}"

        log(res_msg)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(res_msg.encode('utf-8'))

    def send_alert_email(self, alerts):
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        receiver = os.getenv("EMAIL_RECEIVER")
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "Alerta de Cambio: Oportunidade de Compra!"
        
        body = "As seguintes moedas atingiram o valor desejado:\n\n"
        for a in alerts:
            body += f"- {a['name']}: R$ {a['rate']:.4f} (Seu limite: R$ {a['threshold']:.4f})\n"
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()
            log("E-mail enviado!")
        except Exception as e:
            log(f"Falha ao enviar e-mail: {e}")
