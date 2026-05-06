# Create contact-center queue

*Provision a new queue (voice or chat) used to route conversations to operators.*


**Endpoint:** `POST https://<base>/api/v2/CreateCenterQueue.php`

Creates a row in `cc_fila` representing a contact-center queue. Queues are how Velip's portal routes inbound voice transfers and chat conversations to operators or to AI agents (tutor / chatbot).

After creation you can attach the queue to a [`CreateCampaign`](CreateCampaign.md) request via `queue_id`.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `name` — type: *string* — **required**

Queue name (visible in the Velip portal).


#### `type` — type: *string* — **required**

Queue type. `au` = voice queue (PA), `ch` = chat queue.


#### `description` — type: *string*

Free-text description.


#### `ai_tutor_id` — type: *integer*

ID of a `cc_bot_agent` (active) used as a tutor for human operators.


#### `ai_chatbot_id` — type: *integer*

ID of a `cc_bot_agent` (active) used as the autonomous chatbot for the queue.


### Quick-action buttons

`button_1` to `button_8` define labelled quick actions shown to the operator handling a conversation.

#### `button_1, button_2, ... button_8` — type: *string*

Label for the corresponding quick action button.


### Dropdowns

#### `dropdown_1` — type: *string | string[]*

Options for the first dropdown shown to operators. Accepts a `;` / `,` / newline-separated string or a JSON array.


#### `dropdown_2` — type: *string | string[]*

Same as above, for the second dropdown.


### Knowledge base templates

#### `templates` — type: *string | integer[]*

Comma-separated string or array of `cc_template.cct_id` to attach to the queue.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/CreateCenterQueue.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "name": "Sales NPS",
    "type": "ch",
    "description": "Inbound sales after NPS survey",
    "ai_tutor_id": 12,
    "ai_chatbot_id": 45,
    "button_1": "Send proposal",
    "button_2": "Mark as won",
    "dropdown_1": ["Hot", "Warm", "Cold"],
    "templates": [101, 102]
  }'
```
## Response
```json 201 Created
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "queue": {
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
        "button_1": "Send proposal",
        "button_2": "Mark as won",
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
  }
}
```
## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `230` | `Nome da fila Ã© obrigatÃ³rio` | Missing `name`. |
| `231` | `Tipo da fila Ã© obrigatÃ³rio` | Missing `type`. |
| `232` | `Tipo invÃ¡lido` | `type` not in `[au, ch]`. |
| `233` | `Tutor de IA nÃ£o encontrado ou inativo` | `ai_tutor_id` does not match an active `cc_bot_agent` for this customer. |
| `234` | `Chatbot de IA nÃ£o encontrado ou inativo` | `ai_chatbot_id` does not match an active `cc_bot_agent` for this customer. |
| `235` | `Nenhum template vÃ¡lido encontrado` | None of the `templates` ids was valid for the customer. |
| `236`/`237` | DB error | Insert failed at the database layer. |

> **Note**
> Error messages are returned in Portuguese (verbatim from the legacy implementation). Prefer to map them to user-facing strings in your client.
