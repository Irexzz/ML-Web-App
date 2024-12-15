from application import app, db
from application import ai_model
from flask_bcrypt import Bcrypt
from application.models import Entry,Prediction
from datetime import datetime
from flask_login import login_user,current_user,logout_user,login_required

def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

def get_entry(id):
    try:
    # entries = Entry.query.filter(Entry.id==id) version 2
        result = db.get_or_404(Prediction, id)
        return result
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
        return 0
    
def get_entryuser(id):
    try:
    # entries = Entry.query.filter(Entry.id==id) version 2
        result = db.get_or_404(Entry, id)
        return result
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
        return 0


def get_entries(email):
    try:
    # entries = Entry.query.all() # version 2
        entries =db.session.execute(db.select(Prediction).order_by(Prediction.id)
                                    .filter(Prediction.email==email)).scalars()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
        return 0
    
def remove_entry(id):
    try:
    # entry = Entry.query.get(id) # version 2
        entry = db.get_or_404(Prediction, id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
        return 0
    
def remove_entryuser(id):
    try:
    # entry = Entry.query.get(id) # version 2
        entry = db.get_or_404(Entry, id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
        return 0
#Handles http://127.0.0.1:5000/hello
@app.route('/hello')
def hello_world():
    return "<h1>Hello World</h1>"


from flask import render_template,redirect,url_for
from application.forms import PredictionForm ,RegistrationForm,LoginForm
#Handles http://127.0.0.1:5000/
@app.route('/')
@app.route('/index')
@app.route('/home')
def index_page():
    form1 = PredictionForm()
    return render_template("index.html", form=form1, title="Enter Car Parameters")

from flask import render_template, request, flash
...
@app.route("/predict", methods=['GET','POST'])
def predict():
    form = PredictionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            tax = form.tax.data
            engine_size = form.engine_size.data
            model = form.model.data
            mileage = form.mileage.data
            year = form.year.data
            mpg = form.mpg.data
            car_mapping = {
                    'A1': 0,
                    'A2': 1,
                    'A3': 2,
                    'A4': 3,
                    'A5': 4,
                    'A6': 5,
                    'A7': 6,
                    'A8': 7,
                    'Q2': 8,
                    'Q3': 9,
                    'Q5': 10,
                    'Q7': 11,
                    'Q8': 12,
                    'R8': 13,
                    'RS3': 14,
                    'RS4': 15,
                    'RS5': 16,
                    'RS6': 17,
                    'RS7': 18,
                    'S3': 19,
                    'S4': 20,
                    'S5': 21,
                    'S8': 22,
                    'SQ5': 23,
                    'SQ7': 24,
                    'TT': 25
                }
            if model not in car_mapping:
                flash("Error: Invalid car model entered", "danger")
                return redirect(url_for('predict'))
            model_name = car_mapping[model]
            X = [[ tax,engine_size,model_name,mileage,year,mpg]]
            result = ai_model.predict(X)
            if current_user.is_authenticated:
                email = current_user.email
                new_entry = Prediction(email=email,
                    tax=tax,
                    engine_size=engine_size,
                    model=model,
                    mileage=mileage,
                    year=year,
                    mpg=mpg,
                    prediction=float(result[0]),
                    predicted_on=datetime.utcnow())
                add_entry(new_entry)
            flash(f"Predicted Car Price: ${result[0]}","success")
            
                
            
        else:
            flash("Error, cannot proceed with prediction","danger")
    return render_template("index.html", title="Enter Car Parameters", form=form, index=True )

bcrypt = Bcrypt()
@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user = User(email=form.email.data,password =hashed_password)
        email = form.email.data
        new_entry = Entry(email=email,
                    password=hashed_password)
        add_entry(new_entry)
        flash(f'Your account as been created','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_page'))
    form = LoginForm()
    if form.validate_on_submit():
        email = Entry.query.filter_by(email=form.email.data).first()
        if email and bcrypt.check_password_hash(email.password,form.password.data):
            login_user(email,remember=form.remember.data)
            return redirect(url_for('index_page'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index_page'))

@app.route("/history")
@login_required
def history():
    if current_user.is_authenticated:
                email = current_user.email
    return render_template('history.html',title='History',entries=get_entries(email))

@app.route('/remove', methods=['POST'])
def remove():
    form = PredictionForm()
    req = request.form
    id = req["id"]
    remove_entry(id)
    if current_user.is_authenticated:
                email = current_user.email
    return render_template("history.html", title="Enter Car Parameters",form=form, entries = get_entries(email), index=True)

from flask import json, jsonify
...
#API: add entry
@app.route("/api/add", methods=['POST'])
def api_add():
#retrieve the json file posted from client
    data = request.get_json()
    #retrieve each field from the data
    tax = data['tax']
    engine_size = data['engine_size']
    model = data['model']
    mileage = data['mileage']
    year = data['year']
    mpg = data['mpg']
    prediction = data['prediction']
    #create an Entry object store all data for db action
    new_entry = Prediction( tax=tax,
                           engine_size=engine_size,
                           model=model,
                           mileage=mileage,
                           year=year,
                           mpg=mpg,
    prediction = prediction,
    predicted_on=datetime.utcnow())
    #invoke the add entry function to add entry
    result = add_entry(new_entry)
    #return the result of the db action
    return jsonify({'id':result})

#API get entry
@app.route("/api/get/<id>", methods=['GET'])
def api_get(id):
    #retrieve the entry using id from client
    entry = get_entry(id)
    #Prepare a dictionary for json conversion
    data = {'id' : entry.id,
    'tax' : entry.tax,
    'engine_size' : entry.engine_size,
    'model' : entry.model,
    'mileage' : entry.mileage,
    'year': entry.year,
    'mpg':entry.mpg,
    'prediction': entry.prediction}
    #Convert the data to json
    result = jsonify(data)
    return result #response back


#API delete entry
@app.route("/api/delete/<id>", methods=['GET'])
def api_delete(id):
    entry = remove_entry(int(id))
    return jsonify({'result':'ok'})

#API: add entry
@app.route("/api/addu", methods=['POST'])
def api_addu():
#retrieve the json file posted from client
    data = request.get_json()
    #retrieve each field from the data
    email = data['email']
    password = data['password']
    
    #create an Entry object store all data for db action
    new_entry = Entry( email=email,
                      password=password
                           )
    #invoke the add entry function to add entry
    result = add_entry(new_entry)
    #return the result of the db action
    return jsonify({'id':result})


@app.route("/api/getuser/<id>", methods=['GET'])
def api_getuser(id):
    #retrieve the entry using id from client
    entry = get_entryuser(id)
    #Prepare a dictionary for json conversion
    data = {'id' : entry.id,
    'email' : entry.email,
    'password' : entry.password,
    }
    #Convert the data to json
    result = jsonify(data)
    return result #response back

@app.route("/api/deleteuser/<id>", methods=['GET'])
def api_deleteuser(id):
    entry = remove_entryuser(int(id))
    return jsonify({'result':'ok'})


