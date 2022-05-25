from flask import Blueprint, redirect, render_template,request,session,flash,redirect
from website.__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_mail import Mail,Message


expert=Blueprint('expert',__name__)
app=create_app()
mail=Mail()


@expert.route("/expert_login",methods=["GET","POST"])
def epert_login():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM experts where username=%s and password=%s",(name,password,))
        user=cur.fetchone()

        if user:
            session['expert']=name
            flash("Login successfully!", category="success")
            return redirect("/expert_dashboard")
        else:
            flash("Wrong username or password!", category="error")
    return render_template("expert/expert_login.html")




@expert.route("/expert_logout")
def expert_logout():
    session.pop("expert", None)
    return redirect("/expert_login")



@expert.route("/experts")
def experts():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM experts")
    all_expert=cur.fetchall()
    return render_template("expert/expert.html",all_expert=all_expert)


@expert.route("/write_problem/<int:id>", methods=["GET","POST"])
def write_problem(id):
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM experts where expert_id=%s",(id,))
        expert=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users where username=%s",(session["user"],))
        user=cur.fetchone()

        if request.method=="POST":
            problem=request.form.get("ckeditor")
            image=request.files["image"]

            print("hello")
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
            cur=db.connection.cursor()
            cur.execute("INSERT INTO expert_help(expert_id,expert_name,username,email,problem,problem_image,date) values(%s,%s,%s,%s,%s,%s,%s)",(id,expert[0],user[1],user[2],problem,image.filename,datetime.now(),))
            db.connection.commit()
            flash("problem upload successfully",category="success")
            return redirect("/")


        return render_template("expert/write_problem.html",expert=expert)
    else:
        return redirect("/login")



@expert.route("/expert_dashboard")
def expert_dashboard():
    if "expert" in session:
        print(session["expert"])
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM expert_help where expert_name=%s",(session["expert"],))
        info=cur.fetchall()
        print(info)
        return render_template("expert/expert_dashboard.html",info=info)
    else:
        return redirect("/expert_login")





@expert.route("/expert_answer/<int:id>",methods=["GET","POST"])
def expert_answer(id):
    if "expert" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM expert_help where sno=%s",(id,))
        data=cur.fetchone()

        if request.method=="POST":
            answer=request.form.get("answer")

            msg = Message("Expert answer",sender="ulachingmarma@gmail.com",recipients=[data[4]])
            msg.body=answer
            mail.send(msg)
            return "<script> alert('answer send successfully') </script>"
        return render_template("expert/expert_answer.html",data=data)
    else:
        return redirect("/expert_login")







