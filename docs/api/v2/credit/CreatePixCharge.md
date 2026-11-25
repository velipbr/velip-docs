# Create a PIX charge (buy credit)

*Generate a PIX QR code that adds credit to your account's prepaid balance.*


**Endpoint:** `POST https://<base>/api/v2/CreatePixCharge.php`

Creates a PIX charge for the account of the credential and returns the QR code (image link and copy-and-paste text). When the payer pays it, the credit is added to the account balance automatically, and the invoice (NFS-e) and the confirmation e-mail follow, as with a purchase made in the Velip portal.

Use it to top up the balance from your own system, without logging in to the portal. Only PIX is available through the API; boleto and credit card stay in the portal.

## How it works

1. Your backend calls `CreatePixCharge` with the `amount` and, ideally, a `reference` (your order id).
2. You show the QR code (`qr_code_url`) or the copy-and-paste text (`pix_copy_paste`) to whoever pays.
3. The payer pays within the validity (`expires_at`, 3 days after creation).
4. You check [`GetChargeStatus`](GetChargeStatus.md) until `status` is `credited`. That status means the credit is already in the balance.

> **Note**
> Release anything in your system only after `GetChargeStatus` returns `credited`. A `pending` charge may never be paid, and a QR code alone is not proof of payment.

## Requirements

The account must:

- **be released by Velip.** New accounts start under review; until then, buy credit in the portal (`210`).
- **be prepaid.** Postpaid accounts are billed by Velip's finance team and cannot buy credit (`211`).
- **have credit purchase enabled.** It is on for accounts contracted directly with Velip. Accounts of a reseller follow the reseller's setting and may have to buy credit from the reseller (`212`).
- **have the payer data in its registration:** CPF or CNPJ and an e-mail. Brazilian accounts also need the fiscal address (ZIP code, street and number), which goes on the invoice (`230` to `232`). Complete them in the portal.

The payer is always the account registration. Name, CPF/CNPJ or e-mail sent in the request are ignored. The e-mail used is that of the user who owns the token. If that user is inactive or has no valid e-mail, the account e-mail is used instead.

## Authentication

Same credentials as the other v2 endpoints: token (`tsid` or the `Authorization: Bearer` header) or HTTP Basic. See [Authentication](../authentication.md).

Call this endpoint **from your backend**, never from the browser: the token gives access to the whole account.

## Request

**POST only** (`200` otherwise), in JSON or form encoding.

#### `amount` — type: *string* or *number* — **required**

Amount in BRL, from `50.00` to `20000.00`, with a dot or a comma and up to 2 decimals: `50`, `150.5`, `150,50`. Do not use a thousands separator: `1.500` and `20.000,00` are refused (`201`), because they are ambiguous.


#### `reference` — type: *string*

Id of the order in your system: 1 to 64 characters among `A-Z`, `a-z`, `0-9`, `.`, `_` and `-` (no spaces). It is case-sensitive: `PED-1` and `ped-1` are different references. It comes back in the response and in [`GetChargeStatus`](GetChargeStatus.md), and it makes the request **idempotent** (see below).


## Idempotency with `reference`

Send a `reference` and retry safely: a timeout or a repeated call never creates a second charge for the same order.

| Charge already created with the same `reference` | Result |
| --- | --- |
| None | A new charge is created (`200`). |
| Pending and still valid, **same** amount | The **same** charge is returned (`200`), with the same QR code and the same `expires_at`. Nothing new is created. |
| Pending and still valid, **different** amount | `409`, code `220`. |
| Paid (credited) or refunded | `409`, code `221`. |
| Expired (not paid within 3 days) | A new charge is created with the same `reference`. |

A retried charge keeps its original `expires_at`, even when it is about to expire. If you need a fresh QR code for the same order before that, use a new `reference`.

Without `reference`, every call creates a new charge.

## Request example
```bash curl (JSON)
curl -X POST 'https://<base>/api/v2/CreatePixCharge.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -H 'Content-Type: application/json' \
  -d '{ "amount": "150.00", "reference": "ORDER-778" }'
```

```bash curl (form)
curl -X POST 'https://<base>/api/v2/CreatePixCharge.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -d 'amount=150,00' \
  -d 'reference=ORDER-778'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0"
  },
  "charge": {
    "charge_id": 12345,
    "reference": "ORDER-778",
    "amount": "150.00",
    "status": "pending",
    "pix_copy_paste": "00020101021226830014br.gov.bcb.pix2561api.pagseguro.com/pix/v2/...6304A1B2",
    "qr_code_url": "https://api.pagseguro.com/qrcode/QRCO_.../png",
    "expires_at": "2026-11-28T08:49:33-03:00"
  }
}
```

```json 409 Reference already paid
{
  "return": {
    "status": "Reference already paid",
    "status_code": "221"
  }
}
```

```json 403 Account under review
{
  "return": {
    "status": "Account under review: credit purchase by API not available",
    "status_code": "210"
  }
}
```
- **`charge.charge_id`** (*integer*) — Id of the charge at Velip. Use it in [`GetChargeStatus`](GetChargeStatus.md).


- **`charge.reference`** (*string* or `null`) — The `reference` you sent, or `null` without one.


- **`charge.amount`** (*string*) — Amount of the charge in BRL, with 2 decimals.


- **`charge.status`** (*string*) — Always `pending` here. Follow the payment with [`GetChargeStatus`](GetChargeStatus.md).


- **`charge.pix_copy_paste`** (*string*) — PIX "copia e cola" text, for the payer to paste in the bank app.


- **`charge.qr_code_url`** (*string*) — Link to the QR code image (PNG), hosted by the payment provider (PagBank).


- **`charge.expires_at`** (*string*) — End of the QR code validity, in ISO 8601 with time zone: 3 days after creation. After it, the QR code can no longer be paid.


`charge` comes only on success; on any error the response has only `return`.

## Error codes

| HTTP | Code | `status` | Cause |
| --- | --- | --- | --- |
| 400 | `200` | `POST required` | The request was not a POST. |
| 400 | `201` | `Invalid amount: 50.00 to 20000.00, up to 2 decimals` | `amount` missing, out of range, with more than 2 decimals or with a thousands separator. |
| 400 | `202` | `Invalid reference: 1 to 64 characters A-Z a-z 0-9 . _ -` | `reference` with spaces or other characters, or longer than 64. |
| 403 | `210` | `Account under review: credit purchase by API not available` | The account is still under review. Buy credit in the portal until Velip releases it. |
| 403 | `211` | `Postpaid account: credit purchase does not apply` | The account is postpaid. |
| 403 | `212` | `Credit purchase not enabled for this account` | Credit purchase is not enabled for the account. Contact your account manager. |
| 403 | `213` | `Inactive account` | The account was disabled. |
| 403 | `214` | `Credential not allowed for this API` | The credential is not a user token or user login. |
| 409 | `220` | `Reference already used with another amount` | A pending charge with this `reference` has a different amount. |
| 409 | `221` | `Reference already paid` | A charge with this `reference` was already paid (or refunded). Nothing was created. |
| 422 | `230` | `Fiscal address required: complete the account address in the panel` | Brazilian account without a usable fiscal address in the registration. |
| 422 | `231` | `CPF/CNPJ required: complete the account registration in the panel` | The registration has no valid CPF or CNPJ. |
| 422 | `232` | `E-mail required: complete the account registration in the panel` | Neither the user nor the account has a valid e-mail. |
| 429 | `240` | `Too many pending charges in the last hour: pay one or try later` | The account already has 10 unpaid charges (PIX or boleto, API or portal) created in the last hour. |
| 429 | `241` | `Too many attempts: try again later` | Attempt limit of the user reached (see [Limits](#limits)). |
| 429 | `242` | `Another charge is being created for this account: try again in a few seconds` | Another request of the account is creating a charge right now. A `Retry-After` header (seconds) is sent. |
| 502 | `250` | `Payment gateway refused the charge: check the account CPF/CNPJ and e-mail` | The payment provider refused the payer data. Check the registration in the portal. |
| 503 | `251` | `Payment gateway unavailable: try again in a few minutes` | The payment provider did not answer. Nothing was created. |
| 500 | `260` | `Charge not saved: try again` | The charge was not recorded and no QR code was returned, so there is nothing to pay. Try again. |
| 500 | `500` | `Internal error` | Temporary failure. Try again later. |

Authentication failures return HTTP 401 with the [global authentication codes](../errors.md).

## Limits

- **10 pending charges per account per hour**, counting PIX and boleto from the API and from the portal (`240`). Paid charges stop counting.
- **Attempts**: 12 in 6 minutes and 120 per hour per user of the token, and 1,000 per account per day (`241`). Every attempt counts, including the refused ones, and the counter is shared with purchases made in the portal by the same user.
- **One charge at a time per account**: a second request waits up to 10 seconds for the first one; after that it gets `242`. With the same `reference`, the second request returns the charge of the first.

See also [Rate limits](../rate-limits.md).

> **Warning**
> The token buys credit on behalf of the account. Keep it in your backend, out of logs and of the browser, and restrict it with the IP allowlist (see [Authentication](../authentication.md)).
