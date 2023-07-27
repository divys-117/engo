from flask import *
from database import *

user=Blueprint('user',__name__)

@user.route('/user_home')
def user_home():
    
    return render_template('user_home.html')
@user.route('/user_view_packages',methods=['get','post'])
def user_view_packages():
    data={}
    if 'submit' in request.form:
        search=request.form['search']+'%'
        q="SELECT *,packages.description as Name  FROM `packages` INNER JOIN `places` ON `places`.`place_id`=`packages`.`places` INNER JOIN `place_category` ON `place_category`.`category_id`=`places`.`category_id` inner join tour_provider using(provider_id)  where package_name LIKE '%s' or place_name like '%s'"%(search,search)
        data['view']=select(q)
    else:
        q="SELECT *,packages.description as Name FROM `packages` INNER JOIN `places` ON `places`.`place_id`=`packages`.`places` INNER JOIN `place_category` ON `place_category`.`category_id`=`places`.`category_id` inner join tour_provider using(provider_id)"
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx___________________",q)
        res=select(q)
        data['view']=res
    return render_template('user_view_packages.html',data=data)



# @user.route('/user_book_package',methods=['get','post'])
# def user_book_package():
#     data={}
#     if 'submit' in request.form:
#         cat=request.form['cat']
#         q="INSERT INTO `place_category` VALUES(NULL,'%s')"%(cat)
#         insert(q)
#     if 'action' in request.args:
#         action=request.args['action']
#         cat_id=request.args['cat_id']
#     else:
#         action=None
#     if action=="delete":
#         q="DELETE FROM `place_category` WHERE `category_id`='%s'"%(cat_id)
#         delete(q)
#         return redirect(url_for('user.user_book_package'))

#     if action=='update':
#         q="SELECT * FROM `place_category` WHERE `category_id`='%s'"%(cat_id)
#         data['up']=select(q)

#     if 'update' in request.form:
#         cat=request.form['cat']

#         q="UPDATE `place_category` SET `category_name`='%s' WHERE `category_id`='%s'"%(cat,cat_id)
#         update(q)
#         return redirect(url_for('user.user_book_package'))
 
#     return render_template('user_book_packages.html',data=data)

@user.route('/user_send_complaints',methods=['get','post'])
def user_send_complaints():
	data={}
	q="SELECT * FROM `complaint`"
	res=select(q)
	data['view']=res
	if 'submit' in request.form:
		com=request.form['com']
		q="INSERT INTO `complaint` VALUES(NULL,'%s','%s','pending',curdate())"%(session['cus_id'],com)
		insert(q)
		return redirect(url_for('user.user_send_complaints'))
	return render_template('user_send_complaints.html',data=data)


@user.route('/user_view_users',methods=['get','post'])
def user_view_users():
    data={}
    # q="SELECT * FROM `customer` where customer_id!='%s'"%(session['cus_id'])
    # res=select(q)
    # data['view']=res




    if "action" in request.args:
        action=request.args['action']
        lid=request.args['lid']



    else:
        action=None

    if action=="request":
        q="insert into chat_request values(NULL,'requested','%s','%s')"%(session['log_id'],lid)
        insert(q)
        return redirect(url_for("user.user_view_users"))

    if 'submit' in request.form:
        search=request.form['search']+'%'
        q="SELECT * FROM `customer` WHERE `first_name` LIKE '%s' OR `place` LIKE '%s' "%(search,search)
        data['view']=select(q)
    else:
        q="SELECT * FROM `customer`where customer_id<>'%s'"%(session['cus_id'])
        print(q)
        data['view']=select(q)

    return render_template('user_view_users.html',data=data)

@user.route('/user_view_chat_request',methods=['get','post'])
def user_view_chat_request():
    data={}
    lid=session['log_id']
    # q="SELECT * FROM `customer` inner join chat_request on customer.login_id=chat_request.receveir_id where customer_id!=(select customer_id from customer where login_id='%s') GROUP BY receveir_id"%(session['log_id'] )
    
    q="""SELECT * FROM chat_request inner join `customer` on customer.login_id=chat_request.`sender_id` where sender_id!='%s'  and receveir_id='%s'
        UNION
        SELECT * FROM chat_request inner join `customer` on customer.login_id=chat_request.`receveir_id` where receveir_id!='%s' and sender_id='%s'
    """ %(lid,lid,lid,lid) 
      # WHERE receveir_id='%s'"%(session['log_id'])
    print("---------------------------",q)
    res=select(q)
    data['view']=res

    if "action" in request.args:
        action=request.args['action']
        lid=request.args['lid']
        cid=request.args['cid']
    else:
        action=None
    if action=="accept":
        q="update chat_request set chat_request_status='accepted' where chat_request_id='%s'"%(cid)
        update(q)
        return redirect(url_for("user.user_view_chat_request"))
    if action=="reject":
        q="update chat_request set chat_request_status='rejected' where chat_request_id='%s'"%(cid)
        update(q)
        return redirect(url_for("user.user_view_chat_request"))
    if action=="block":
        q="update chat_request set chat_request_status='blocked' where chat_request_id='%s'"%(cid)
        update(q)
        return redirect(url_for("user.user_view_chat_request"))

    return render_template('user_view_chat_request.html',data=data)

@user.route('/user_chat_user',methods=['get','post'])
def user_chat_user():
    data={}
    uid=session['log_id']
    data['uid']=uid
    cid=request.args['cid']

    did=request.args['lid']
    if 'btn' in request.form:
        name=request.form['txt']
        
    
        q="insert into chat values(NULL,'%s','%s',(SELECT IF(sender_id='%s',`receveir_id`,sender_id) FROM chat_request WHERE chat_request_id='%s'),'%s',now(),'chat')"%(cid,uid,uid,cid,name)
        print(q)
        insert(q)
        # q="update chat set message='%s',date=curdate(),status='accepted' where sender_id='%s'"%(name,uid)
        # update(q)
        return redirect(url_for("user.user_chat_user",lid=did,cid=cid))
    q="SELECT * FROM chat WHERE (sender_ids='%s' AND receiver_ids=(SELECT IF(sender_id='%s',`receveir_id`,sender_id) FROM chat_request WHERE chat_request_id='%s') and chat_request_id='%s') OR (sender_ids=(SELECT IF(sender_id='%s',`receveir_id`,sender_id) FROM chat_request WHERE chat_request_id='%s') AND receiver_ids='%s' and chat_request_id='%s')"%(uid,uid,cid,cid,uid,cid,uid,cid)
    print(q)
    # q="select * from chats where senderid='%s' and receiverid=( select login_id from doctors where doctor_id='%s' )"%(uid,did)
    print(q)
    res=select(q)
    data['ress']=res

    return render_template('user_chat_user.html',data=data,uid=uid)





@user.route('/user_book_packages',methods=['get','post'])
def user_book_packages():
    data={}
    amt=request.args['amt']
    data['amt']=amt
    cid=request.args['cid']
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",cid)

    if 'submit' in request.form:
        # amt=request.form['amt']
        qty=request.form['qty']
        date=request.form['tdate']
        tamt=request.form['tamt']
        # q="select * from booking inner join package using(package_id) where package_name='%s'"%()
        q="INSERT INTO `booking` VALUES(NULL,'%s','0','%s','%s',curdate(),'%s','%s','booked')"%(cid,session['cus_id'],qty,date,tamt)
        print("cccccccccccccccccccccccccccccccc",q)
        insert(q)
        return redirect(url_for('user.user_book_packages',amt=amt,cid=cid))
    return render_template('user_book_packages.html',data=data)

@user.route('/user_payment',methods=['get','post'])
def user_payment():
    data={}
    amt=request.args['amt']
    data['amt']=amt
    cid=request.args['cid']
    if 'submit' in request.form:
        amt=request.form['amt']
        # qty=request.form['qty']
        # date=request.form['tdate']
        # tamt=request.form['tamt']
        q="INSERT INTO `payment` VALUES(NULL,'%s','%s','cardpayment',now())"%(cid,amt)
        res=insert(q)
        if res:
            flash("Payment Successfull!...")
        else:
            flash("Payment Failed!...Try again")

        return redirect(url_for('user.user_payment',amt=amt,cid=cid))
    return render_template('user_payment.html',data=data)

@user.route('/user_view_bookings',methods=['get','post'])
def user_view_bookings():
    data={}
    # q="SELECT * FROM `packages` INNER JOIN `booking` USING(`package_id`) INNER JOIN `customer` USING(`customer_id`) WHERE login_id='%s'"%(session['pro_id'])
    q="SELECT * FROM `packages` INNER JOIN `booking` USING(`package_id`) inner join tour_provider using(provider_id) where customer_id='%s'"%(session['cus_id'])
    print(q)
    res=select(q)
    data['view']=res
    return render_template('user_view_bookings.html',data=data)


# @user.route('/user_create_package',methods=['get','post'])
# def user_create_package():
#     data={}
#     q="select * from places"
#     res=select(q)
#     data['place_name']=res
#     if 'submit' in request.form:
#         pname=request.form['place_id']
#         des=request.form['des']
#         nop=request.form['nop']
#         mode=request.form['mode']
#         price=request.form['price']
       
#         q="INSERT INTO `recommendations` VALUES (NULL,'%s','%s','%s','%s','%s','%s','pending')"%(session['cus_id'],pname,des,nop,mode,price)
#         print(q)
#         insert(q)
   
#     q="select * from recommendations inner join places using(place_id)"
#     data['view']=select(q)
#     return render_template('user_create_package.html',data=data)


@user.route('/user_add_portal',methods=['get','post'])
def user_add_portal():
    data={}
    # id=request.args['id']
    q="SELECT * FROM `portal` INNER JOIN `tour_provider` ON `tour_provider`.`provider_id`=`portal`.`provider_id`"
    data['user']=select(q)
    
    if 'submit' in request.form:
        
        place=request.form['place']
        desi=request.form['desi']
        people=request.form['people']
        travel=request.form['travel']
        price=request.form['price']
        days=request.form['days']
        q="INSERT INTO `portal` VALUES(NULL,'%s','0','%s','%s','%s','%s','%s','pending','0','%s')"%(session['cus_id'],place,desi,people,travel,price,days)
        insert(q)
        return redirect(url_for('user.user_add_portal',id=id))
    if 'action' in request.args:
        action=request.args['action']
        log_id=request.args['log_id']
    else:
        action=None

    if action=='accept':
        q="UPDATE `portal` set `status`='accepted' WHERE `portal_id`='%s'"%(log_id)
        print(q)
        update(q)
        return redirect(url_for('user.user_add_portal'))

    if action=='reject':
        q="UPDATE `portal` set `status`='pending',modified_price='0' WHERE `portal_id`='%s'"%(log_id)
        print(q)
        update(q)
        return redirect(url_for('user.user_add_portal'))


    return render_template('user_add_portal.html',data=data)

@user.route('/user_view_tour_provider',methods=['get','post'])
def user_view_tour_provider():
    data={}
    q="SELECT * FROM `login` INNER JOIN `tour_provider` USING(`login_id`)"
    res=select(q)
    data['view']=res
    return render_template('user_view_providers.html',data=data)


@user.route('/user_add_enq',methods=['get','post'])
def user_add_enq():
    data={}
    id=request.args['id']
    q="select * from enquiry where provider_id='%s'"%(id)
    data['user']=select(q)
    
    if 'submit' in request.form:
        
        enq=request.form['enq']
        q="INSERT INTO `enquiry` VALUES(NULL,'%s','%s','%s','pending',now())"%(session['cus_id'],id,enq)
        insert(q)
        return redirect(url_for('user.user_add_enq',id=id))
        
    return render_template('user_add_enq.html',data=data)


@user.route('/user_add_rating',methods=['get','post'])
def user_add_rating():

    
    if "submit" in request.form:
        cid=request.args['cid']
        r=request.form['r']
        review=request.form['review']
        q="insert into review_ratings values(null,'%s','%s','%s','%s',now())"%(cid,session['cus_id'],r,review)
        insert(q)
        return redirect(url_for("user.user_add_rating",cid=cid))
    
    return render_template('user_add_rating.html')

@user.route('/user_view_rating',methods=['get','post'])
def user_view_rating():
    data={}
    # cid=request.args['cid']
    cid=request.args['cid']
    data['cid']=cid
    print(data['cid'])
    q="SELECT * FROM `review_ratings` INNER JOIN `customer` on review_ratings.customer=customer.customer_id inner join packages using(package_id) where package_id='%s'and customer_id<>'%s'"%(cid,session['cus_id'])
    res=select(q)
    data['view']=res

    if "action" in request.args:
        action=request.args['action']
        lid=request.args['lid']
        cid=request.args['cid']
    else:
        action=None

    if action=="request":
        q="insert into chat_request values(NULL,'requested','%s','%s')"%(session['log_id'],lid)
        insert(q)
        return redirect(url_for("user.user_view_rating",cid=cid))
        
    return render_template('user_view_rating.html',data=data)


