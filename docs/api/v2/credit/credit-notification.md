# Credit notification (webhook)

*Velip calls your URL when a credit purchase is paid and the credit is in the balance.*

Instead of checking [`GetChargeStatus`](GetChargeStatus.md) over and over, register a URL and Velip sends a `POST` with a JSON body for every credit purchase that is paid and credited to the account:

- PIX, boleto and credit card;
- purchases created by [`CreatePixCharge`](CreatePixCharge.md) and purchases made in the Velip portal.

Credit added manually by the Velip team and refunds are not notified. A refund shows up as `refunded` in [`GetChargeStatus`](GetChargeStatus.md).

> **Note**
> The notification is a signal, not a proof of payment. Before releasing anything in your system, confirm the charge with [`GetChargeStatus`](GetChargeStatus.md) and act only on `status` = `credited`. See [Handling the notification](#handling-the-notification).

## Set up the URL

In the Velip portal, open **Integrations > Webhook returns**, group **Billing**, field **Credit confirmed URL**, and save.

- It must be a full public URL (`https://…`). Internal or private addresses are refused when saving.
- The notification uses the **username, password and extra headers** set at the top of that page, the same ones as the other callbacks of the account. With a username and password, the request carries HTTP Basic authentication.
- It is **always `POST` with JSON**, whatever HTTP method and data format are chosen on that page for the other callbacks.
- If you change the URL to another host and a password is stored, the portal asks for the password again before saving.
- Leave the field empty to stop the notifications.

Only credits made after the URL is saved are sent. Credits from up to one hour before may also arrive; older ones are not sent.

## The request

```http
POST /your/path HTTP/1.1
Host: your-server.example.com
Content-Type: application/json
Authorization: Basic dXNlcjpwYXNzd29yZA==

{"event":"credit","charge_id":12345,"reference":"ORDER-778","method":"pix","origin":"api","amount":"150.00","credited_amount":"150.00","credited_at":"2026-11-24T14:03:11-03:00","balance_after":"1234.56"}
```

The `Authorization` header is present only when a username and password are set; your extra headers are added to every notification.

```json Body
{
  "event": "credit",
  "charge_id": 12345,
  "reference": "ORDER-778",
  "method": "pix",
  "origin": "api",
  "amount": "150.00",
  "credited_amount": "150.00",
  "credited_at": "2026-11-24T14:03:11-03:00",
  "balance_after": "1234.56"
}
```
- **`event`** (*string*) — Always `credit`.


- **`charge_id`** (*integer*) — Id of the charge, the same returned by [`CreatePixCharge`](CreatePixCharge.md) and accepted by [`GetChargeStatus`](GetChargeStatus.md).


- **`reference`** (*string* or `null`) — The `reference` sent to [`CreatePixCharge`](CreatePixCharge.md); `null` for charges created without one, including all purchases made in the portal.


- **`method`** (*string*) — `pix`, `boleto` or `card`.


- **`origin`** (*string*) — `api` (created by [`CreatePixCharge`](CreatePixCharge.md)) or `panel` (purchase made in the portal).


- **`amount`** (*string*) — Amount of the charge in BRL.


- **`credited_amount`** (*string*) — Amount added to the balance. It is the amount actually paid, which can differ from `amount`.


- **`credited_at`** (*string*) — When the credit entered the balance, in ISO 8601 with time zone.


- **`balance_after`** (*string*) — Balance of the account right after this credit. Later usage and purchases change the balance: for the current one, use [`GetChargeStatus`](GetChargeStatus.md).


The body never carries the payer's CPF/CNPJ, name or e-mail.

## Your response

Answer with any `2xx` status. The response body is ignored.

- Velip waits up to 5 seconds to connect and 15 seconds for the whole request. Do the heavy work after answering.
- With `https`, the certificate must be valid.
- A redirect is followed only to the same host (same scheme and port, or from `http` to `https`); any other redirect counts as a failure.

## Retries

When the request fails (no answer, timeout, an address that does not resolve, or a status other than `2xx`), Velip tries again after 1, 5, 15, 60 and 180 minutes: up to **6 sends**, in about 4 hours and 20 minutes. After the sixth failure the notification is not sent again; the charge is still available in [`GetChargeStatus`](GetChargeStatus.md).

A notification is normally sent within one or two minutes of the credit.

Every send appears in the portal report **Integrations > Reports > Webhook returns**, with the number `CREDIT`, the `charge_id` in the ID column, the HTTP status and the response of your server. The account credentials are masked in the report.

## Handling the notification

- **Confirm before acting.** Anyone who learns your URL can send a request that looks like a notification; the only protection is the username, password or headers you set. Call [`GetChargeStatus`](GetChargeStatus.md) with the `charge_id` and release the order only when `status` is `credited`.
- **Discard repeats by `charge_id`.** The same notification can arrive more than once, for example when your server processed it but the answer was lost. Each charge is credited only once, so a second notification with a `charge_id` you already handled is a repeat.
- **Use `https`**, a username and password or a secret header, and a path that is hard to guess.
- **Source addresses.** Notifications come from `35.232.103.91` or `35.184.30.236`, the same addresses as the other callbacks (see [Webhook delivery](../voice/GetCallStatus.md#webhook-delivery)). If your endpoint filters by IP, allow both.

## Test

1. Point the **Credit confirmed URL** to a test endpoint you control and save.
2. Buy R$ 50 (the minimum) with PIX, by [`CreatePixCharge`](CreatePixCharge.md) or in the portal, and pay it.
3. Within a couple of minutes of the credit, one notification arrives, with `origin` = `api` or `panel`, and the send appears in **Integrations > Reports > Webhook returns**.
4. Check the same `charge_id` with [`GetChargeStatus`](GetChargeStatus.md): `credited`.
