from flask import Blueprint,session,render_template,redirect,request,url_for,flash
from app import db
from app.models import User

# Blueprint
# Small module of routes
auth_dp=Blueprint('auth',__name__)

@auth_dp.route("/register",methods=["GET","POST"])
def register():

    #Form submitted
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        #Check existing user
        existing_user=User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists","danger")
            return redirect(url_for('auth.register'))
        
        #Create new user
        new_user=User(username=username)

        #Hash password
        new_user.set_password(password)

        #Save in database
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful","Sucess")

        return redirect(url_for('auth.login'))
    
    return render_template("register.html")

@auth_dp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #Find user
        user=User.query.filter_by(username=username).first()

        #Check password
        if user and user.check_password(password):
            
            #Save login session
            session["user_id"]=user.id 
            session["username"]=user.username

            flash("Login successful", "success")

            return redirect(url_for('tasks.view_tasks'))

        flash("Invalid username or password", "danger")
        return redirect(url_for('auth.login'))

    return render_template("login.html")

@auth_dp.route('/logout')
def logout():
    #Remove session
    session.clear()
    # session.pop('user',None)
    flash("Logged out OUT",'info')
    return redirect(url_for('auth.login'))