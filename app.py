from flask import Flask, redirect, render_template, request, session, flash  
from flask_session import Session  
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.security import generate_password_hash, check_password_hash  

app = Flask(__name__)  

# Configuration for session  
app.config["SESSION_PERMANENT"] = False  
app.config["SESSION_TYPE"] = "filesystem"  
Session(app)  

# Configuration for the database  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)  

# User model  
class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(80), unique=True, nullable=False)  
    password = db.Column(db.String(12), nullable=False)  

# Create the database tables  
with app.app_context():  
    db.create_all()  

@app.route('/')  
def index():  
    return render_template("index.html", name=session.get('name'))  

@app.route('/login', methods=["GET", "POST"])  
def login():  
    if request.method == "POST":  
        name = request.form.get("name")  
        password = request.form.get("password")  
        user = User.query.filter_by(name=name).first()  
        
        if user and check_password_hash(user.password, password):  
            session["name"] = name  
            return redirect('/')  
        else:  
            flash("Invalid username or password", "danger")  
    
    return render_template("login.html")  

@app.route('/register', methods=["GET", "POST"])  
def register():  
    if request.method == "POST":  
        name = request.form.get("name")  
        password = request.form.get("password")  
        hashed_password = generate_password_hash(password)  

        # Check if user already exists  
        existing_user = User.query.filter_by(name=name).first()  
        if existing_user:  
            flash("User already exists. Please log in.", "danger")  
            return redirect('/login')  

        new_user = User(name=name, password=hashed_password)  
        db.session.add(new_user)  
        db.session.commit()  
        flash("Registration successful! You can now log in.", "success")  
        return redirect('/login')  

    return render_template("register.html")  

@app.route('/logout')  
def logout():  
    session.pop("name", None)  
    return redirect('/')  
if __name__ == "__main__":  
    app.run(debug=True)