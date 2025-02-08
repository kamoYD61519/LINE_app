import requests
import datetime
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# LINE Messaging API のチャネルアクセストークン（Long-lived token）
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_LINE_CHANNEL_ACCESS_TOKEN'

# メッセージ送信関数
def send_line_message(reply_token, messages):
    """
    LINEユーザーにメッセージを返信する
    """
    line_api = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": messages
    }
    response = requests.post(line_api, headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"メッセージ送信失敗: {response.status_code}, {response.text}")

# Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received Webhook:", data)  # デバッグ用ログ

    # ライン無料スタンプの用意　https://developers.line.biz/ja/docs/messaging-api/sticker-list/
    sally=[]
    for i in range(10855,10895): 
        sally.append([789,i]) # [packageId,steckerID]

    if "events" in data and len(data["events"]) > 0:
        event = data["events"][0]  # 最初のイベントを取得
        reply_token = event.get("replyToken")  # 返信トークン取得
        user_message = event.get("message", {}).get("text", "").strip()  # ユーザーのメッセージを取得

        if not reply_token:
            return jsonify({"status": "no reply token"}), 200
        # もし「1, 2, 3」のメニュー選択肢が送られた場合、対応するメッセージを返す
        if user_message in ("1", "2", "3"):
            if user_message == "1":
                response_message = {"type": "text", "text": "こんにちは！ 僕は自動応答 Botです。"}
            elif user_message == "2":
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                response_message = {"type": "text", "text": f"今の時間は {current_time} です。"}
            elif user_message == "3":
                r=random.randint(0,len(sally)-1)
                pkgid,stkid=sally[r]
                response_message = {"type": "sticker", "stickerId": f"{stkid}", "packageId": f"{pkgid}"}  # ランダムに返信用スタンプをセットする

            send_line_message(reply_token, [response_message])
            return jsonify({"status": "response sent"}), 200

        # それ以外のメッセージにはメニューを送信
        menu_message = {
            "type": "text",
            "text": "次の中から希望メニュー(数字)を選んでください。\n  1. 自己紹介をする\n  2. 今の時間を教える\n  3. スタンプを返す"
        }
        send_line_message(reply_token, [menu_message])
        return jsonify({"status": "menu sent"}), 200

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)