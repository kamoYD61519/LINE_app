import requests

# LINE公式アカウントのチャネルアクセストークン（Long-lived token）
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_LINE_CHANNEL_ACCESS_TOKEN'

# 送信先のユーザーID（Webhookのreceived msgのsourceから取得）
LINE_USER_ID = 'DESTINATION_USER_ID'

def main():
    send_line_message('Hello, my dear friend.\nThis is a test message.')

def send_line_message(notification_message):
    """
    LINEにメッセージを送信する（Messaging API）
    """
    line_api = 'https://api.line.me/v2/bot/message/push'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}' #ベアラートークン:持参人トークン
    }
    
    data = {
        'to':LINE_USER_ID,
        'messages': [{'type': 'text', 'text': notification_message}]
    }
    
    response = requests.post(line_api, headers=headers, json=data)
    
    if response.status_code == 200:
        print("メッセージ送信成功")
    else:
        print(f"メッセージ送信失敗: {response.status_code}, {response.text}")

if __name__ == "__main__":
    main()