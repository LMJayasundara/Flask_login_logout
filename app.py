from logging import log
from flask import Flask, render_template, session, request, redirect, url_for
import os
from functools import wraps
app = Flask(__name__)

app.secret_key = os.urandom(24)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            print('Unauthorized, Please login')
            return redirect(url_for('index'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # print(username)
        if username == 'shan' and password == '123':

            session['logged_in'] = True
            session['username'] = username
            print("You are now logged in")

            return redirect(url_for('protect'))
    return render_template('index.html')

@app.route('/protect')
@is_logged_in
def protect():
    return render_template('protect.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    print('You are now logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)