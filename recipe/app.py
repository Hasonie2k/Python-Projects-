from flask import Flask, render_template, redirect, request, url_for, flash, session
from model import User
from model_r import Recipe
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'very_secret'
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def log_reg():
    return render_template('login.html')

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
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('log_reg'))

@app.route('/menu')
def hello():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    recipes = Recipe.get_all()
    return render_template('menu.html', user=user, recipes=recipes , users_id=user.id)

@app.route('/view/<name>' , methods=['GET'])
def view(name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    recipe = Recipe.get_by_name(name)
    return render_template('view_recipe.html', user=user, recipe=recipe)

@app.route('/create/recipe')
def create():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    return render_template('create.html', user=user)

@app.route('/update/recipe' , methods=['POST', 'GET'])
def update():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    recipe = Recipe.get_by_id(session['user_id'])
    return render_template('update.html', user=user , recipe=recipe)

@app.route('/delete_recipe/<int:users_id>', methods=['POST'])
def delete_recipe(users_id):
    recipe = Recipe.get_by_id(users_id)
    if recipe is not None and recipe.users_id == session['user_id']:
        Recipe.delete_recipe_by_id(users_id)
    return redirect(url_for('hello'))

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

@app.route('/recipe/save', methods=['POST'])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/create/recipe')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'users_id': session['user_id'],
        'date_cooked': request.form['date_cooked'],
        'under': request.form['under']
    }
    Recipe.save_recipe(data)
    return redirect(url_for('hello'))

@app.route('/edit/recipe/<int:users_id>', methods=['GET', 'POST'])
def update_recipe(users_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    recipe = Recipe.get_by_id(users_id)
    if recipe is None or recipe.users_id != user.id:
        return redirect(url_for('hello'))
    if request.method == 'POST':
        if not Recipe.validate_recipe(request.form):
            return redirect(url_for('update_recipe', users_id=users_id))
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instruction': request.form['instruction'],
            'users_id': user.id,
            'date_cooked': request.form['date_cooked'],
            'under': request.form['under']
        }
        Recipe.update_recipe_by_id(users_id, data)
        return redirect(url_for('hello', name=recipe.name))
    return render_template('update.html', user=user, recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
