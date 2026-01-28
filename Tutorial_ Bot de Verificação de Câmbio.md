# Tutorial: Bot de Verificação de Câmbio

Este bot monitora as cotações do Dólar e Euro e envia um alerta por e-mail caso ambos estejam abaixo dos limites definidos (USD < 5.20 e EUR < 6.00).

## Estrutura do Projeto

- `api/index.py`: Script principal que realiza a consulta e envia o e-mail.
- `vercel.json`: Configuração para deploy na Vercel e agendamento do Cron Job.
- `requirements.txt`: Dependências do projeto.

## Instalação e Execução Local

### 1. Pré-requisitos
- Python 3.9 ou superior instalado.
- Uma conta de e-mail (ex: Gmail) para envio das notificações.

### 2. Instalação de Dependências
No terminal, dentro da pasta do projeto, execute:
```bash
pip install -r requirements.txt
```

### 3. Configuração de Variáveis de Ambiente
Para que o bot consiga enviar e-mails, você deve configurar as seguintes variáveis no seu sistema ou em um arquivo `.env`:
- `EMAIL_USER`: Seu endereço de e-mail.
- `EMAIL_PASS`: Sua senha de aplicativo (No Gmail, use "Senhas de App").
- `KEY_AWESOMEAPI`: Sua senha de api da AwesomeApi.

### 4. Execução Manual
```bash
python api/index.py
```

## Deploy na Vercel

### 1. Preparação
Certifique-se de ter a [Vercel CLI](https://vercel.com/docs/cli) instalada ou conecte seu repositório GitHub à Vercel.

### 2. Configuração de Variáveis na Vercel
No painel da Vercel, vá em **Settings > Environment Variables** e adicione:
- `EMAIL_USER`: Seu e-mail.
- `EMAIL_PASS`: Sua senha de aplicativo.

### 3. Cron Job
O arquivo `vercel.json` já está configurado para executar o bot diariamente às **13:00 (Horário de Brasília)**. 
> Nota: O horário no `vercel.json` está como `0 16 * * *` (UTC), que corresponde às 13:00 BRT.

## Segurança e Fallback
O bot utiliza a **AwesomeAPI** como fonte primária (usando sua chave de API). Caso a AwesomeAPI falhe, o bot automaticamente tenta consultar a **Frankfurter API** como alternativa de segurança.
