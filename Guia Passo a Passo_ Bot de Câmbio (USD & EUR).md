# Guia Passo a Passo: Bot de Câmbio (USD & EUR)

Este guia explica como configurar, testar e colocar seu bot para rodar automaticamente.

---

## 1. Preparação do E-mail (Gmail)
Para que o bot envie e-mails, você **não** deve usar sua senha normal. Você precisa de uma "Senha de App".
1. Acesse sua [Conta Google](https://myaccount.google.com/).
2. Vá em **Segurança**.
3. Ative a **Verificação em duas etapas**.
4. Procure por **Senhas de App** (no final da página de segurança).
5. Crie uma nova senha chamada "Bot Cambio" e copie o código de 16 dígitos gerado. **Este código será sua `EMAIL_PASSWORD`**.

---

## 2. Como Rodar Manualmente (No seu PC)
1. **Instale o Python**: Certifique-se de ter o Python instalado.
2. **Baixe os arquivos**: Coloque todos os arquivos em uma pasta.
3. **Instale as dependências**:
   Abra o terminal na pasta e digite:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure as variáveis**:
   - Renomeie o arquivo `.env.example` para `.env`.
   - Abra o `.env` e coloque seu e-mail e a senha de app que você gerou.
   - Ajuste os valores de `THRESHOLD_VALUES` para o preço que você deseja (ex: 5.10 para dólar e 5.50 para euro).
5. **Execute**:
   ```bash
   python main.py
   ```
   O bot fará uma verificação imediata e depois ficará rodando, verificando às 09:00 e 15:00.

---

## 3. Como Rodar Sozinho na Vercel (Grátis)
A Vercel permite rodar scripts via "Cron Jobs" (tarefas agendadas).

### Passo A: Preparar o GitHub
1. Crie um repositório no seu GitHub (ex: `meu-bot-cambio`).
2. Suba todos os arquivos para lá (`main.py`, `requirements.txt`, `vercel.json`, pasta `api/`, etc).

### Passo B: Configurar na Vercel
1. Vá para [Vercel.com](https://vercel.com/) e faça login com seu GitHub.
2. Clique em **Add New** > **Project**.
3. Importe o repositório que você criou.
4. **IMPORTANTE**: Antes de clicar em Deploy, vá em **Environment Variables** e adicione todas as variáveis do seu arquivo `.env`:
   - `CURRENCY_PAIRS`
   - `THRESHOLD_VALUES`
   - `EMAIL_SENDER`
   - `EMAIL_PASSWORD`
   - `EMAIL_RECEIVER`
5. Clique em **Deploy**.

### Passo C: Ativar o Agendamento (Cron)
1. No painel do seu projeto na Vercel, vá na aba **Settings**.
2. Procure por **Cron Jobs**.
3. O arquivo `vercel.json` já configurou o caminho `/api/check` para rodar às 10:00 e 16:00 (horário UTC).
   *Nota: O horário da Vercel é UTC. 10:00 UTC é 07:00 no Brasil (Brasília).*

---

## 4. Resumo das Variáveis no `.env`
| Variável | Exemplo | Descrição |
| :--- | :--- | :--- |
| `CURRENCY_PAIRS` | `USD-BRL,EUR-BRL` | Moedas para monitorar |
| `THRESHOLD_VALUES` | `5.20,5.80` | Preços limites (na mesma ordem) |
| `EMAIL_SENDER` | `seu@gmail.com` | Seu e-mail de envio |
| `EMAIL_PASSWORD` | `xxxx xxxx xxxx xxxx` | Senha de App do Google |
| `EMAIL_RECEIVER` | `seu@gmail.com` | E-mail que recebe o alerta |
