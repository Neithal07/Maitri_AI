from flask import Flask, request, render_template_string

app = Flask(__name__)
alerts = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Ground Station Alerts</title>
<style>
body {
    background:#0b0f1a;
    color:#e0e6ff;
    font-family: Arial;
}
header {
    background:#12182b;
    padding:15px;
    text-align:center;
    font-size:22px;
}
.alert {
    background:#12182b;
    border:1px solid #1f2a4d;
    margin:10px;
    padding:10px;
    border-radius:6px;
}
.intensity { color:#ff4d4d; font-weight:bold; }
</style>
<meta http-equiv="refresh" content="60">
</head>

<body>
<header>🚨 Ground Station Alerts</header>

{% for a in alerts[::-1] %}
<div class="alert">
⏱ {{a.time}} <br>
💬 {{a.text}} <br>
<div class="intensity">🔥 Intensity: {{a.intensity}}</div>
</div>
{% endfor %}

</body>
</html>
"""

@app.route("/alert", methods=["POST"])
def receive_alert():
    alerts.append(request.json)
    return "ok"

@app.route("/")
def dashboard():
    return render_template_string(HTML, alerts=alerts)

app.run(host="0.0.0.0", port=8000)
