from flask import Flask, render_template, request, redirect, session, url_for, g, flash
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import EqualTo

app = Flask(__name__)
app.secret_key = 'mixshades'

class LoginForm(Form):
    admin = 'admin'
    username = StringField('username', validators=[EqualTo('admin',message='must login as admin')])

@app.after_request
def remove_if_invalid(response):
    if "__invalidate__" in session:
        response.delete_cookie(app.session_cookie_name)
    return response

@app.route('/', methods=['GET','POST'])
def login():
    session['user'] = None
    error = None
    form = LoginForm()
    if request.method =='POST':
        session['user'] = request.form['username']
        if request.form['username']=='admin':
            return redirect(url_for('counter'))
        else:
            error = 'invalid username. must be "admin".'
    return render_template('login.html', form=form, error = error)

@app.route('/logout', methods=['POST','GET'])
def logout():
    session['user'] = None
    session['counter'] = 0
    return redirect('/')

@app.route('/counter', methods=['GET','POST'])
def counter():
    if session['user'] != 'admin':
        error = 'must login as admin.'
        return redirect('/')
    else:
        try:
            session['counter']
        except:
            session['counter'] = 0
        session['counter'] += 1
        return render_template('counter.html')


@app.route('/add2', methods=['POST'])
def add2():
    session['counter'] += 1
    return redirect('/counter')

@app.route('/reset', methods=['POST'])
def reset():
    session['counter'] = 0
    return redirect('/counter')

if __name__ == '__main__':
    app.run(debug=True)
