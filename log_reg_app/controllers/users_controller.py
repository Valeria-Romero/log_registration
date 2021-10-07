from flask import render_template, request, redirect, session, flash
from log_reg_app import app
from log_reg_app.models.User import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/", methods=['GET'])
def load_main_page():
    return render_template("index.html")

@app.route("/user/add", methods=['POST'])
def add_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    encrypted_password = bcrypt.generate_password_hash(password)
    password_confirmation = request.form['confirm_password']


    if User.validate_registry(first_name, last_name, email, encrypted_password, password, password_confirmation):
        new_user = User(first_name, last_name, email, encrypted_password)
        User.add_new_user(new_user)
        return redirect("/")
    else:
        print("something went wrong")
        return redirect("/")

@app.route("/login", methods=['POST'])
def login_validation():
    email = request.form['login_email']
    password = request.form['login_password']

    result = User.validate_login(email)
    print(result)
    if result == ():
        flash("email not registered")
        return redirect("/")
    else:
        database_password = result[0]['password']
        if result[0]['email'] == email:

            if bcrypt.check_password_hash(database_password, password):
                session.clear()
                data={
                    'id':result[0]['id'],
                    'First_name': result[0]['First_name']
                }
                session['id'] = result[0]['id']
                print(session['id'])
                return redirect("/dashboard")
            else:
                flash("Wrong password, try again")

    return redirect("/")

@app.route("/dashboard", methods=['GET'])
def load_dashboard_page():
    if 'id' not in session:
        return redirect('/')
    user_info = User.get_one(session['id'])
    data = {
        "id": session['id'],
        "first_name": user_info[0]['first_name']
    }
    return render_template("dashboard.html", data=data)

@app.route("/logout", methods=['GET'])
def logout_session():
    session.clear()
    return redirect("/")
