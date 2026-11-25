# Get charge status and balance

*Status of a credit purchase and the current account balance.*


**Endpoint:** `GET` or `POST https://<base>/api/v2/GetChargeStatus.php`

Returns the status of one credit purchase of the account (charge) and the current balance. Use it after [`CreatePixCharge`](CreatePixCharge.md) to know when the payment was credited. It only reads: nothing in the charge changes.

Any charge of the account can be queried: PIX created by the API, and PIX, boleto or credit card purchases made in the Velip portal. Without `charge_id` and `reference`, it returns only the balance.

## Authentication

Same credentials as the other v2 endpoints: token (`tsid` or the `Authorization: Bearer` header) or HTTP Basic. See [Authentication](../authentication.md).

## Request

Both parameters are optional.

#### `charge_id` — type: *integer*

The `charge_id` returned by [`CreatePixCharge`](CreatePixCharge.md).


#### `reference` — type: *string*

The `reference` sent to [`CreatePixCharge`](CreatePixCharge.md), case-sensitive. When several charges share it (an expired one and its replacement), the most recent one is returned.


With both, the charge must match both. A charge of another account answers exactly like one that does not exist (`404`).

## Request example
```bash curl (by charge_id)
curl 'https://<base>/api/v2/GetChargeStatus.php?charge_id=12345' \
  -H 'Authorization: Bearer YOUR_TSID'
```

```bash curl (by reference)
curl -X POST 'https://<base>/api/v2/GetChargeStatus.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -H 'Content-Type: application/json' \
  -d '{ "reference": "ORDER-778" }'
```

```bash curl (balance only)
curl 'https://<base>/api/v2/GetChargeStatus.php' \
  -H 'Authorization: Bearer YOUR_TSID'
```
## Response
```json 200 Credited
{
  "return": {
    "status": "OK",
    "status_code": "0"
  },
  "balance": "1234.56",
  "charge": {
    "charge_id": 12345,
    "reference": "ORDER-778",
    "method": "pix",
    "origin": "api",
    "amount": "150.00",
    "status": "credited",
    "created_at": "2026-11-25T08:49:33-03:00",
    "paid_at": "2026-11-25T09:19:39-03:00",
    "credited_amount": "150.00",
    "expires_at": "2026-11-28T08:49:33-03:00"
  }
}
```

```json 200 Pending
{
  "return": {
    "status": "OK",
    "status_code": "0"
  },
  "balance": "1084.56",
  "charge": {
    "charge_id": 12345,
    "reference": "ORDER-778",
    "method": "pix",
    "origin": "api",
    "amount": "150.00",
    "status": "pending",
    "created_at": "2026-11-25T08:49:33-03:00",
    "paid_at": null,
    "credited_amount": null,
    "expires_at": "2026-11-28T08:49:33-03:00"
  }
}
```

```json 200 Balance only
{
  "return": {
    "status": "OK",
    "status_code": "0"
  },
  "balance": "1234.56"
}
```

```json 404 Not found
{
  "return": {
    "status": "Charge not found",
    "status_code": "202"
  },
  "balance": "1234.56"
}
```
- **`balance`** (*string*) — Current balance of the account in BRL, with 2 decimals. It can be negative after a refund. Present in every response of an authenticated account, except `429`.


- **`charge.charge_id`** (*integer*) — Id of the charge.


- **`charge.reference`** (*string* or `null`) — The `reference` of the charge; `null` for charges created without one, including all purchases made in the portal.


- **`charge.method`** (*string*) — `pix`, `boleto` or `card`.


- **`charge.origin`** (*string*) — `api` (created by [`CreatePixCharge`](CreatePixCharge.md)) or `panel` (purchase made in the portal).


- **`charge.amount`** (*string*) — Amount of the charge in BRL.


- **`charge.status`** (*string*) — See the table below.


- **`charge.created_at`** (*string* or `null`) — When the charge was created, in ISO 8601 with time zone.


- **`charge.paid_at`** (*string* or `null`) — When the payment was confirmed. Filled for `credited`, and for `refunded` when the payment had been confirmed; `null` otherwise.


- **`charge.credited_amount`** (*string* or `null`) — Amount added to the balance by this charge. It is the amount actually paid, which can differ from `amount`.


- **`charge.expires_at`** (*string* or `null`) — PIX: end of the QR code validity (date and time). Boleto: due date (`YYYY-MM-DD`). Card: `null`.


## Charge status

| `status` | Meaning | What to do |
| --- | --- | --- |
| `pending` | Waiting for payment, within the validity (3 days from creation). | Wait and check again. |
| `credited` | Paid, and the credit is already in the balance. | Final: release the order in your system. |
| `expired` | Not paid within 3 days. A PIX QR code can no longer be paid. | Create a new charge; the same `reference` can be reused. |
| `refunded` | Paid and then refunded; the credit was removed from the balance. | Final. |
| `failed` | Not completed: credit card declined, or a charge from an older payment system. | Final. |

`credited` comes from the credit posted to the balance, not from the payment provider's notice alone.

A **boleto** paid on its due date takes 1 to 3 business days to clear. Until then it may show `expired`, and it changes to `credited` when the credit enters.

## Error codes

| HTTP | Code | `status` | Cause |
| --- | --- | --- | --- |
| 400 | `200` | `Invalid charge_id` | `charge_id` is not a positive integer. |
| 400 | `201` | `Invalid reference` | `reference` with spaces or other characters, or longer than 64. |
| 404 | `202` | `Charge not found` | No charge of the account matches `charge_id` and/or `reference`. Charges of other accounts are never shown. |
| 429 | `210` | `Rate limit exceeded: max 60 requests per hour` | The account made 60 requests in the last hour. A `Retry-After` header (seconds) is sent. |
| 500 | `500` | `Internal error` | Temporary failure. Try again later. |

Authentication failures return HTTP 401 with the [global authentication codes](../errors.md).

## Limits

**60 requests per hour per account**, counting every request, including balance-only ones. Requests refused by this limit do not count. Under parallel requests the limit is approximate.

A practical pattern: while the payer is looking at the QR code, check about once a minute; after that, check rarely (for example, once an hour) until the charge is `credited` or `expired`.

See also [Rate limits](../rate-limits.md).
