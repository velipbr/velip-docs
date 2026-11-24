# Get WebRTC SIP credentials

*Credentials of a WebRTC softphone for one agent of your system.*


**Endpoint:** `POST https://<base>/api/v2/GetWebRTC.php`

Returns the SIP user, password and server that a browser softphone uses to register on the Velip WebRTC server. The softphone is identified by your `userid`: the first call creates it with a random password, later calls return the same credentials.

The endpoint must be enabled for your account by Velip, with the number of softphones you need. Until then it answers `204` (HTTP 403); ask Velip support to enable it.

Call this endpoint **from your backend**, never from the browser, and pass to the agent's page only the returned credentials. The full flow (register the softphone, place the call with [`MakeTTSCall`](MakeTTSCall.md), answer it in the browser) is in the [WebRTC softphone integration guide](webrtc-softphone.md); to try it without writing code, use the [WebRTC softphone demo](https://developers.velip.com.br/api/v2/voice/webrtc-demo.html).

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account (or the `Authorization: Bearer` header).


#### `userid` — type: *string* — **required**

Id of the agent **in your system**: letters and digits only (`A-Z`, `a-z`, `0-9`), 1 to 30 characters, case-sensitive. Use one per agent and keep it stable. The softphone name (`sipname`) is derived from it and is not the `userid` itself.


#### `reset` — type: *string*

`1` replaces the softphone password and returns the new one. **POST only** (`205` otherwise). Use it when the credentials leak. The old password stops working right away: a page registered with it stops receiving calls and must register again with the new one.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetWebRTC.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -H 'Content-Type: application/json' \
  -d '{ "userid": "333xl33" }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "sipname": "VW1234XNCEJDrzS",
    "sipsecret": "yEVPQavMUe6O",
    "sipserver": "gv17.velip.com.br",
    "wss_url": "wss://gv17.velip.com.br/ws",
    "ice_servers": [
      { "urls": "stun:stun.l.google.com:19302" },
      { "urls": "stun:gv17.velip.com.br:3478" },
      { "urls": "turns:vox14.velip.com.br:443?transport=tcp", "username": "...", "credential": "..." }
    ]
  }
}
```

```json 400 Validation
{
  "return": {
    "status": "Invalid userid",
    "status_code": "201",
    "sipname": "",
    "sipsecret": "",
    "sipserver": ""
  }
}
```
- **`return.sipname`** (*string*) — SIP user of the softphone (15 characters, always the same for the same `userid`). It is also the `dest` you send to [`MakeTTSCall`](MakeTTSCall.md) to call this agent.


- **`return.sipsecret`** (*string*) — SIP password. It stays the same until you call with `reset=1`.


- **`return.sipserver`** (*string*) — SIP domain: the softphone registers as `sip:<sipname>@<sipserver>`.


- **`return.wss_url`** (*string*) — WebSocket address of the SIP server (port 443).


- **`return.ice_servers`** (*array*) — STUN and TURN servers to use in the browser `RTCPeerConnection` (`pcConfig.iceServers`), as returned. The TURN entry (TLS on port 443, with `username` and `credential`) relays the audio on networks that block UDP. Pass the list as it comes; do not store or log the TURN credential.


`sipname`, `sipsecret` and `sipserver` come empty on any error; `wss_url` and `ice_servers` come only on success.

## Error codes

| HTTP | Code | `status` | Cause |
| --- | --- | --- | --- |
| 400 | `200` | `No userid` | Missing `userid` parameter. |
| 400 | `201` | `Invalid userid` | `userid` has characters other than letters and digits, or more than 30 characters. |
| 400 | `203` | `WebRTC user limit reached` | The account already has all the softphones enabled for it, and this `userid` is new. Contact Velip support to raise the number. |
| 403 | `204` | `WebRTC not enabled for this account` | The endpoint is not enabled for the account. Contact Velip support. |
| 400 | `205` | `reset requires POST` | `reset=1` sent in a GET request. |
| 500 | `500` | `Internal error` | Temporary failure. Try again later. |

Authentication failures return HTTP 401 with the [global authentication codes](../errors.md).

> **Warning**
> The credentials are a password: anyone who has them can register as that agent and receive the calls placed to it. Send them only to the logged-in agent's page, over HTTPS; keep them out of logs and browser storage; use `reset=1` if they leak.
