# List approved WhatsApp templates

*Return all templates approved by Meta for a WhatsApp line.*


**Endpoint:** `POST https://<base>/api/v2/GetWATemplates.php`

Returns the list of WhatsApp templates that have been approved by Meta (`cwt_status = 'APPROVED'`) for a given WhatsApp line. Useful for populating template pickers in custom dashboards or when sending [`MakeWhatsapp`](MakeWhatsapp.md) calls with `mtype=wa_template`.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `app_id` — type: *integer* — **required**

ID of the WhatsApp line (`cd_v8_line.v8l_id`). Must belong to the authenticated customer and be active.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetWATemplates.php' \
  -H 'Content-Type: application/json' \
  -d '{ "tsid": "YOUR_TSID", "app_id": 1234 }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0"
  },
  "templates": [
    {
      "cwt_id": 123,
      "cwt_name": "shipment_update",
      "cwt_category": "UTILITY",
      "cwt_language": "pt_BR",
      "cwt_status": "APPROVED",
      "cwt_body_text": "Hi {{1}}, your shipment {{2}} is on the way.",
      "cwt_header_type": "TEXT",
      "cwt_header_text": "Update from Acme",
      "cwt_footer_text": "Reply STOP to opt out.",
      "cwt_variables_examples": "{\"body_text\":[\"John\",\"ABC-123\"]}",
      "cwt_button_type": "URL",
      "cwt_button_config": "{\"buttons\":[{...}]}"
    }
  ]
}
```
- **`templates`** (*array*) — Array of template objects. Empty when there are no approved templates for the line.


- **`templates[].cwt_id`** (*integer*) — Local Velip id of the template (use it as `template_id` in [`CheckTemplateStatus`](CheckTemplateStatus.md) and [`DeleteWhatsappTemplate`](DeleteWhatsappTemplate.md)).


- **`templates[].cwt_name`** (*string*) — Template name registered with Meta (used as `name` in [`MakeWhatsapp`](MakeWhatsapp.md) template calls).


- **`templates[].cwt_variables_examples`** (*string*) — JSON-encoded examples for placeholders (`body_text`, `header_text`).


- **`templates[].cwt_button_config`** (*string*) — JSON-encoded button definitions when the template includes buttons (URL, quick replies, call permission).


## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `201` | `app_id is required` | Missing `app_id`. |
| `202` | `Invalid or unauthorized app_id` | Line is missing, inactive, or does not belong to this customer. |
| `500` | (DB error) | Internal database error preparing or running the query. |
