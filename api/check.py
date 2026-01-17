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
        # Configurações
        api_key = os.getenv("EXCHANGE_RATE_API_KEY", "61471d6335fab5571e8994864f342cda339da59144c361b825ba0ff12b941f90") # Use a sua chave aqui
        threshold_usd = float(os.getenv("THRESHOLD_USD", "5.20"))
        threshold_eur = float(os.getenv("THRESHOLD_EUR", "6.00"))
        
        alerts = []
        
        # Consulta Dólar e Euro (Base USD para facilitar)
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
        
        try:
            log(f"Consultando nova API..." )
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get("conversion_rates", {})
                
                # Valor do Dólar em BRL
                usd_brl = rates.get("BRL")
                if usd_brl:
                    log(f"USD-BRL: {usd_brl}")
                    if usd_brl <= threshold_usd:
                        alerts.append({'name': 'Dólar Americano', 'rate': usd_brl, 'threshold': threshold_usd})
                
                # Valor do Euro em BRL (Calculado via paridade se necessário, ou consulta direta)
                # Para ser mais preciso, consultamos o Euro também
                url_eur = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/EUR"
                response_eur = requests.get(url_eur, timeout=15 )
                if response_eur.status_code == 200:
                    eur_brl = response_eur.json().get("conversion_rates", {}).get("BRL")
                    log(f"EUR-BRL: {eur_brl}")
                    if eur_brl and eur_brl <= threshold_eur:
                        alerts.append({'name': 'Euro', 'rate': eur_brl, 'threshold': threshold_eur})

                if alerts:
                    self.send_alert_email(alerts)
                    res_msg = f"Alerta enviado para {len(alerts)} moedas."
                else:
                    res_msg = "Cotações verificadas. Valores acima do limite."
            else:
                res_msg = f"Erro na nova API: Status {response.status_code}. Verifique sua API Key."
                
        except Exception as e:
            res_msg = f"Erro: {str(e)}"

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
        msg['Subject'] = "Alerta de Cambio: Oportunidade!"
        body = "Moedas em baixa:\n\n" + "\n".join([f"- {a['name']}: R$ {a['rate']:.4f}" for a in alerts])
        msg.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            log(f"Erro e-mail: {e}")
