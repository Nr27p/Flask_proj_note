from flask import Flask, Blueprint , render_template , request , flash , redirect , url_for
from .modals import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def Login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully",category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again",category='error')
        else:
            flash("Email does not exist",category='error')
    return render_template("login.html",user=current_user )

@auth.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('auth.Login'))

@auth.route('/sign-up',methods=['GET','POST'])
def SignUp():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstname')
        password=request.form.get('password1')
        confirmPassword=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists",category='error')
        elif len(email)<4:
            flash("Email must be greater than 3 characters",category='error')
        elif len(firstName)<2:
            flash("First name must be greater than 1 character",category='error')
        elif password!=confirmPassword:
            flash("Passwords don't match",category='error')
        else:
            new_user=User(email=email,first_name=firstName,password=generate_password_hash(password,method='pbkdf2:sha256'))   
            db.session.add(new_user)
            db.session.commit()

            flash("Account created",category='success')
            return redirect(url_for('views.home'))

        
    return render_template("signup.html",user=current_user)