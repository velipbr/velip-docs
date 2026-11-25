# Build your integration with an AI agent

*Let ChatGPT, Claude, Claude Code or Cursor read the Velip docs and your system's docs, and write the integration for you, or give you a step-by-step guide.*

![An AI agent reads the Velip API docs and the CRM docs, then writes the integration code or a step-by-step guide. Afterwards, a CRM event calls a webhook, the webhook calls MakeTTSCall, the customer gets a call, and the result goes back to the CRM through rurl.](ai-integration.svg)

Most Velip integrations follow the same pattern. Something happens in your system (a new lead in the CRM, an overdue invoice, an appointment tomorrow), your system calls a webhook, and the webhook calls a Velip API: [`MakeTTSCall`](../api/v2/voice/MakeTTSCall.md) for a voice call, [`MakeSMS`](../api/v2/sms/MakeSMS.md) for SMS, [`MakeWhatsapp`](../api/v2/whatsapp/MakeWhatsapp.md) for WhatsApp. When the call ends, Velip can send the result back to your system.

Building this means reading two sets of docs, the Velip docs and your CRM's docs, and mapping one onto the other. AI agents do this well. This repository is plain Markdown so that an agent can read it directly.

The same approach works for two other integrations, each with its own prompt below: [calls from your own agent screen](#calls-from-your-own-agent-screen-webrtc) (a WebRTC softphone in the browser) and [buying credit automatically](#buy-credit-automatically) with PIX.

## What you need

- A Velip account with API access and an **API token** (`tsid`), created in the Velip portal on the integrations screen. See [Authentication](../api/v2/authentication.md).
- The **API and webhook docs of your CRM** (or ERP, e-commerce, helpdesk) and admin access to configure webhooks there.
- **Your own phone number** for the first tests.
- An **AI agent**:

| Agent | Best for |
| --- | --- |
| ChatGPT or Claude (chat, with web access) | A step-by-step guide and sample code. You do the setup. |
| Claude Code, Cursor or another coding agent | Writing, running and testing the code in your own project. |

## How it works

1. The agent reads the Velip docs (the [key pages](#key-pages-for-the-agent) are listed below) and your CRM docs.
2. It checks whether your CRM's webhook can call the Velip API directly or needs a small piece of code in between. Many CRMs cannot send the token and the fields the Velip API expects, so a small middleware is common.
3. It maps your CRM fields to Velip parameters: phone to `dest`, contact name to `nome`, and so on.
4. It writes the code, or the steps to configure everything yourself.
5. You test with your own number and then turn it on.

## Example prompt

Copy one of the prompts below and fill in the parts in `[brackets]`. Ask the agent to explain each step before you run anything.

### In Portuguese

```text
Quero integrar o meu CRM com a Velip para fazer uma ligação automática
quando [EVENTO, ex.: um lead novo for criado].

1. Leia a documentação da Velip em https://github.com/velipbr/velip-docs,
   começando por:
   - docs/api/v2/getting-started.md
   - docs/api/v2/authentication.md
   - docs/api/v2/voice/MakeTTSCall.md
   - docs/api/v2/voice/GetCallStatus.md (resultado da ligação pelo rurl)
   - docs/api/v2/errors.md
   A URL base da minha conta é https://vox.velip.com.br.

2. Leia a documentação do meu CRM: [NOME DO CRM], [LINK DA DOCUMENTAÇÃO
   DE API E WEBHOOK].

3. Antes de escrever código, me diga:
   - se o webhook do CRM consegue chamar a API da Velip direto ou se
     precisa de um código intermediário, e onde hospedá-lo;
   - qual campo do CRM vai para cada parâmetro da MakeTTSCall;
   - o que mais você precisa saber de mim.

4. Depois, [escreva o código da integração | me dê o passo a passo para
   eu configurar], incluindo:
   - a mensagem falada: "[TEXTO, ex.: Olá <NOME>, aqui é da Empresa X...]";
   - proteção contra ligação repetida para a mesma pessoa (httpdup);
   - o tratamento dos códigos de erro da Velip;
   - o resultado da ligação de volta no CRM (rurl), atualizando
     [CAMPO OU ETAPA DO LEAD].

5. Use YOUR_TSID no lugar do token. Não me peça o token nesta conversa:
   ele fica numa variável de ambiente ou num campo seguro do CRM.

6. Termine com um teste de ligação para o meu número: [SEU NÚMERO].
```

### In English

```text
I want to connect my CRM to Velip so that a phone call is placed
automatically when [EVENT, e.g. a new lead is created].

1. Read the Velip docs at https://github.com/velipbr/velip-docs,
   starting with:
   - docs/api/v2/getting-started.md
   - docs/api/v2/authentication.md
   - docs/api/v2/voice/MakeTTSCall.md
   - docs/api/v2/voice/GetCallStatus.md (call result through rurl)
   - docs/api/v2/errors.md
   My account's base URL is https://vox.velip.com.br.

2. Read my CRM docs: [CRM NAME], [LINK TO ITS API AND WEBHOOK DOCS].

3. Before writing any code, tell me:
   - whether the CRM webhook can call the Velip API directly or needs
     a small piece of code in between, and where to host it;
   - which CRM field goes into each MakeTTSCall parameter;
   - anything else you need to know from me.

4. Then [write the integration code | give me the steps to set it up
   myself], including:
   - the spoken message: "[TEXT, e.g. Hello <NOME>, this is Company X...]";
   - protection against calling the same person twice (httpdup);
   - handling of the Velip error codes;
   - sending the call result back to the CRM (rurl), updating
     [LEAD FIELD OR STAGE].

5. Use YOUR_TSID instead of the real token. Do not ask me for the token
   in this chat: it goes in an environment variable or a secure CRM field.

6. Finish with a test call to my own number: [YOUR NUMBER].
```

## Key pages for the agent

| Page | Why the agent needs it |
| --- | --- |
| [Getting started](../api/v2/getting-started.md) | Base URL, request format, encoding, phone number format. |
| [Authentication](../api/v2/authentication.md) | The `tsid` token and the IP allowlist. |
| [MakeTTSCall](../api/v2/voice/MakeTTSCall.md) | Places the call: text or recorded audio, placeholders such as `<NOME>`, IVR, transfer, `rurl`. |
| [GetCallStatus](../api/v2/voice/GetCallStatus.md) | The fields of the call result sent to your `rurl`. |
| [Error codes](../api/v2/errors.md) | What each `status_code` means. |
| [CreateCampaign](../api/v2/campaigns/CreateCampaign.md) | For many calls at once, instead of one request per record. |
| [WebRTC softphone guide](../api/v2/voice/webrtc-softphone.md) | Calls from your own agent screen: the full flow, the browser code (JsSIP) and the `MakeTTSCall` that connects agent and customer. |
| [GetWebRTC](../api/v2/voice/GetWebRTC.md) | The softphone credentials of each agent, fetched by your backend. |
| [CreatePixCharge](../api/v2/credit/CreatePixCharge.md) | Buys credit with PIX: QR code, `reference` for safe retries, account requirements. |
| [GetChargeStatus](../api/v2/credit/GetChargeStatus.md) | When the purchase is `credited`, and the account balance. |

If the agent gets only one URL, give it [`https://developers.velip.com.br/llms.txt`](https://developers.velip.com.br/llms.txt): the index of every page, with links to the raw Markdown. If the agent cannot open GitHub pages, give it the raw files, for example `https://raw.githubusercontent.com/velipbr/velip-docs/main/docs/api/v2/voice/MakeTTSCall.md`. A coding agent can also clone the repository with `git clone https://github.com/velipbr/velip-docs` and read the `docs/` folder.

## Before going live

- **Keep the token secret.** It places calls, sends messages and buys credit on behalf of your account. Do not paste it into a chat, a code repository or code that runs in the browser: the browser gets only what it needs, such as the softphone credentials from `GetWebRTC`. Store it in an environment variable or a secure field of your CRM. If it leaks, create a new one in the portal: the old one stops working at once.
- **Review what the agent wrote.** Agents make mistakes. Check the parameters against the docs and ask the agent to explain any part you do not understand.
- **Test with your own number first**, then with a small group, then turn it on for everyone.
- **Avoid duplicate calls.** CRMs often resend a webhook when the first attempt fails. Set `httpdup` (up to 600 seconds) so that the same number is not called twice within that window.
- **Use `rurl` for the result** instead of polling `GetCallStatus`, which has [rate limits](../api/v2/rate-limits.md). The result comes from `35.232.103.91` or `35.184.30.236`; if your endpoint filters by IP, allow both.
- **Restrict by IP** when your middleware has a fixed IP address: add it to the allowlist described in [Authentication](../api/v2/authentication.md).
- **Call only people who agreed to be contacted**, at reasonable hours.

## Other channels

The same prompt works for SMS and WhatsApp. Replace `MakeTTSCall` with [`MakeSMS`](../api/v2/sms/MakeSMS.md) or [`MakeWhatsapp`](../api/v2/whatsapp/MakeWhatsapp.md) and point the agent to that page. On WhatsApp, a message to a contact who has not written to you in the last 24 hours must use an approved template: see [`GetWATemplates`](../api/v2/whatsapp/GetWATemplates.md).

## Calls from your own agent screen (WebRTC)

Your agents click *Call* in your own system and talk to the customer in the browser. Your backend fetches the softphone credentials of each agent with [`GetWebRTC`](../api/v2/voice/GetWebRTC.md) and places the call with [`MakeTTSCall`](../api/v2/voice/MakeTTSCall.md): Velip rings the agent's browser first and then dials the customer. The [WebRTC softphone guide](../api/v2/voice/webrtc-softphone.md) has the whole flow and the browser code; the [demo page](https://developers.velip.com.br/api/v2/voice/webrtc-demo.html) lets you try it without code.

Ask Velip support to enable WebRTC for your account first, with the number of agents you need: until then `GetWebRTC` answers `204`. The softphone places calls; it does not receive incoming calls yet.

### In Portuguese

```text
Quero colocar ligações dentro da tela de atendimento do meu sistema
([NOME DO SISTEMA E TECNOLOGIA, ex.: meu CRM em React com backend em Node]):
o atendente clica em "Ligar" e fala com o cliente pelo navegador.

1. Leia a documentação da Velip em https://github.com/velipbr/velip-docs:
   - docs/api/v2/voice/webrtc-softphone.md (fluxo completo e código do navegador)
   - docs/api/v2/voice/GetWebRTC.md
   - docs/api/v2/voice/MakeTTSCall.md
   - docs/api/v2/authentication.md
   A URL base da minha conta é https://vox.velip.com.br.

2. Antes de escrever código, me diga:
   - qual rota do meu backend chama a GetWebRTC e qual chama a MakeTTSCall
     (o token nunca vai para o navegador);
   - qual id do atendente no meu sistema vira o userid;
   - como a tela mostra o estado do softphone (pronto, em ligação, sem conexão).

3. Depois escreva:
   - a rota que entrega as credenciais só ao atendente logado;
   - o softphone no navegador com JsSIP servido pelo meu próprio site,
     que atende sozinho a ligação que a Velip faz para o atendente;
   - a rota que faz a ligação (type 3, dest = sipname do atendente,
     dest2 = número do cliente), conferindo antes se o atendente pode ligar;
   - o resultado da ligação de volta no meu sistema (rurl).
   Se a GetWebRTC responder 204, pare e me avise: falta a Velip liberar o
   WebRTC na conta.

4. Use YOUR_TSID no lugar do token. Não me peça o token nesta conversa:
   ele fica numa variável de ambiente do backend.

5. Termine com um teste: eu, como atendente, ligando para o meu celular
   [SEU NÚMERO].
```

### In English

```text
I want calls inside the agent screen of my system
([SYSTEM AND STACK, e.g. my React CRM with a Node backend]):
the agent clicks "Call" and talks to the customer in the browser.

1. Read the Velip docs at https://github.com/velipbr/velip-docs:
   - docs/api/v2/voice/webrtc-softphone.md (full flow and browser code)
   - docs/api/v2/voice/GetWebRTC.md
   - docs/api/v2/voice/MakeTTSCall.md
   - docs/api/v2/authentication.md
   My account's base URL is https://vox.velip.com.br.

2. Before writing any code, tell me:
   - which route of my backend calls GetWebRTC and which calls MakeTTSCall
     (the token never goes to the browser);
   - which agent id of my system becomes the userid;
   - how the screen shows the softphone state (ready, in call, offline).

3. Then write:
   - the route that gives the credentials only to the logged-in agent;
   - the browser softphone with JsSIP served from my own site, answering
     automatically the call Velip places to the agent;
   - the route that places the call (type 3, dest = the agent's sipname,
     dest2 = the customer's number), checking first that the agent may call;
   - the call result back in my system (rurl).
   If GetWebRTC answers 204, stop and tell me: Velip still has to enable
   WebRTC for the account.

4. Use YOUR_TSID instead of the real token. Do not ask me for the token
   in this chat: it goes in an environment variable of the backend.

5. Finish with a test: me, as the agent, calling my own phone
   [YOUR NUMBER].
```

## Buy credit automatically

Your system buys credit with PIX without anyone logging in to the portal: for example, when the balance drops below a threshold, or when your finance team approves a purchase. [`CreatePixCharge`](../api/v2/credit/CreatePixCharge.md) returns the QR code for whoever pays, and [`GetChargeStatus`](../api/v2/credit/GetChargeStatus.md) tells when the payment is `credited` and what the balance is.

The account must be released by Velip (not under review), prepaid, and with CPF/CNPJ, e-mail and, in Brazil, the fiscal address complete in the portal: the payer is always the account registration.

### In Portuguese

```text
Quero que o meu sistema compre crédito na Velip por PIX, sem entrar no
portal, quando [EVENTO, ex.: o saldo ficar abaixo de R$ 200 | o financeiro
aprovar uma compra].

1. Leia a documentação da Velip em https://github.com/velipbr/velip-docs:
   - docs/api/v2/credit/CreatePixCharge.md
   - docs/api/v2/credit/GetChargeStatus.md
   - docs/api/v2/authentication.md
   - docs/api/v2/errors.md
   A URL base da minha conta é https://vox.velip.com.br.

2. Antes de escrever código, me diga:
   - como o QR do PIX chega a quem paga ([QUEM PAGA, ex.: o financeiro,
     por e-mail]);
   - onde o meu sistema guarda o charge_id e a reference de cada compra;
   - o que mais você precisa saber de mim.

3. Depois escreva a integração com estas regras:
   - a reference é o id da compra no meu sistema, para um retry nunca gerar
     dois PIX;
   - a compra só é dada como paga quando a GetChargeStatus responder
     status "credited";
   - no máximo uma consulta por minuto enquanto o PIX está pendente, e o
     saldo (GetChargeStatus sem parâmetros) no máximo a cada 15 minutos:
     o limite é 60 consultas por hora, contando as do saldo;
   - tratamento dos códigos de erro, em especial 403, 409, 422 e 429.

4. Use YOUR_TSID no lugar do token. Não me peça o token nesta conversa:
   ele fica numa variável de ambiente do backend.

5. Termine com um teste de R$ 50 (o mínimo), pago por mim.
```

### In English

```text
I want my system to buy credit from Velip with PIX, without logging in to
the portal, when [EVENT, e.g. the balance drops below R$ 200 | finance
approves a purchase].

1. Read the Velip docs at https://github.com/velipbr/velip-docs:
   - docs/api/v2/credit/CreatePixCharge.md
   - docs/api/v2/credit/GetChargeStatus.md
   - docs/api/v2/authentication.md
   - docs/api/v2/errors.md
   My account's base URL is https://vox.velip.com.br.

2. Before writing any code, tell me:
   - how the PIX QR code reaches whoever pays ([WHO PAYS, e.g. finance,
     by e-mail]);
   - where my system stores the charge_id and the reference of each purchase;
   - anything else you need to know from me.

3. Then write the integration with these rules:
   - the reference is the purchase id in my system, so that a retry never
     creates two PIX charges;
   - a purchase counts as paid only when GetChargeStatus answers
     status "credited";
   - at most one status check per minute while the PIX is pending, and the
     balance (GetChargeStatus without parameters) at most every 15 minutes:
     the limit is 60 requests per hour, balance checks included;
   - handling of the error codes, especially 403, 409, 422 and 429.

4. Use YOUR_TSID instead of the real token. Do not ask me for the token
   in this chat: it goes in an environment variable of the backend.

5. Finish with a R$ 50 test (the minimum), paid by me.
```

## Tip: test from the agent with the MCP server

If you connect the [Velip MCP server](../mcp/README.md) to Claude or Cursor, the agent can also place a test call or send a test message itself while it builds the integration. Your production integration still uses the REST API described above.
