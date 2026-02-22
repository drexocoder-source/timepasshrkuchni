import os
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

BOT_NAME = "Gojo Satoru Bot"
BOT_USERNAME = "@YourBotUsername"
START_TIME = datetime.now()

def get_status():
    return "🟢 ONLINE"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Gojo Satoru Bot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(-45deg,#0f0c29,#302b63,#24243e,#000);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: white;
            text-align: center;
        }

        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .container {
            margin-top: 10%;
        }

        h1 {
            font-size: 48px;
            background: linear-gradient(90deg,#00f2ff,#00ff95);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { text-shadow: 0 0 10px #00f2ff; }
            to { text-shadow: 0 0 20px #00ff95; }
        }

        .card {
            margin: auto;
            margin-top: 30px;
            padding: 25px;
            width: 320px;
            background: rgba(255,255,255,0.08);
            border-radius: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 0 40px rgba(0,255,255,0.2);
        }

        .status {
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }

        .intro {
            font-size: 18px;
            opacity: 0.8;
        }

        footer {
            margin-top: 50px;
            opacity: 0.5;
            font-size: 14px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>⚡ Gojo Satoru ⚡</h1>

    <div class="card">
        <div class="intro">
            The Strongest Sorcerer is Watching Your Group.
        </div>

        <div class="status">
            Status: {{ status }}
        </div>

        <div>
            Uptime: {{ uptime }}
        </div>

        <div style="margin-top:10px;">
            Bot: {{ bot }}
        </div>
    </div>

    <footer>
        Domain Expansion • Unlimited Moderation
    </footer>
</div>

</body>
</html>
"""

@app.route("/")
def home():
    uptime = str(datetime.now() - START_TIME).split(".")[0]
    return render_template_string(
        HTML,
        status=get_status(),
        uptime=uptime,
        bot=BOT_USERNAME
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
