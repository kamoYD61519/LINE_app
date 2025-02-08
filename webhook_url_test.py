from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])  # POSTリクエストを許可
# webhook 接続テスト
def webhook():
    data = request.get_json()
    print("Received Webhook:", data)  # 受信データをログ出力

    if data and "events" in data and len(data["events"]) > 0:
        event = data["events"][0]
        if "source" in event and "userId" in event["source"]:
            user_id = event["source"]["userId"]
            print("Your LINE User ID:", user_id)

    return jsonify({"status": "ok"}), 200  # 必ず200 OKを返す

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)