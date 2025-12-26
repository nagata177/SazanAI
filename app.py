import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 1. トップページを表示
@app.route('/')
def home():
    return render_template('index.html')

# 2. チャットのやり取りをする場所
@app.route('/chat', methods=['POST'])
def chat():
    # 画面から送られてきた「message」を受け取る
    user_message = request.json.get('message')
    
    # Renderに設定したキーを読み込む
    api_key = os.environ.get('DIFY_API_KEY')
    
    if not api_key:
        return jsonify({'answer': 'エラー: DIFY_API_KEYが設定されていません'}), 500

    # Difyへ送る手紙の準備
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "user": "sazan-user"
    }

    try:
        # Difyに送信！
        response = requests.post(
            'https://api.dify.ai/v1/chat-messages',
            headers=headers,
            json=payload
        )
        data = response.json()
        
        # 【重要】もし答えがなかったら、Difyからのエラーメッセージをそのまま表示する
        answer = data.get('answer')
        if not answer:
            # エラーの正体を画面に出す
            return jsonify({'answer': f"【Difyからのエラー】: {str(data)}" })
            
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'answer': f"サーバー内部エラー: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
