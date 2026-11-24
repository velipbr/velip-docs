# WebRTC softphone integration

*Put calls inside your own web app: your agents talk in the browser, your backend places the calls.*

This guide shows how a SaaS or CRM adds voice calls to its own agent screen using two endpoints:
[`GetWebRTC`](GetWebRTC.md) (softphone credentials) and [`MakeTTSCall`](MakeTTSCall.md) (the call itself).

**Before you start:** ask Velip support to enable WebRTC for your account, with the number of agents (softphones) you need. Until then `GetWebRTC` answers `204`.

## How it works

```
 Agent's browser                 Your backend                     Velip
 ───────────────                 ────────────                     ─────
 1. opens the agent screen ───►  2. GetWebRTC (token, userid) ──► returns sipname, sipsecret,
                                                                   wss_url, ice_servers
 3. registers the softphone ◄─── credentials
    (WebSocket + SIP) ─────────────────────────────────────────►  Velip WebRTC server
 4. agent clicks "Call" ───────► 5. MakeTTSCall
                                    dest  = sipname
                                    dest2 = customer number ────► 6. rings the agent's browser,
                                                                     then dials the customer and
 7. agent and customer talk ◄═══════════ audio (WebRTC) ═══════►     bridges both legs
```

1. When the agent opens your screen, your frontend asks **your backend** for the softphone credentials.
2. Your backend calls [`GetWebRTC`](GetWebRTC.md) with your API token and a `userid` that identifies the agent in your system.
3. Your frontend registers the softphone on the Velip WebRTC server with those credentials. The credentials stay valid while the page is open; there is no need to fetch new ones for each call.
4. When the agent wants to call, your frontend asks **your backend** to place the call.
5. Your backend calls [`MakeTTSCall`](MakeTTSCall.md) with `dest` = the agent's `sipname` and `dest2` = the customer's number.
6. Velip first rings the agent's browser (your page answers it automatically), then dials the customer and joins both legs.
7. Agent and customer talk. The audio goes straight between the browser and Velip; your backend only sends requests.

Calls never start from the browser. Your API token stays in your backend, and you decide who may call and how much each of your customers may spend before you call `MakeTTSCall`.

## Step 1 — Get the softphone credentials (backend)

Call [`GetWebRTC`](GetWebRTC.md) with the same token you use for the other endpoints:

```bash curl
curl -X POST 'https://<base>/api/v2/GetWebRTC.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -H 'Content-Type: application/json' \
  -d '{ "userid": "333xl33" }'
```

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
      { "urls": "stun:gv17.velip.com.br:3478" }
    ]
  }
}
```

- `userid` is the agent's id **in your system**: letters and digits only, 1 to 30 characters. Use one per agent and keep it stable; the same `userid` always returns the same softphone. The `sipname` is derived from it: store the `sipname` returned, do not build it yourself.
- Send to the browser only what the page needs (`sipname`, `sipsecret`, `sipserver`, `wss_url`, `ice_servers`), over HTTPS, and keep `sipsecret` out of logs and browser storage.
- To replace a softphone password (for example, after a leak), call `GetWebRTC` again with `"reset": "1"` in a POST. The old password stops working right away; pages using it must fetch the credentials again.

## Step 2 — Register the softphone (browser)

The example below uses [JsSIP](https://jssip.net) 3.10.0. It registers the softphone, answers the call that Velip places to the agent, plays the remote audio and offers *Hang up* and *Mute*. Adapt it to your framework.

Serve JsSIP from your own site: download the browser build `jssip-3.10.0.min.js` from the [JsSIP downloads](https://jssip.net/download/) (or bundle the `jssip@3.10.0` npm package with your app). Loading it from a third-party host would let that host run code on your agent screen.

Your page must be served over **HTTPS** (browsers only give microphone access to secure pages) and needs an audio element for the remote party:

```html
<audio id="remoteAudio" autoplay></audio>
<button id="btnHangup" disabled>Hang up</button>
<button id="btnMute" disabled>Mute</button>
<span id="phoneStatus">offline</span>

<script src="/js/jssip-3.10.0.min.js"></script>  <!-- your own copy, see above -->
<script>
  // Credentials from your backend (Step 1). Never call GetWebRTC from the browser:
  // that would expose your API token.
  async function startSoftphone() {
    const creds = await fetch('/your-backend/webrtc-credentials').then(r => r.json());

    const remoteAudio = document.getElementById('remoteAudio');
    const status = (text) => { document.getElementById('phoneStatus').textContent = text; };
    let session = null;

    const ua = new JsSIP.UA({
      sockets: [new JsSIP.WebSocketInterface(creds.wss_url)],
      uri: 'sip:' + creds.sipname + '@' + creds.sipserver,
      password: creds.sipsecret,
      display_name: 'Agent',          // free text
      register: true,
      register_expires: 300,
      session_timers: false,
    });

    ua.on('connected',          () => status('connected'));
    ua.on('disconnected',       () => status('connection lost'));   // JsSIP retries by itself
    ua.on('registered',         () => status('ready'));
    ua.on('unregistered',       () => status('not registered'));
    ua.on('registrationFailed', (e) => status('registration failed: ' + e.cause));

    // Velip calls the agent first: answer it automatically.
    ua.on('newRTCSession', (e) => {
      if (e.session.direction !== 'incoming') return;
      if (session) { e.session.terminate(); return; }   // one call at a time
      session = e.session;

      session.on('peerconnection', (ev) => {
        ev.peerconnection.addEventListener('track', (t) => {
          remoteAudio.srcObject = t.streams[0];
        });
      });
      session.on('confirmed', () => { status('in call'); setButtons(true); });
      session.on('ended',     () => { status('ready');   setButtons(false); session = null; });
      session.on('failed',    () => { status('ready');   setButtons(false); session = null; });

      session.answer({
        mediaConstraints: { audio: true, video: false },
        pcConfig: { iceServers: creds.ice_servers },
      });
    });

    function setButtons(inCall) {
      document.getElementById('btnHangup').disabled = !inCall;
      document.getElementById('btnMute').disabled = !inCall;
    }
    document.getElementById('btnHangup').onclick = () => { if (session) session.terminate(); };
    document.getElementById('btnMute').onclick = () => {
      if (!session) return;
      if (session.isMuted().audio) session.unmute({ audio: true }); else session.mute({ audio: true });
    };

    ua.start();
  }

  startSoftphone();
</script>
```

Hanging up in the browser ends the whole call (both legs). Show the agent the softphone state (`ready`, `connection lost`, `in call`) and hide your *Call* button while a call is active, as in the events above.

## Step 3 — Place the call (backend)

When the agent clicks *Call* in your screen, your backend checks what it needs (permissions, your customer's balance) and calls [`MakeTTSCall`](MakeTTSCall.md):

```bash curl
curl -X POST 'https://<base>/api/v2/MakeTTSCall.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "3",
    "priority": "-1",
    "dest": "VW1234XNCEJDrzS",
    "dest2": "5511999999999",
    "content": "tf19472806",
    "contentfail": "tf481661861",
    "content1": "",
    "content2": "",
    "rec": "300",
    "timelimit": "300",
    "free": "1"
  }'
```

| Field | Value |
| --- | --- |
| `type` | `3`: the second leg (`dest2`) is dialed as soon as the first leg (the agent's browser) answers. |
| `priority` | `-1`: dial immediately. |
| `dest` | The agent's `sipname` from Step 1. It must be a softphone of **your** account; otherwise the call is rejected with `203`. |
| `dest2` | Customer number with country and area code (e.g. `5511999999999`). |
| `content` | Audio the agent hears before the customer is dialed. `tf19472806` is a short silence provided by Velip. |
| `contentfail` | Audio the agent hears when the customer does not answer. `tf481661861` is provided by Velip; you can use your own audio ([`GetAudiosList`](../audio-files/GetAudiosList.md)). |
| `content1`, `content2` | Optional audios played when the customer answers. Leave them empty. |
| `rec` | Seconds of the call to record (`0` = do not record). |
| `timelimit` | Maximum call length in seconds. |
| `free` | `1` = do not check the Procon do-not-call list. Use it only when your contract and the call purpose allow it. |

```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "cd_id": "e_368915"
  }
}
```

The agent's browser rings almost immediately; your page answers it (Step 2) and then the customer is dialed. For the agent this is transparent: they click *Call* and hear the customer's phone ringing.

## Step 4 — Follow the call

`cd_id` identifies the call. Use it to:

- query the call with [`GetCallStatus`](GetCallStatus.md);
- receive the end-of-call webhook with all call data, including the charged rate (`rurl` in [`MakeTTSCall`](MakeTTSCall.md), or the account's default callback; see [Webhook delivery](GetCallStatus.md#webhook-delivery));
- find it in the Velip web reports.

## Rules and limits

- WebRTC is enabled per account by Velip, with a number of softphones (`204` from `GetWebRTC` while it is not enabled; `203` when a new `userid` would pass the number). Contact Velip support to enable it or raise the number.
- `GetWebRTC`: `userid` with letters and digits only, 1 to 30 characters (`201` otherwise).
- `MakeTTSCall` dials only softphones of your own account in `dest` / `dest2`.
- The credentials returned by `GetWebRTC` are a password: anyone who has them can register as that agent. Deliver them only to the logged-in agent's page and use `reset` if they leak.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `registrationFailed` with `Authentication Error` | The page is using an old `sipsecret` (for example, after a `reset`). Fetch the credentials again. |
| `disconnected` right after start | The page reaches `wss_url` over port 443. Corporate proxies that block WebSocket prevent the connection. |
| Call connects but there is no audio | Microphone permission denied, page not served over HTTPS, or the browser blocked autoplay of `remoteAudio` (the agent must interact with the page once before the first call). Networks that block UDP may also prevent audio: contact Velip support. |
| `MakeTTSCall` returns `203 number invalid` with `dest` = sipname | `dest` is not a softphone of the account that owns the token, or was mistyped. Use the `sipname` exactly as returned by `GetWebRTC`. |
