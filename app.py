import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# .envファイルからAPIキーを読み込む（安全対策）
load_dotenv()
API_KEY = os.getenv('DIFY_API_KEY')

app = Flask(__name__)

# 1. ユーザーがアクセスしてきたら、画面（HTML）を表示する
@app.route('/')
def home():
    return render_template('index.html')

# 2. 画面から質問が来たら、ここで鍵をつけてDifyに問い合わせる
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Difyへの問い合わせ設定
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "user": "sazan-user"
    }

    try:
        response = requests.post(
            'https://api.dify.ai/v1/chat-messages',
            headers=headers,
            json=payload
        )
        data = response.json()
        return jsonify({'answer': data.get('answer', 'エラーが発生しました')})
    except Exception as e:
        return jsonify({'answer': 'サーバーエラーが発生しました'}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)