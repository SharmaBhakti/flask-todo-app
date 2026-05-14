from app import db
from werkzeug.security import check_password_hash,generate_password_hash

#Coverth this Python Class into real database table

#User table
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    password_hash=db.Column(db.String(200),nullable=False)
    #One user-> many tasks
    tasks=db.relationship("Task",backref="owner",lazy=True)

    #Hash password
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    #Check password during login
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

#Task table
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    status=db.Column(db.String(20),default="Pending")
    #Foreign key
    #Connect task with user
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
