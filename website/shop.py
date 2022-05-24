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


@shop.route("/checkout/<int:id>",methods=["GET","POST"])
def checkout(id):
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM products WHERE product_id=%s",(id,))
        product=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s",(session["user"],))
        user=cur.fetchone()

        if request.method=="POST":
            address=request.form.get("address")
            card=request.form.get("card")
            card_number=request.form.get("card_number")
            cvv=request.form.get("cvv")

            cur=db.connection.cursor()
            cur.execute("INSERT INTO orders(card,card_number,card_cvv,product,price,username,address,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(card,card_number,cvv,product[1],product[3],user[1],address,datetime.now()))
            db.connection.commit()
            flash("Your Order Taken.",category="success")
            return render_template("shop/thank_you.html")

        return render_template("shop/checkout.html",product=product)
    else:
        return redirect("/login")



@shop.route("/thank_you")
def thank_you():
    return render_template("/thank_you")

