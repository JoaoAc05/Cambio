# Bot de Consulta de Câmbio

Este bot monitora a cotação de moedas 2 vezes ao dia e envia um alerta por e-mail quando o valor atinge um limite pré-definido.

## Como configurar

1. Clone este repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Copie o arquivo `.env.example` para `.env` e preencha com suas configurações:
   - `CURRENCY_PAIR`: Par de moedas (ex: USD-BRL, EUR-BRL).
   - `THRESHOLD_VALUE`: Valor limite para disparo do alerta.
   - `EMAIL_SENDER`: Seu e-mail (Gmail recomendado).
   - `EMAIL_PASSWORD`: Senha de aplicativo do seu e-mail (veja a documentação do Google sobre como gerar uma).
   - `EMAIL_RECEIVER`: E-mail que receberá os alertas.

## Como executar

```bash
python main.py
```

## Deploy na Render

Para manter o bot rodando 24/7 na Render (recomendado):
1. Crie uma conta gratuita na [Render](https://render.com/).
2. Crie um novo **Background Worker**.
3. Conecte seu repositório do GitHub onde o código está hospedado.
4. **Comando de Build**: `pip install -r requirements.txt`
5. **Comando de Start**: `python main.py`
6. Na seção "Environment", adicione as variáveis de ambiente do seu arquivo `.env`.

## Alternativa: Deploy na Vercel

A Vercel é mais focada em aplicações web e Serverless Functions. Para rodar este bot lá, seria necessário adaptar o script para o formato de **Cron Jobs** da Vercel, configurando um arquivo `vercel.json`. A abordagem com a Render é mais direta para este tipo de processo contínuo em segundo plano.
