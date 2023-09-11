from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
app.config['style.css'] = 'static'
import pymysql

def connect(users):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db=users,
        autocommit=True
    )
    return connection

@app.route('/')
def index():
    connection = connect('users')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    connection.close()
    return render_template('read.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        connection = connect('users')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (first_name, last_name , email) VALUES (%s, %s,%s)', (first_name, last_name ,email))
        connection.commit()
        connection.close()
        return redirect('/')
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)