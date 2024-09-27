from flask import Flask, request, render_template, make_response, redirect

app = Flask(__name__)

# admin_password 라는 텍스트 파일에 관리자의 비밀번호가 들어있습니다.
ADMIN_PASSWORD = open('./admin_password.txt', 'r').read()

# 아이디: 비밀번호를 1) 키, 2) 값 형태로 선언했습니다.
users = {
    'admin': ADMIN_PASSWORD,
    'user': '1234'
}


# 메인 라우터, content 라는 텍스트 파일에 저장된 내용을 보여줍니다.
@app.route('/')
def index():
    content = open('./content.txt', 'r').read()

    response = ''
    try:
        cookie = request.cookies.get('cookie', None)
        id, password = cookie.split(",")
        pw = users[id]
        if id == 'admin' and password == pw:
            response += '<h1>당신은 관리자입니다.</h1>'.format(password)
    except:
        print('error')

    # 취약한 부분으로 사용자가 입력한 내용을 필터링 없이 그대로 보여줍니다.
    response += '<h1>"등록된 내용 " {0}</h1>'.format(content)

    return response


# 게시판
@app.route('/board', methods=['GET', 'POST'])
def board_write():
    # GET 요청이면 board.html 을 보여줍니다.
    if request.method == 'GET':
        return render_template('board.html')
    # POST 요청이면 전달받은 content 를 텍스트 파일에 저장해줍니다.
    else:
        # 취약한 부분으로, 사용자가 입력한 내용을 검사하지 않고 그대로 저장합니다.
        content = request.form.get('content')
        f = open("content.txt", 'w')
        f.write(content)
        f.close()
        return '<script>alert("글이 등록되었습니다.");location.href="/"</script>'


# 로그인 라우터
@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET 요청이면 로그인을 위한 html 을 보여줍니다.
    if request.method == 'GET':
        return render_template('login.html')
    # POST 요청이면 로그인을 진행합니다.
    else:
        id = request.form.get('id')
        password = request.form.get('password')

        try:
            pw = users[id]
        except:
            return '<script>alert("등록되지 않은 유저입니다."); history.go(-1)</script>'

        if password != pw:
            return '<script>alert("잘못된 비밀번호 입니다."); history.go(-1)</script>'
        else:
            # 로그인에 성공하면 메인으로 리다이렉트 시켜줍니다.
            resp = make_response(redirect('/'))
            # 로그인에 성공하면 아이디,비밀번호 형태를 쿠키로 저장합니다.
            resp.set_cookie('cookie', "{0},{1}".format(id, users[id]))
            return resp
