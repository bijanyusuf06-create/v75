import os
is_scanning = False
update.message.reply_text("🛑 Scanning stopped.")




def status_command(update, context):
state = "scanning 🔍" if is_scanning else "stopped ⏸️"
update.message.reply_text(f"V75Analysis Bot status: {state}")


dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(CommandHandler('stop', stop_command))
dispatcher.add_handler(CommandHandler('status', status_command))


# -----------------------------
# Keep-alive Flask app + self-pinger
# -----------------------------
app = Flask(__name__)


@app.route('/')
def index():
return jsonify({"status": "V75Analysis Bot running"})




def self_pinger(url):
while True:
try:
requests.get(url, timeout=10)
except Exception:
pass
time.sleep(60 * 4) # ping every 4 minutes


# -----------------------------
# Runner
# -----------------------------


def run_bot():
# start websocket in thread
ws_thread = threading.Thread(target=start_ws, daemon=True)
ws_thread.start()
# start telegram polling
updater.start_polling()
print("Telegram polling started")
# start flask app in separate thread
flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=PORT), daemon=True)
flask_thread.start()
# start self-pinger
public_url = os.getenv('SELF_URL') or f"http://127.0.0.1:{PORT}"
pinger_thread = threading.Thread(target=lambda: self_pinger(public_url), daemon=True)
pinger_thread.start()
print("Service running. Press Ctrl+C to stop.")
try:
while True:
time.sleep(1)
except KeyboardInterrupt:
print("Shutting down...")
updater.stop()
if ws_app:
ws_app.close()


if __name__ == '__main__':
run_bot()