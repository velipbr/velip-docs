# Check WhatsApp template status

*Poll Meta for the current approval status of a submitted template.*


**Endpoint:** `POST https://<base>/api/v2/CheckTemplateStatus.php`

Queries the Meta Graph API for the current status of a template (`PENDING`, `APPROVED`, `REJECTED`, etc.) and synchronizes the local `cc_wa_templates.cwt_status` column with the Meta response. A status change is also recorded in `cc_wa_template_sends`.

Use this after submitting a template via [`CreateWhatsappTemplate`](CreateWhatsappTemplate.md) — Meta typically takes a few minutes to a few hours to finish review.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `template_id` — type: *integer* — **required**

Local id of the template (`cc_wa_templates.cwt_id`).


#### `v8l_id` — type: *integer* — **required**

ID of the WhatsApp line.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/CheckTemplateStatus.php' \
  -H 'Content-Type: application/json' \
  -d '{ "tsid": "YOUR_TSID", "template_id": 123, "v8l_id": 1234 }'
```
## Response
```json 200 OK (status changed)
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "template_id": "123",
    "result": {
      "meta_template_id": "456789012345678",
      "meta_status": "APPROVED",
      "previous_status": "PENDING",
      "status_changed": true,
      "meta_name": "shipment_update"
    }
  }
}
```

```json 200 OK (no change)
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "template_id": "123",
    "result": {
      "meta_template_id": "456789012345678",
      "meta_status": "PENDING",
      "previous_status": "PENDING",
      "status_changed": false,
      "meta_name": "shipment_update"
    }
  }
}
```
## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `230` | `No template_id` | Missing or non-numeric `template_id`. |
| `233` | `No API key` | Line is missing the Meta token. |
| `234` | `No Business ID` | Line is missing the Meta business id. |
| `235` | `Line not found` | Line missing, inactive, or wrong customer. |
| `236` | `No v8l_id` | Missing or non-numeric `v8l_id`. |
| `238` | `Template not found` | `template_id` does not belong to the customer/line. |
| `239` | `Template not yet sent to Meta` | `cwt_template_id` is empty — submit it first via [`CreateWhatsappTemplate`](CreateWhatsappTemplate.md). |
| `260` | `Meta API error` | Meta returned an error; full message in `result.error_message`. |
