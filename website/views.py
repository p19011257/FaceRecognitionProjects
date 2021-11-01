from flask import Blueprint,render_template,request,flash
from website import mysql

views= Blueprint('views',__name__)

@views.route('/home', methods=['GET','POST'])
def home():
   if request.method == 'POST':
      name = request.form['form-name']
      email = request.form['form-email']
      mobile=request.form['form-mobile']
      message=request.form['form-message']
      cur = mysql.connection.cursor()
      cur.execute("INSERT INTO comments (name,email,mobile,message) VALUES(%s,%s,%s,%s)", (name,email,mobile,message))

      mysql.connection.commit()
      flash('Successful Inserted Comments', "info")
      return render_template("home.html")
   return render_template("home.html")
      #return render_template("home.html")
