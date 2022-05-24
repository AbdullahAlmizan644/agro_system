import re
from flask import Blueprint, redirect, render_template,request,flash,session
from datetime import datetime
from website.__init__ import db,create_app


expert=Blueprint('expert',__name__)
app=create_app()


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



@expert.route("/expert_dashboard")
def expert_dashboard():
    if "expert" in session:
        return render_template("expert/expert_dashboard.html")
    else:
        return redirect("/expert_login")



@expert.route("/expert_answer")
def expert_answer():
    return render_template("expert/expert_answer.html")