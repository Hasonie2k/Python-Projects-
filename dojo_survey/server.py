from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['message'] = request.form['message']
        return redirect(url_for('result'))
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('results.html', name=session['name'], email=session['email'], message=session['message'])

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('form'))
    else:
        return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True) 
