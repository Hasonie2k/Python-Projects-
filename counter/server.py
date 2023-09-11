from flask import Flask, render_template, redirect,  session , url_for

app = Flask(__name__)
app.secret_key = "verysecret123"

@app.route('/')
def root_route():
    if 'count' in session: 
        session ['count'] += 1
    else:
        session ['count'] = 0
    return render_template('index.html', count=session['count'])

@app.route('/reset')
def clear():
    session.clear()
    return redirect('/')

@app.route('/add_two')
def add_two():
    session['count'] +=1
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)