# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import os
import requests
import sys

class handler(BaseHTTPRequestHandler ):
    def do_GET(self):
        # 1. Tenta ler as variáveis
        pairs_raw = os.getenv("CURRENCY_PAIRS", "USD-BRL,EUR-BRL")
        
        # 2. Tenta consultar a API
        url = f"https://economia.awesomeapi.com.br/last/{pairs_raw}"
        
        try:
            response = requests.get(url, timeout=10 )
            status = response.status_code
            if status == 200:
                data = response.json()
                res_msg = f"SUCESSO! API respondeu para: {list(data.keys())}"
            else:
                res_msg = f"ERRO API: Status {status} para a URL: {url}"
        except Exception as e:
            res_msg = f"ERRO DE CONEXAO: {str(e)}"

        # 3. Responde no navegador para você ver na hora
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(res_msg.encode('utf-8'))
