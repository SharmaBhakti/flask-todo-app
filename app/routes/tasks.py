from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from app import db
from app.models import Task
from sqlalchemy import text

# Blueprint for task routes
task_dp=Blueprint('tasks',__name__)

@task_dp.route('/')
def view_tasks():
    if "user_id" not in session:
        return redirect(url_for('auth.login'))
    
    # Shows only user tasks
    tasks=Task.query.filter_by(user_id=session["user_id"]).all()
    # tasks=Task.query.all()
    return render_template('task.html',tasks=tasks)

@task_dp.route('/add',methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for('auth.login'))
    
    title=request.form.get('title')
    if title:
        #Create task
        new_task=Task(title=title,status='Pending',user_id=session["user_id"])

        #Save in DB
        db.session.add(new_task)
        db.session.commit()
        flash('Task Added','success')

    return redirect(url_for('tasks.view_tasks'))

@task_dp.route("/toggle/<int:task_id>",methods=["POST"])
def toggle_status(task_id):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )
    # task=Task.query.get(task_id)
    task=Task.query.filter_by(id=task_id,user_id=session["user_id"]).first()

    if task:
        if task.status=='Pending':
            task.status='Working'
        elif task.status =='Working':
            task.status='Done'
        else:
            task.status="Pending"
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@task_dp.route("/clear",methods=["POST"])
def clear_tasks():
    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    Task.query.filter_by(
        user_id=session["user_id"]
    ).delete()

    db.session.commit()

    flash("All tasks cleared", "info")

    return redirect(url_for("tasks.view_tasks"))