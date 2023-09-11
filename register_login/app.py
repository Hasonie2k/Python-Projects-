from flask import Flask, render_template, redirect, flash, request, url_for, session
from mysqlconnection import connectToMySQL
from user_model import User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'verysecret'

bcrypt = Bcrypt(app)

@app.route('/')
def log_reg():
    return render_template('/index.html')

@app.route('/register/user' , methods=['POST'])
def add_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password' : pw_hash,
    }
    new_user_id = User.save_user(data)
    session['user_id'] = new_user_id
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_by_email(email)
        if user:
            if bcrypt.check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('hello'))
            else:
                flash('Invalid email or password.')
                return redirect(url_for('log_reg'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('log_reg'))
    return render_template('hello.html' , user=user)


@app.route('/hello')
def hello():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    return render_template('hello.html')


if __name__ == '__main__':
    app.run(debug=True)
