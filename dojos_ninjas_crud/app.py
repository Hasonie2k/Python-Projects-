from flask import Flask, render_template, url_for, redirect, request
from mysqlconnection import connectToMySQL
from models import Dj, Ninjas

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            query = "INSERT INTO dojos_ninjas.dojos (name) VALUES (%(name)s);"
            data = {"name": name}
            dojo_id = connectToMySQL('dojos_ninjas').query_db(query, data)
            return redirect(url_for("info", dojo_id=dojo_id))
    else:
        dojos = Dj.get_all()
        return render_template("index.html", dojos=dojos)

@app.route('/dojos/ninjas/<int:dojo_id>', methods=["GET", "POST"])
def info(dojo_id):
    dojo = Dj.get_one({"id": dojo_id})
    ninjas = Ninjas.get_all_ninjas()

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        if first_name and last_name and age:
            ninja_data = {"first_name": first_name, "last_name": last_name, "age": age, "dojo_id": dojo_id}
            Ninjas.add_ninja(ninja_data)
    return render_template('info.html', dojo=dojo, ninjas=ninjas)

if __name__ == "__main__":
    app.run(debug=True)
