import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User
from flask import session
from flask_wtf.csrf import CSRFProtect
from Forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/')
def mainpage():
    userid = session.get('userid', None)
    return render_template('main.html', userid=userid)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        usertable = User()
        usertable.userid = form.data.get('userid')
        usertable.email = form.data.get('email')
        usertable.password = form.data.get('password')

        db.session.add(usertable)
        db.session.commit()
        return "등록성공"
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('{}가 로그인'.format(form.data.get('userid')))
        session['userid']=form.data.get('userid')
        return redirect('/')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']='wcsfeufhwiquehfdx'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()

    app.run(host="127.0.0.1", port=5000, debug=True)