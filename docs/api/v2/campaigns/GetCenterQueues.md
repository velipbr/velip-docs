# List contact-center queues

*Return all active queues (voice and chat) for the authenticated account.*


**Endpoint:** `POST https://<base>/api/v2/GetCenterQueues.php`

Returns every active row in `cc_fila` for the authenticated customer (`ccf_active = 1`), sorted alphabetically by name. Useful to populate queue pickers in custom dashboards or before calling [`CreateCampaign`](CreateCampaign.md) with `queue_id`.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


This endpoint takes no other parameters.

## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetCenterQueues.php' \
  -H 'Content-Type: application/json' \
  -d '{ "tsid": "YOUR_TSID" }'
```
## Response
```json 200 OK
{
  "return": { "status": "OK", "status_code": "0" },
  "queues": [
    {
      "queue_id": 678,
      "name": "Sales NPS",
      "type": "ch",
      "type_description": "Chat",
      "description": "Inbound sales after NPS survey",
      "active": true,
      "created_date": "2026-05-06",
      "ai_tutor": { "id": 12, "name": "Sales tutor" },
      "ai_chatbot": { "id": 45, "name": "Sales bot" },
      "buttons": {
        "button_1": "Send proposal", "button_2": "Mark as won",
        "button_3": "", "button_4": "",
        "button_5": "", "button_6": "",
        "button_7": "", "button_8": ""
      },
      "dropdowns": {
        "dropdown_1": ["Hot", "Warm", "Cold"],
        "dropdown_2": []
      },
      "templates": ["101", "102"]
    }
  ]
}
```
## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `240` | `Erro ao buscar filas` | Database error preparing/running the query. |
