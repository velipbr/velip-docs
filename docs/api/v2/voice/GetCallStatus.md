# Get call status / list calls

*Query call records (single or paginated) and optionally push them to a webhook.*


**Endpoint:** `POST https://<base>/api/v2/GetCallStatus.php`

Returns call records — a single call when you pass `cd_id` or `ctid`, or a paginated list when you pass campaign / date filters. When you supply `rurl`, results are POSTed to your webhook in either JSON or URL-encoded format instead of being returned in the response body.

This is the polling counterpart to the per-account return URL configured via the Velip portal.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `cd_id` — type: *string*

Single call id, in the form `<cdcs_db>_<numeric>` returned by [`MakeTTSCall`](MakeTTSCall.md). When supplied, returns one record.


#### `ctid` — type: *string*

Customer-side correlation id. Pass `null` to query records with empty `ctid`.


#### `cp_id` — type: *integer*

Campaign id (`cd_programa.cp_id`). Returns all calls for the campaign.


#### `cpid` — type: *string*

Customer-side campaign id (`cd_programa.cp_ctid`). Resolved internally to the latest matching `cp_id`.


#### `date_start` — type: *string*

Start date (`YYYY-MM-DD`). Alias `dini`.


#### `date_end` — type: *string*

End date (`YYYY-MM-DD`). Alias `dend`.


#### `maxreg` — type: *integer* — default: `1000`

Maximum records returned per page, capped at **5000**. `-1` (legacy "unlimited") and any value above 5000 are treated as 5000 and the response carries `pagination.maxreg_capped: true` with `maxreg_applied`; keep paginating with `last_id`. The endpoint actually fetches `maxreg + 1` rows so it can detect whether more pages exist.


#### `last_id` — type: *integer*

Cursor for pagination. Pass the `pagination.next_id` of the previous response.


#### `onlydtmf` — type: *integer*

When `1`, only return calls where the user pressed at least one digit (any of `cd_resp_1`, `cd_resp_2`, `cd_resp_3` non-empty).


#### `numtype` — type: *string*

Format for the destination number in the response. Empty = `DDI+DDD+number`, `0DDD` = `0+DDD+number`, `DDD` = `DDD+number` (Brazilian numbers only).


#### `origin` — type: *string* — default: `api`

Marker echoed back in `origin`. Allowed `[a-zA-Z0-9_-]{1,32}`; otherwise reset to `api`.


### Webhook delivery

Pass `rurl` to deliver the results to your endpoint instead of receiving them inline. Per-account defaults are used when these fields are omitted.

#### `rurl` — type: *string*

Public URL that receives the data.


#### `rurl_method` — type: *string*

`POST` or `GET`. Default is the customer's `cdcs_return_url_type`.


#### `rurl_type` — type: *string*

`json` to deliver as a JSON body; otherwise URL-encoded form parameters per call. Default is the customer's `cdcs_return_data_type`.


#### `rurl_headers` — type: *string*

Newline-separated extra headers (`Header: value`).


#### `rurl_user` — type: *string*

HTTP Basic username for the webhook.


#### `rurl_password` — type: *string*

HTTP Basic password for the webhook.


## Response
```json 200 OK (inline)
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "pagination": { "has_more": true, "next_id": 9876544 }
  },
  "calls": [
    {
      "cd_id": 9876545,
      "cd_status": "OK",
      "cd_amdasw": "ND",
      "cp_id": 555,
      "cpid": "lote-2026-05-06",
      "ctid": "row-42",
      "origin": "api",
      "dest": "5511999999999",
      "date": "2026-05-06",
      "time_dial": "10:00:01",
      "time_start": "10:00:08",
      "time_end": "10:00:35",
      "dur": 27,
      "resp_1": "1",
      "resp_2": "12345",
      "resp_3": "0",
      "route": "Mobile BR",
      "rate": "0,050",
      "value": "0,050",
      "cdr_url": "https://...",
      "cdr_sec": 27
    }
  ]
}
```
- **`calls[].cd_amdasw`** (*string*) — Answering-machine detection result: `MA` (machine), `HM` (human), `ND` (not determined). Only meaningful when AMD was enabled on the campaign.


- **`calls[].resp_1, resp_2, ...`** (*string*) — DTMF responses captured during the call. Number of `resp_*` keys is dynamic — depends on how many digits the IVR collected.


- **`calls[].cdr_url`** (*string*) — Recording URL when recording was enabled. `cdr_sec` carries the duration in seconds.


- **`return.pagination.has_more`** (*boolean*) — Present only when `maxreg` is set. `true` when more pages exist.


- **`return.pagination.next_id`** (*integer*) — Cursor to pass as `last_id` on the next page.


- **`return.pagination.maxreg_capped`** (*boolean*) — Present when the requested `maxreg` (`-1` or above 5000) was reduced to the 5000 cap; `maxreg_applied` carries the page size actually used. In webhook (`rurl`) JSON mode the same `pagination` object is included in the pushed payload when the page was truncated.


### Security: masked numbers and authorized IPs (list requests)

To limit the damage of a leaked token, **list requests** (by period, campaign, pagination, or a `ctid` shared by more than one call) have two extra rules:

- **Authorized IP** — the request should come from an IP registered under Integrations > IPs. During the transition period the endpoint does not block: it adds `return.warning` to the response when the IP is not registered. Blocking (HTTP 403, `status_code: 105`) will be enabled after customers are notified.
- **Masked numbers** — for tokens without the option **Full numbers in list responses** (Integrations > API tokens), `dest`, the `cdc_extra*` fields and `conf` come masked (`xxxxx877`, the same format the web app uses) and the response carries `return.numbers_masked: true`. Tokens created before 2026-09-03 have the option enabled; new tokens are masked by default. Point lookups by `cd_id` / single-call `ctid` always return the full number. Basic-auth (user/password) requests keep full numbers.

### Rate limit

List requests (any call **without** `cd_id` or `ctid`, i.e. by period, campaign or pagination) are limited to **200 per client per hour**. Point lookups (`cd_id` / `ctid`) have a **daily cap proportional to the account's call volume**: 500 + 40 × (average calls per day over the last 30 days + calls placed today). Do not poll finished calls repeatedly; use the return URL (`rurl`) to receive the final status instead. Above either limit the endpoint answers **HTTP 429** with `status_code: 429` and a `Retry-After` header (seconds); `status` starts with `Rate limit exceeded: ...` for list requests and `Daily limit of status lookups reached ...` for point lookups (the daily cap resets at midnight). Use `cp_id` or shorter date ranges, and page with `maxreg` / `last_id` instead of re-fetching.


## Error codes

This endpoint inherits the [global authentication codes](../errors.md). It does not raise endpoint-specific business codes — invalid filters simply produce an empty `calls` list.

> **Note**
> This endpoint is read-only on the call records (`cd_envia_*`), but writes to `cd_returl` when `rurl` is supplied — to track whether the webhook delivery succeeded. `cd_returl > 0` = delivered, `< 0` = retries failed.
