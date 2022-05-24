from flask import Blueprint, redirect, render_template,request,session,flash,redirect
from website.__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime




admin=Blueprint('admin',__name__)
app=create_app()


@admin.route("/dashboard")
def dashboard():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users")
        users=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(sno) from users ")
        total_user=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT count(post_id) from posts ")
        total_posts=cur.fetchone()
        return render_template("admin/index.html",users=users,total_user=total_user,total_posts=total_posts)
    else:
        return redirect("/admin_login")



@admin.route("/admin_login",methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        email=request.form.get("email") 
        password=request.form.get("password")

        if email=="admin@gmail.com" and password=="12345":
            session["admin"]=email
            return redirect("/dashboard") 
        else:
            flash("wrong mail or password", category="error")
    return render_template("admin/login.html")



@admin.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/")


@admin.route("/all_user")
def all_user():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users")
        users=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(sno) from users ")
        total_user=cur.fetchone()
        return render_template("admin/user.html",total_user=total_user,users=users)

    else:
        return redirect("/admin_login")


@admin.route("/delete_user/<int:sno>")
def delete_user(sno):
    cur=db.connection.cursor()
    cur.execute("Delete FROM users where sno=%s",(sno,))
    db.connection.commit()
    return redirect("/dashboard")


@admin.route("/all_posts")
def all_posts():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM posts")
        posts=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(post_id) from posts ")
        total_post=cur.fetchone()
        return render_template("admin/posts.html",total_post=total_post,posts=posts)

    else:
        return redirect("/admin_login")


    
@admin.route("/delete_post/<int:sno>")
def delete_post(sno):
    cur=db.connection.cursor()
    cur.execute("Delete FROM posts where post_id=%s",(sno,))
    db.connection.commit()
    return redirect("/all_posts")




@admin.route("/all_expert")
def all_expert():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM experts")
        experts=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(expert_id) from experts ")
        total_experts=cur.fetchone()
        return render_template("admin/all_expert.html",experts=experts,total_experts=total_experts)

    else:
        return redirect("/admin_login")


@admin.route("/add_expert",methods=["GET","POST"])
def add_expert():
    if "admin" in session:
        if request.method=="POST":
            name=request.form.get("name")
            email=request.form.get("image")
            password=request.form.get("password")
            image=request.files["image"]
            details=request.form.get("details")
            if image.filename=="":
                flash("No file selected", category="error")
                return redirect(request.url)

            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
                cur=db.connection.cursor()
                cur.execute("INSERT INTO experts(username,password,image,details,date) VALUES(%s,%s,%s,%s,%s)",(name,password,image.filename,details,datetime.now(),))
                db.connection.commit()
                flash("Joined Expert Successfully",category="success")
                return redirect("/all_expert")

        return render_template("admin/add_expert.html")

    else:
        return redirect("/admin_login")


@admin.route("/all_product")
def all_product():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM products")
        products=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(product_id) from products")
        total_products=cur.fetchone()
        return render_template("admin/all_product.html",products=products,total_products=total_products)

    else:
        return redirect("/admin_login")




@admin.route("/add_product",methods=["GET","POST"])
def add_product():
    if "admin" in session:
        if request.method=="POST":
            name=request.form.get("name")
            description=request.form.get("description")
            price=request.form.get("price")
            image=request.files["image"]
            
            if image.filename=="":
                flash("No file selected", category="error")
                return redirect(request.url)

            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
                cur=db.connection.cursor()
                cur.execute("INSERT INTO products(name,image,price,description,date) VALUES(%s,%s,%s,%s,%s)",(name,image.filename,price,description,datetime.now(),))
                db.connection.commit()
                flash("product add",category="success")
                return redirect("/all_product")

        return render_template("admin/add_product.html")

    else:
        return redirect("/admin_login")



@admin.route("/delete_product/<int:sno>")
def delete_product(sno):
    cur=db.connection.cursor()
    cur.execute("Delete FROM products where product_id=%s",(sno,))
    db.connection.commit()
    return redirect("/all_product")
