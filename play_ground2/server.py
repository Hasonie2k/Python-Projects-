from flask import Flask , render_template
app = Flask(__name__)

@app.route('/play')
def section_1():
    return render_template('index.html', number= 1 , box_color="blue")

@app.route('/play/<int:x>')
def section_2(x):
    return render_template('index.html' , number= x , box_color="blue")

@app.route('/play/<int:x>/<string:color>')
def section_3(x , color):
    return render_template('index.html', number= x , box_color= color)

if __name__=="__main__":
    app.run(debug=True)