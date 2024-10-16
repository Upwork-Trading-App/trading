from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import re
from models import db, Users

app = Flask(__name__)
    
app.config['SECRET_KEY'] = 'eGRklsAtNW6FQ48egn9bExF3WFLH2P'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/trading'
  
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
   
bcrypt = Bcrypt(app)
db.init_app(app)
migrate = Migrate(app, db)  

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        fullname = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user_exists = Users.query.filter_by(email=email).first() is not None
        
        if user_exists:
            message = 'Email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not fullname or not username or not password or not email:
            message = 'Please fill out the form!'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = Users(full_name=fullname, email=email, username=username, password_hash=hashed_password, role='customer')
            db.session.add(new_user)
            db.session.commit()
            message = 'You have successfully registered!'
            return redirect(url_for('login'))  # Redirect to login after registration success

    return render_template('auth/register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == '' or password == '':
            message = 'Please enter email and password!'
        else:
            user = Users.query.filter_by(email=email).first()
            
            if user is None:
                message = 'Please enter correct email / password!'
            else:
                if not bcrypt.check_password_hash(user.password_hash, password):
                    message = 'Please enter correct email and password!'
                else:    
                    session['loggedin'] = True
                    session['userid'] = user.id
                    session['name'] = user.full_name
                    session['email'] = user.email
                    message = 'Logged in successfully!'
                    return redirect(url_for('dashboard'))

    return render_template('auth/login.html', message=message)

@app.route("/", methods =['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:        
        return render_template("dashboard.html")
    return redirect(url_for('login'))   
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


### USERS
@app.route('/users', methods=['GET'])
def list_users():
    if 'loggedin' in session:
        users = Users.query.all()
        return render_template('users/list.html', users=users)
    return redirect(url_for('login'))

@app.route('/users/view/<int:user_id>')
def view_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('users/view.html', user=user)

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.full_name = request.form['full_name']
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        
        new_password = request.form['password']
        if new_password:  
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password_hash = hashed_password  
        
        db.session.commit()
        
        return redirect(url_for('list_users'))
    
    return render_template('users/edit.html', user=user)

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

if __name__=='__main__':
    app.run(debug=True)