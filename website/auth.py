import MySQLdb
from flask import Blueprint, render_template, request,flash,redirect,session,url_for,Response
from website import mysql
from website import create_app
from flask_mail import Mail,Message
import os, bcrypt,uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.utils import secure_filename
from fpdf import FPDF
import csv
auth= Blueprint('auth', __name__)
#mail=Mail(auth)

#auth.config["MAIL_SERVER"] = "smtp.gmail.com"
#auth.config["MAIL_PORT"] = 465
#auth.config["MAIL_USERNAME"] = "yongyee373@gmail.com"
#auth.config["MAIL_PASSWORD"] = "8298767abc"
#auth.config["MAIL_USE_TLS"] = False
#auth.config["MAIL_USE_SSL"] = True


app=create_app()

ALLOWED_EXTENSIONS= {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/facilities')
def facilities():
   return render_template('facilities.html')

@auth .route('/classes')
def classes():
    return render_template("classes.html")

@auth.route('/about_us')
def about_us():
    return render_template("about_us.html")



@auth .route('/payment_detail1', methods=['GET','POST'])
def payment_detail1():
    if request.method == 'POST':
        email=request.form['email']
        package= request.form['package']
        price = request.form['price']
        name = request.form['cname']
        now = datetime.now()
        current_date=now.strftime('%Y-%m-%d')
        after_date = datetime.today()+ relativedelta(months=1)
        expired_date=after_date.strftime('%Y-%m-%d')
        second_date=datetime.today()+ relativedelta(months=2)
        second_expireddate=second_date.strftime('%Y-%m-%d')
        status="paid"
        print("Email:",email,"Package Name:",package,"Price: RM",price,"Name of member:",name,"Joined date:",current_date,"Expired Date:",expired_date)
        # upload file loop
        file = request.files['file']
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO members_joined (package,price,user,date,expired_date) VALUES(%s,%s,%s,%s,%s)",
                    (package,price,name,current_date,expired_date))
        cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                    (email,name,price,current_date,expired_date))
        cur.execute("UPDATE payment_status SET status=%s WHERE user=%s",[status,name])
        cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                    (email,name,price,expired_date,second_expireddate))
        mysql.connection.commit()
        flash('Member Checkout Successfully', "info")
        return render_template("membership.html")
    return render_template("payment_detail1.html")

@auth .route('/payment_detail2', methods=['GET','POST'])
def payment_detail2():
    if request.method == 'POST':
        email = request.form['email']
        package = request.form['package']
        price = request.form['price']
        name = request.form['cname']
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        after_date = datetime.today() + relativedelta(months=1)
        expired_date = after_date.strftime('%Y-%m-%d')
        second_date = datetime.today() + relativedelta(months=2)
        second_expireddate = second_date.strftime('%Y-%m-%d')
        status = "paid"
        file = request.files['file']
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO members_joined (package,price,user,date,expired_date) VALUES(%s,%s,%s,%s,%s)",
                    (package, price, name, current_date, expired_date))
        cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                    (email, name, price, current_date, expired_date))
        cur.execute("UPDATE payment_status SET status=%s WHERE user=%s", [status, name])
        cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                    (email, name, price, expired_date, second_expireddate))
        mysql.connection.commit()
        return render_template("membership.html")
    return render_template("payment_detail2.html")

@auth .route('/payment_detail3', methods=['GET','POST'])
def payment_detail3():
    if request.method == 'POST':
        email = request.form['email']
        package = request.form['package']
        price = request.form['price']
        name = request.form['cname']
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        after_date = datetime.today() + relativedelta(months=1)
        expired_date = after_date.strftime('%Y-%m-%d')
        second_date = datetime.today() + relativedelta(months=2)
        second_expireddate = second_date.strftime('%Y-%m-%d')
        status = "paid"
        file = request.files['file']
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO members_joined (package,price,user,date,expired_date) VALUES(%s,%s,%s,%s,%s)",
                    (package, price, name, current_date, expired_date))
        cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                    (email, name, price, current_date, expired_date))
        cur.execute("UPDATE payment_status SET status=%s WHERE user=%s", [status, name])
        cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                    (email, name, price, expired_date, second_expireddate))
        mysql.connection.commit()
        return render_template("membership.html")
    return render_template("payment_detail3.html")

@auth.route('/wallet_payment', methods=['GET','POST'])
def wallet_payment():
    if request.method == 'POST':
        email=session['email']
        package = request.form['package']
        price = request.form['price'] #price of package to insert into payment status
        wallet_price=int(price)#for the users wallet
        name = request.form['cname']
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        after_date = datetime.today() + relativedelta(months=1)
        expired_date = after_date.strftime('%Y-%m-%d')
        second_date = datetime.today() + relativedelta(months=2)
        second_expireddate = second_date.strftime('%Y-%m-%d')
        status = "paid"
        file = request.files['file']
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users where email=%s",(email,))
        data = cur.fetchall()
        for i in data:
            money=i[3]
        print(type(money))
        print("Before paying wallet: RM",money)
        print("Package Price: RM",price)
        if wallet_price>money:
            return render_template("topup.html")
        else:
            wallet_price=money-wallet_price
            print("After paying wallet: RM",wallet_price)
           # print(email)
            cur.execute("UPDATE users SET wallet=%s WHERE email=%s", [wallet_price, email])
            cur.execute("INSERT INTO members_joined (package,price,user,date,expired_date) VALUES(%s,%s,%s,%s,%s)",
                        (package, price, name, current_date, expired_date))
            cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                        (email, name, price, current_date, expired_date))
            cur.execute("UPDATE payment_status SET status=%s WHERE user=%s", [status, name])
            cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                        (email, name, price, expired_date, second_expireddate))

        mysql.connection.commit()
        return render_template("membership.html")
    return render_template("wallet_payment.html")

@auth.route('/wallet_payment2', methods=['GET','POST'])
def wallet_payment2():
    if request.method == 'POST':
        email=session['email']
        package = request.form['package']
        price = request.form['price'] #price of package to insert into payment status
        wallet_price=int(price)#for the users wallet
        name = request.form['cname']
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        after_date = datetime.today() + relativedelta(months=1)
        expired_date = after_date.strftime('%Y-%m-%d')
        second_date = datetime.today() + relativedelta(months=2)
        second_expireddate = second_date.strftime('%Y-%m-%d')
        status = "paid"
        file = request.files['file']
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users where email=%s",(email,))
        data = cur.fetchall()
        for i in data:
            money=i[3]
        print(type(money))
        print(money)
        print(price)
        if wallet_price>money:
            return render_template("topup.html")
        else:
            wallet_price=money-wallet_price
            print(wallet_price)
            print(email)
            cur.execute("UPDATE users SET wallet=%s WHERE email=%s", [wallet_price, email])
            cur.execute("INSERT INTO members_joined (package,price,user,date,expired_date) VALUES(%s,%s,%s,%s,%s)",
                        (package, price, name, current_date, expired_date))
            cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                        (email, name, price, current_date, expired_date))
            cur.execute("UPDATE payment_status SET status=%s WHERE user=%s", [status, name])
            cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                        (email, name, price, expired_date, second_expireddate))

        mysql.connection.commit()
        return render_template("membership.html")
    return render_template("wallet_payment2.html")

@auth.route('/wallet_payment3', methods=['GET','POST'])
def wallet_payment3():
    if request.method == 'POST':
        email=session['email']
        package = request.form['package']
        price = request.form['price'] #price of package to insert into payment status
        wallet_price=int(price)#for the users wallet
        name = request.form['cname']
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        after_date = datetime.today() + relativedelta(months=1)
        expired_date = after_date.strftime('%Y-%m-%d')
        second_date = datetime.today() + relativedelta(months=2)
        second_expireddate = second_date.strftime('%Y-%m-%d')
        status = "paid"
        file = request.files['file']
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users where email=%s",(email,))
        data = cur.fetchall()
        for i in data:
            money=i[3]
        print(type(money))
        print(money)
        print(price)
        if wallet_price>money:
            return render_template("topup.html")
        else:
            wallet_price=money-wallet_price
            print(wallet_price)
            print(email)
            cur.execute("UPDATE users SET wallet=%s WHERE email=%s", [wallet_price, email])
            cur.execute("INSERT INTO members_joined (package,price,user,date,expired_date) VALUES(%s,%s,%s,%s,%s)",
                        (package, price, name, current_date, expired_date))
            cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                        (email, name, price, current_date, expired_date))
            cur.execute("UPDATE payment_status SET status=%s WHERE user=%s", [status, name])
            cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                        (email, name, price, expired_date, second_expireddate))

        mysql.connection.commit()
        return render_template("membership.html")
    return render_template("wallet_payment3.html")

@auth.route('/member_payment')
def member_payment():
    if 'email' in session:
        email=session['email']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM payment_status WHERE status='pending' AND email=%s",(email,))
        data=cur.fetchall()
        cur.close()

        return render_template("member_payment.html",paymentData=data)
    return render_template("member_payment.html")

@auth.route('/member_monthlypayment', methods=['GET','POST'])
def member_monthlypayment():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['cname']
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        after_date = datetime.today() + relativedelta(months=2)
        start_date = after_date.strftime('%Y-%m-%d')
        second_date = datetime.today() + relativedelta(months=3)
        finish_expireddate = second_date.strftime('%Y-%m-%d')
        status = "paid"
        cur = mysql.connection.cursor()
        cur.execute("UPDATE payment_status SET status=%s WHERE user=%s AND status='pending'", [status, name])
        amountresult = cur.execute("SELECT amount,max(date_expired) FROM payment_status where user=%s ", (name,))
        if amountresult > 0:
            data = cur.fetchall()
            for i in data:
                price = i[0]
                lastexpired_date=i[1]
                print(price)
                print(lastexpired_date)
            latest_date=datetime.strptime(lastexpired_date,'%Y-%m-%d')
            latest_date=latest_date+relativedelta(months=1)
            latest_date=latest_date.strftime('%Y-%m-%d')
            print(latest_date)

           # print(latest_date)

            print(type(price))

        cur.execute("INSERT INTO payment_status (email,user,amount,date_started,date_expired) VALUES(%s,%s,%s,%s,%s)",
                    (email, name, price, lastexpired_date, latest_date))
        mysql.connection.commit()
        return render_template("home.html")
    return render_template("member_monthlypayment.html")



@auth.route('/membership')
def membership():
    return render_template("membership.html")





@auth.route('/realtime')
def realtime():
    with open('website/Attendance.csv') as csvfile:
        reader = csv.reader(x.replace('\0', '') for x in csvfile)
        count = 0
        newList = []

        for row in reader:
            count = count + 1
            #print(row)
            newList.append(row)
        userDetails = len(newList)
        print("Total Members:",userDetails)
        return render_template("realtime.html", userDetails=userDetails)


@auth.route('/topup' , methods=['GET','POST'])
def topup():
    if request.method=="POST":
        email=request.form['email']
        strwallet=request.form['amount']
        password = request.form['password'].encode('utf-8')
        wallet=int(strwallet)
        print(type(wallet))
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        try:
            if len(user) > 0:
                if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                    cur = mysql.connection.cursor()
                    result = cur.execute("SELECT * from users WHERE email=%s", [email])
                    if result > 0:
                        data = cur.fetchall()
                        for i in data:
                            amount = i[3]
                        print("Before top up RM:",amount)
                        print("top up amount: RM", wallet)
                        if wallet >0:
                            wallet = wallet + amount
                            print("After top up RM:", wallet)
                            cur = mysql.connection.cursor()
                            cur.execute("UPDATE users SET wallet=%s  WHERE email=%s", [wallet, email])
                            mysql.connection.commit()
                            cur.close()
                            flash('Top Up Successfully', "info")
                            return render_template("home.html")
                        else:
                            flash('Amount need to be more than RM0', "info")
                            return render_template("topup.html")
                flash('Invalid password', "info")
                return render_template("topup.html")
        except ValueError:
            return redirect(url_for('auth.topup'))
    else:
        return render_template("topup.html")


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password'].encode('utf-8')

        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user=cur.fetchone()
        cur.close()
        try:
            if len(user) > 0:
                if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                    session['name'] = user['name']
                    session['email'] = user['email']
                    session['phone'] = user['phone']
                    session['wallet']=user['wallet']
                    flash('Successful Login', "info")
                    return render_template("home.html")
                else:
                    flash('Invalid Password',"info")
                    return redirect(url_for('auth.login'))
        except TypeError:
            flash('Please enter information', "info")
            return redirect(url_for('auth.login'))
    else:
        if "name" in session:
            return render_template("home.html")
        return render_template("login.html")

@auth.route('/forgot',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['email']
        token=str(uuid.uuid4())
        cur=mysql.connection.cursor()
        result=cur.execute("SELECT * from users WHERE email=%s",[email])
        if result>0:
            data= cur.fetchone()
            #msg=Message(subject="Forgot password request",sender="smtp.gmail.com",recipients=[email])
            #msg.body=render_template("sent.html",token=token,data=data)
            #mail.send(msg)
            cur=mysql.connection.cursor()
            cur.execute("UPDATE users SET token=%s WHERE email=%s",[token,email])
            mysql.connection.commit()
            cur.close()
            flash("Email Sent to Email","success")
            return render_template("home.html")
        else:
            flash("Error")
    return render_template("forgot.html")

@auth.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    if request.method=="POST":
        password=request.form["password"].encode('utf-8')
        confirm_password = request.form["confirm_password"].encode('utf-8')
        token1 = str(uuid.uuid4())
        if password !=confirm_password:
            flash("Password not match","danger")
            return redirect("reset")
        password=bcrypt.hashpw(password, bcrypt.gensalt())
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE token=%s",[token])
        user=cur.fetchone()
        if user:
            cur=mysql.connection.cursor()
            cur.execute("UPDATE users SET token=%s,password=%s WHERE token=%s",[token1,password,token])
            mysql.connection.commit()
            cur.close()
            flash("Password updated","success")
            return render_template("home.html")
        else:
            flash("Invalid","danger")
            return render_template("reset.html")

    return render_template("reset.html")

@auth.route('/logout')
def logout():
   session.clear()
   flash('Successful Logout', "info")
   return render_template("home.html")

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email=request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        password1 = request.form['password1'].encode('utf-8')
        password2=request.form['password2'].encode('utf-8')
        hash_password=bcrypt.hashpw(password1, bcrypt.gensalt())
        hash_password2 = bcrypt.hashpw(password2, bcrypt.gensalt())
        email_check=[]
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * from users")
        if result > 0:
            data = cur.fetchall()
            for i in data:
                amount = i[1]
                email_check.append(amount)
            print(email_check)
        #database inserting
        if email not in email_check:
            if password1==password2:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (email,name,phone,password) VALUES(%s,%s,%s,%s)",
                            (email, name, phone, hash_password))
                mysql.connection.commit()
                session['name'] = name
                session['email'] = email
                session['phone'] = phone
                flash('Successful Sign Up', "info")
                return redirect(url_for("views.home"))
                cur.close()
                return "Success"
            else:
                flash('Password Not Matched', "info")
                return render_template("sign_up.html")
        else:
            flash('Email already existed', "info")
            return render_template("sign_up.html")


    return render_template("sign_up.html")

@auth.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']
        cur = mysql.connection.cursor()
        amountresult = cur.execute("SELECT * FROM users where email=%s", (email,))
        if amountresult > 0:
            data = cur.fetchall()
            return render_template("profile.html", amount=data)
    return render_template("profile.html")

#--> Start below is the admin side website

@auth.route('/admin_home')
def admin_home():
    with open('website/Attendance.csv') as csvfile:
        reader = csv.reader(x.replace('\0', '') for x in csvfile)
        count = 0
        newList = []

        for row in reader:
            count = count + 1
            #print(row)
            newList.append(row)
        userDetails = len(newList)
        print("Total Members:",userDetails)
        return render_template("admin_home.html", userDetails=userDetails)



@auth.route('/admin_dashboard')
def admin_dashboard():
    cur = mysql.connection.cursor()
    valueResult = cur.execute("SELECT COUNT(user), SUM(PRICE) FROM members_joined ORDER BY user")
    if valueResult > 0:
        userDetails = cur.fetchall()
        return render_template("admin_dashboard.html", userDetails=userDetails)

@auth.route('/admin_comments')
def admin_comments():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM comments")
    data=cur.fetchall()
    cur.close()

    return render_template("admin_comments.html",comments=data)

@auth.route('/admin_payment')
def admin_payment():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM payment_status")
    data=cur.fetchall()
    cur.close()

    return render_template("admin_payment.html",paymentData=data)

@auth.route('/admin_viewmembers')
def admin_viewmembers():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM members_joined")
    data=cur.fetchall()
    cur.close()

    return render_template("admin_viewmembers.html",memberData=data)

@auth.route('/download/report/pdf')
def download_report():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM comments")
    result = cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 8 * pdf.l_margin
    pdf.set_font('Times', 'B', 5.0)
    pdf.cell(page_width, 0.0, 'Comments Data', align='C')
    pdf.ln(10)
    pdf.set_font('Courier', '', 5)
    col_width = page_width/3
    pdf.ln(1)
    th = pdf.font_size
    for row in result:
        pdf.cell(col_width, th, str(row[0]), border=1)
        pdf.cell(col_width, th, row[1], border=1)
        pdf.cell(col_width, th, row[3], border=1)
        pdf.cell(col_width, th, row[4], border=1)
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times', '', 10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=comments_report.pdf'})

@auth.route('/download/payment/pdf')
def download_payment():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM payment_status")
    result = cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 8 * pdf.l_margin
    pdf.set_font('Times', 'B', 5.0)
    pdf.cell(page_width, 0.0, 'Payment Data', align='C')
    pdf.ln(10)
    pdf.set_font('Courier', '', 5)
    col_width = page_width/3
    pdf.ln(1)
    th = pdf.font_size
    for row in result:
        pdf.cell(col_width, th, str(row[0]), border=1)
        pdf.cell(col_width, th, row[1], border=1)
        pdf.cell(col_width, th, row[2], border=1)
        pdf.cell(col_width, th, str(row[3]), border=1)
        pdf.cell(col_width, th, row[4], border=1)
        pdf.cell(col_width, th, row[5], border=1)
        pdf.cell(col_width, th, row[6], border=1)
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times', '', 10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=payment_report.pdf'})

@auth.route('/download/members/pdf')
def download_members():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM members_joined")
    result = cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 8 * pdf.l_margin
    pdf.set_font('Times', 'B', 5.0)
    pdf.cell(page_width, 0.0, 'Members Data', align='C')
    pdf.ln(10)
    pdf.set_font('Courier', '', 5)
    col_width = page_width/3
    pdf.ln(1)
    th = pdf.font_size
    for row in result:
        pdf.cell(col_width, th, row[0], border=1)
        pdf.cell(col_width, th, row[1], border=1)
        pdf.cell(col_width, th, str(row[2]), border=1)
        pdf.cell(col_width, th, str(row[3]), border=1)
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times', '', 10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=members_report.pdf'})


@auth.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method=="POST":
        name=request.form['name']
        password=request.form['password'].encode('utf-8')

        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM admin WHERE name=%s",(name,))
        user=cur.fetchone()
        cur.close()
        try:
            if len(user) > 0:
                if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                    session['name'] = user['name']
                    flash('Successful Login', "info")
                    return redirect(url_for('auth.admin_home'))
                else:
                    flash('Password not matched', "info")
                    return render_template("admin_login.html")
            else:
                flash('Please fill in information', "info")
                return render_template("admin_login.html")
        except TypeError:
            flash('Please enter information', "info")
            return redirect(url_for('auth.admin_login'))


    else:
        if "name" in session:
            return render_template("admin_home.html")
        return render_template("admin_login.html")

@auth.route('/admin_logout')
def admin_logout():
   session.clear()
   flash('Successful Logout', "info")
   return render_template("admin_login.html")