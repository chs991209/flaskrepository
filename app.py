import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask_wtf.csrf import CSRFProtect

from forms import LoginForm, RegisterForm
from models import db, Fcuser

app = Flask(__name__)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')
        return redirect('/')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser)
        db.session.commit()
        print('Success!')

        return redirect('/')

    return render_template('register.html', form=form)


@app.route('/')
def hello():
    userid = session.get('userid', None)
    return render_template('hello.html', userid=userid)


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # app내 app 설정
    app.config['SECRET_KEY'] = 'laskdjldskajflkasjdlk'

    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)  # 초기화
    db.app = app
    db.create_all()  # db 생성
    app.run(host='127.0.0.1', port=5000, debug=True)