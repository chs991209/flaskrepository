import os
from flask import Flask
from flask import render_template
from flask import request, redirect
from models import db, Fcuser


app = Flask(__name__)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    else:
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')

        if not (userid and username and password and re_password):
            return render_template('register.html')

        if password != re_password:
            return render_template('register.html')

        fcuser = Fcuser()
        fcuser.userid = userid
        fcuser.username = username
        fcuser.password = password

        db.session.add(fcuser)
        db.session.commit()

        return redirect('/')


@app.route('/')
def hello():
    return render_template('hello.html')


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # app내 app 설정

    db.init_app(app)  # 초기화
    db.app = app
    db.create_all()  # db 생성
    app.run(host='127.0.0.1', port=5000, debug=True)