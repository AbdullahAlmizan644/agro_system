from math import prod
from flask import Blueprint, redirect, render_template,request,flash,session
from .__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta


shop=Blueprint('shop',__name__)
app=create_app()

@shop.route("/shop")
def shops():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM products")
    products=cur.fetchall()
    return render_template("shop/shop.html",products=products)


@shop.route("/product_details/<int:id>")
def product_details(id):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM products WHERE product_id=%s",(id,))
    product=cur.fetchone()
    return render_template("shop/product_details.html",product=product)



@shop.route("/thank_you")
def thank_you():
    return render_template("shop/thank_you.html")


@shop.route("/order_confirm/<int:id>",methods=["GET","POST"])
def order_confirm(id):
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM products WHERE product_id=%s",(id,))
        product=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s",(session["user"],))
        user=cur.fetchone()
        if request.method=="POST":
            address=request.form.get("address")
            payment=request.form.get("paymentMethod")
            total=request.form.get("total")

            cur=db.connection.cursor()
            cur.execute("INSERT INTO orders(product,price,username,address,date,payment,total) VALUES(%s,%s,%s,%s,%s,%s,%s)",(product[1],product[3],user[1],address,datetime.now(),payment,total,))
            db.connection.commit()
            flash("order complete",category="success")
            return redirect("/thank_you")

        return render_template("shop/checkout.html",product=product)
    
    else:
        return redirect("/login")