from flask import *
from database import *
import random
import string

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

public=Blueprint('public',__name__)

@public.route('/')
def home():
    
    return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
    if 'submit' in request.form:
        username=request.form['username']
        password=request.form['password']
        q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'"%(username,password)
        res=select(q)
        if res:
            user=res[0]['user_type']
            session['log_id']=res[0]['login_id']
            if user=='admin':

                return redirect(url_for('admin.admin_home'))
            if user=='provider':
                q="SELECT `provider_id` FROM `tour_provider` WHERE `login_id`='%s'"%(session['log_id'])
                res=select(q)
                if res:
                    session['pro_id']=res[0]['provider_id']
                return redirect(url_for('provider.provider_home'))
                flash('login success')
            if user=='customer':
                q="SELECT `customer_id` FROM `customer` WHERE `login_id`='%s'"%(session['log_id'])
                res=select(q)
                if res:
                    session['cus_id']=res[0]['customer_id']
                return redirect(url_for('user.user_home'))
                flash('login success')
        else:
            flash('ivalid username or password')
    return render_template("login.html")
@public.route('/provider_registration',methods=['get','post'])
def provider_registration():
    data={}
    if 'submit' in request.form:
        proname=request.form['proname']
        place=request.form['place']
        district=request.form['district']
        pincode=request.form['pincode']
        phone=request.form['phone']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']

        q="INSERT INTO `login` VALUES(NULL,'%s','%s','pending')"%(username,password)
        res=insert(q)
        q="INSERT INTO `tour_provider` VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s')"%(proname,place,district,pincode,phone,email,res)
        insert(q)
    
    return render_template('provider_registration.html',data=data)

@public.route('/userregistration',methods=['get','post'])
def userregistration():
    data={}
    if 'submit' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        hname=request.form['hname']
        place=request.form['place']
        dis=request.form['district']
        coun=request.form['coun']
        pin=request.form['pincode']
        phn=request.form['phone']
        email=request.form['email']
        # pnum=request.form['pnum']
        gen=request.form['gen']
        dob=request.form['dob']
        # lat=request.form['lat']
        # lon=request.form['lon']
        username=request.form['username']
        password=request.form['password']

        q="INSERT INTO `login` VALUES(NULL,'%s','%s','customer')"%(username,password)
        res=insert(q)
        q="INSERT INTO `customer` VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','0','%s','%s','%s','','')"%(fname,lname,hname,place,dis,coun,pin,phn,email,gen,dob,res)
        insert(q)
    
    return render_template('userregistration.html',data=data)

@public.route('/Forgot_password',methods=['get','post'])
def Forgot_password():

    if 'submit' in request.form:
        uname=request.form['uname']
        email=request.form['email']
        q="SELECT * FROM  `login` INNER JOIN `customer` USING(`login_id`) where username='%s' and email='%s'"%(uname,email)
        res=select(q)
        if res:
            username=res[0]['username']
            return redirect(url_for('public.confirmpassword',unames=username))
        else:
            flash('verification faild incorrect username or email')

    return render_template('Forgot_password.html')

@public.route('/confirmpassword',methods=['get','post'])
def confirmpassword():
    if 'submit' in request.form:
        unames = request.args['unames']
        password = request.form['password']
        c_password = request.form['c_password']
        if password==c_password:
            q="UPDATE `login` SET `password`='%s' WHERE `username`='%s'"%(c_password,unames)
            print(q)
            update(q)
            return redirect(url_for('public.home'))
        else:
            flash('check your confirmpassword')
    
    return render_template('confirm_password.html')
