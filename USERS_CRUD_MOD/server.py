from flask import Flask, render_template,  request, redirect
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

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        user_id = request.values.get('id')
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        connection = connect('users')
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET first_name=%s, last_name=%s, email=%s WHERE id=%s', (first_name, last_name, email, user_id))
        connection.commit()
        connection.close()
        return redirect('/')
    else:
        user_id = request.args.get('id')
        connection = connect('users')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id=%s', id)
        user = cursor.fetchone()
        connection.close()
        return render_template('update.html', user=user)
    
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    connection = connect('users')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id=%s', user_id)
    connection.commit()
    connection.close()
    return redirect('/')
    
    
if __name__ == '__main__':
    app.run(debug=True)