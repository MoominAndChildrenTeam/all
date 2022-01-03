from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mail import Mail, Message
from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib
import random

client = MongoClient('mongodb+srv://jcode:1234@cluster0.z0xvg.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbsparta

RANDOM_CHAR = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZ'
CHOISE_CHAR = ''

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jcodeofficer@gmail.com'
app.config['MAIL_PASSWORD'] = 'Gpassword4whatO!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
SECRET_KEY = 'fuckingFlask'

def send_mail(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)

def send_auth_email(email):
    try:
        global CHOISE_CHAR
        CHOISE_CHAR = "".join(random.sample(RANDOM_CHAR, 6))

        text = f'인증번호 : {CHOISE_CHAR}'
        send_mail('Moominstagram', sender='jcodeofficer@gmail.com', recipients=[email], text_body=text)
        return True
    except:
        return False

def isLogin():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"email": payload['email']})
        return user_info
    except:
        return False


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"email": payload['email']})

        all_posts = list(db.posts.find({}, {'_id': False}))


        return render_template('index.html', nickname=user_info['nickname'], auth=user_info['auth'], posts=all_posts)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))





########################### Login / Register #############################################

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register2')
def register2():
    return render_template('register2.html')


##################### MENU #############################################

# 검색
@app.route('/search')
def search():
    return render_template('search.html')

# 글쓰기
@app.route('/write')
def write():
    return render_template('write.html')

# 좋아요/찜
@app.route('/like')
def like():
    return render_template('like.html')

# 마이페이지
@app.route('/mypage')
def my_page():
    return render_template('mypage.html')


##################### API #############################################

# 닉네임 중복 체크
@app.route('/api/checknick', methods=['POST'])
def api_check_nickname():
    nickname = request.form['nickname']

    if db.users.find_one({'nickname':nickname}):
        return jsonify({'result':'fail', 'msg': '이미 존재하는 닉네임입니다.'})
    else:
        return jsonify({'result': 'success', 'msg': '닉네임 중복 인증 성공'})

# 이메일 중복 체크
@app.route('/api/checkemail', methods=['POST'])
def api_check_email():
    email = request.form['email']

    if db.users.find_one({'email':email}):
        return jsonify({'result':'fail', 'msg': '가입된 이메일입니다.'})
    else:
        return jsonify({'result': 'success', 'msg': '닉네임 중복 인증 성공'})


# 회원가입
@app.route('/api/register', methods=['POST'])
def api_register():
    email = request.form['email']
    nickname = request.form['nickname']
    pw = request.form['pw']

    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    if db.users.find_one({'email':email}):
        return jsonify({'result':'fail', 'msg': '가입된 이메일입니다.'})

    if db.users.find_one({'nickname':nickname}):
        return jsonify({'result':'fail', 'msg': '이미 존재하는 닉네임입니다.'})


    if send_auth_email(email) == False:
        return jsonify({'result': 'fail', 'msg': '올바른 이메일을 입력하세요'})

    doc = {
        'email': email,
        'nickname': nickname,
        'pw': pw_hash,
        'auth': False
    }

    db.users.insert_one(doc)

    # 로그인
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5000)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return jsonify({'result':'success', 'msg': '1차 회원가입 성공', 'token':token})

# 이메일 인증번호 재전송
@app.route('/api/resend', methods=['POST'])
def api_resned():
    user_info = isLogin()
    if user_info:
        if send_auth_email(user_info['email']):
            return jsonify({'result': 'success', 'msg': '이메일 재전송'})
        else:
            return jsonify({'result': 'fail', 'msg': '이메일 재전송 실패 - 이메일 오류 '})
    else:
        return jsonify({'result': 'fail', 'msg': '로그인 first'})

# 이메일 인증번호 발송
@app.route('/api/register2', methods=['POST'])
def api_register2():
    user_checked = isLogin()
    if user_checked:
        EMAIL_AUTH_KEY = request.form['emailauth']
        if EMAIL_AUTH_KEY == CHOISE_CHAR:
            db.users.update_one(user_checked, {'$set': {'auth': True}})
            return jsonify({'result': 'success', 'msg': '이메일 인증 성공'})
        else:
            return jsonify({'result': 'fail', 'msg': '잘못된 인증번호 입니다.'})
    else:
        return jsonify({'result': 'fail', 'msg': '로그인 해주세요'})

# 로그인
@app.route('/api/login', methods=['POST'])
def api_login():
    email = request.form['id']
    pw = request.form['pw']

    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    doc = {
      'email': email,
      'pw': pw_hash
    }

    result = db.users.find_one(doc)

    print(result)

    if result is not None:
        payload = {
           'email': email,
           'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5000)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})

    else:
       return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



@app.route('/api/write', methods=['POST'])
def api_write():
    coment = request.form['coment']
    login_user = isLogin()
    doc = {
        'nickname' : login_user['nickname'],
        'coment': coment,
        'like' : 0,
        'date': datetime.datetime.utcnow(),
    }

    db.posts.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '게시물 작성 완료'})





if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)