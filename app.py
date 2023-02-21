# app.py

from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = str(random.randrange(11111, 99999))
messages = []

def load_messages():
    global messages
    if os.path.exists("messages.json"):
        with open("messages.json", encoding="UTF-8") as f:
            messages = json.load(f)

def save_messages():
    with open("messages.json", "w", encoding="UTF-8") as f: # , 
        json.dump(messages, f, indent=2, ensure_ascii=False) # , ensure_ascii=False

@app.route('/')
def index():
    try: session['login']
    except: return render_template('login.html')
    else:
        load_messages()
        return render_template('index.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    try: session['login']
    except: return render_template('login.html')
    else:
        name = session['login']
        message = request.form['message']
        if message == "":
            return redirect(url_for('index'))
        else:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            messages.append({'name': name, 'message': message, 'timestamp': timestamp})
            save_messages()
            return redirect(url_for('index'))


#! 회원 기능 --->

# 회원 정보가 저장될 json 파일 경로
USER_DATA_FILE = 'user_data.json'

# 회원가입 페이지
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        email = request.form.get('email')
        
        # json 파일에서 모든 사용자 정보를 가져와 중복 닉네임 체크
        with open(USER_DATA_FILE, 'r') as f:
            user_data = json.load(f)
        for user in user_data:
            if user['nickname'] == nickname:
                return render_template('signup.html', error="Already Nickname!")

        # 새로운 유저 정보 생성
        user_info = {
            'nickname': nickname,
            'password': password,
            'email' : email,
            'join_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # json 파일에 새로운 유저 정보 추가
        with open(USER_DATA_FILE, 'w') as f:
            user_data.append(user_info)
            json.dump(user_data, f, indent=4)

        return redirect(url_for('login'))

    return render_template('signup.html', error="None")

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')

        # json 파일에서 해당 닉네임의 유저 정보를 가져와 비밀번호 확인
        with open(USER_DATA_FILE, 'r') as f:
            user_data = json.load(f)
        for user in user_data:
            if user['nickname'] == nickname:
                if user['password'] == password:
                    session['login'] = nickname
                    return redirect(url_for('index'))

                else:
                    return render_template('login.html', error="Wrong Password")

        return render_template('login.html', error="None Nickname")

    return render_template('login.html', error="None")

#! 실행 --->
if __name__ == '__main__':
    app.run(debug=True)