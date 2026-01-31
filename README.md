# 💱 Alerta de Cotação de Câmbio

Aplicação desenvolvida em **Python** que realiza a consulta da cotação de moedas através de uma **API de câmbio** e envia um **alerta por e-mail** quando o valor atinge ou fica abaixo de um limite definido pelo usuário.

O projeto está implantado em ambiente **serverless na Vercel**, garantindo simplicidade, baixo custo e escalabilidade.

---

## 🚀 Funcionalidades
- 🔄 Consulta de cotação de moedas em tempo real
- 📉 Monitoramento baseado em valor mínimo configurável
- 📧 Envio automático de alerta por e-mail
- ⚡ Execução em ambiente serverless (Vercel)
- 🔐 Uso de variáveis de ambiente para dados sensíveis

---

<details>
<summary>
  Ver mais...
</summary>
  
## 🧠 Como funciona
1. A aplicação consulta uma API de câmbio.
2. Obtém a cotação atual da moeda desejada.
3. Compara o valor retornado com o limite definido.
4. Caso a cotação esteja **igual ou abaixo do valor configurado**, um e-mail de alerta é enviado ao usuário.
5. A execução pode ser feita manualmente ou de forma agendada (cron).

---

## 🛠️ Tecnologias Utilizadas
- **Python**
- **python-dotenv**
- **Requests** (consumo de API)
- **SMTP / Serviço de e-mail**
- **Vercel (Serverless Functions)**

---

## ⚙️ Variáveis de Ambiente
Configure as seguintes variáveis no arquivo `.env` ou diretamente no painel da Vercel:

```env
LIMIT_USDL= Valor_Minimo_Dolar
LIMIT_EUR= Valor_Minimo_Euro

EMAIL_USER= Seu_Email_Para_Envio
EMAIL_PASS= Senha_de_App

KEY_AWESOMEAPI= Key_AwesomeApi

```
</details>
