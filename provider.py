from flask import *
from database import *
import uuid

provider=Blueprint('provider',__name__)

@provider.route('/provider_home')
def provider_home():
	
	return render_template('provider_home.html')

@provider.route('/provider_manage_place',methods=['get','post'])
def provider_manage_place():
	data={}
	q="select * from place_category"
	res=select(q)
	data['place_category']=res


	if 'place' in request.form:
		pcat=request.form['pcat']
		pname=request.form['pname']
		discription=request.form['discriptionxxxx']
		proimg=request.files['proimg']
		path='static/'+str(uuid.uuid4())+proimg.filename
		proimg.save(path)
		lati=request.form['lat']
		longi=request.form['lon']
		q="select * from `places` inner join place_category using(category_id) where place_name='%s' and category_name='%s'"%(pname,pname)
		res=select(q)
		if res:
			flash("Place already added!....")
		else:

			q="insert into `place_category` values(null,'%s')"%(pcat)
			res=insert(q)
			q="INSERT INTO `places` VALUES(NULL,'%s','%s','%s','%s','%s','%s')"%(res,pname,discription,path,lati,longi)
			ress=insert(q)

	if 'action' in request.args:
		action=request.args['action']
		place_id=request.args['place_id']
	else:
		action=None

	if action=='remove':
		q="DELETE FROM `places` WHERE `place_id`='%s'"%(place_id)
		delete(q)
	q="select * from places"
	res=select(q)
	data['view']=res
	return render_template('provider_manage_place.html',data=data)

@provider.route('/provider_manage_tour_package',methods=['get','post'])
def provider_manage_tour_package():
	data={}
	q="select * from places"
	res=select(q)
	data['place_namess']=res
	if 'submit' in request.form:
		pname=request.form['pname']
		place_id=request.form['place_id']
		amount=request.form['amount']
		days=request.form['days']
		nights=request.form['nights']
		adult=request.form['adult']
		child=request.form['child']
		desc=request.form['desi']
		# end=request.form['end']
		# start=request.form['start']
		q="INSERT INTO `packages` VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(session['pro_id'],pname,place_id,amount,days,nights,adult,child,desc)
		print(q)
		insert(q)
	if 'action' in request.args:
		action=request.args['action']
		pac_id=request.args['pac_id']
	else:
		action=None

	if action=='remove':
		q="DELETE FROM `packages` WHERE `package_id`='%s'"%(pac_id)
		delete(q)
	q="select * from packages"
	data['view']=select(q)
	return render_template('provider_manage_tour_package.html',data=data)


@provider.route('/provider_view_booking',methods=['get','post'])
def provider_view_booking():
	data={}
	# q="SELECT * FROM `packages` INNER JOIN `booking` USING(`package_id`) INNER JOIN `customer` USING(`customer_id`) WHERE login_id='%s'"%(session['pro_id'])
	q="SELECT * FROM `packages` INNER JOIN `booking` USING(`package_id`) INNER JOIN `customer` USING(`customer_id`)"
	print(q)
	res=select(q)
	data['view']=res
	
	if 'action' in request.args:
		action=request.args['action']
		b_id=request.args['b_id']

	else:
		action=None

	if action=='accept':
		q="UPDATE `booking` SET `booking_status`='confirmed' WHERE `booking_id`='%s'"%(b_id)
		update(q)
		flash ("booking confirmed")
		return redirect(url_for('provider.provider_view_booking'))
	return render_template('provider_view_booking.html',data=data)

@provider.route('/provider_view_enquiries',methods=['get','post'])
def provider_view_enquiries():
	data={}
	# q="SELECT * FROM `enquiry` INNER JOIN `customer` USING(`customer_id`) where login_id='%s'"%(session['pro_id'])
	q="SELECT * FROM `enquiry` INNER JOIN `customer` USING(`customer_id`)"
	print(q)
	res=select(q)
	data['view']=res
	j=0
	for i in range(1,len(res)+1):
		if 'submit' +str(i) in request.form:
			reply_details=request.form['reply_details'+str(i)]
			q="UPDATE `enquiry` SET `reply_details`='%s' WHERE `customer_id`='%s' "%(reply_details,res[j]['enquiry_id'])
			update(q)
			flash('success')
			return redirect(url_for('provider.provider_view_enquiries'))
		j=j+1
	
	return render_template('provider_view_enquiries.html',data=data)


@provider.route('/provider_view_recommendation',methods=['get','post'])
def provider_view_recommendation():
    data={}
    # q="SELECT * FROM `portal` INNER JOIN `customer` on portal.user_id=customer.customer_id inner join tour_provider using(provider_id)"
    q="SELECT * FROM `portal` INNER JOIN `customer` ON `customer`.`customer_id`=`portal`.`user_id`"
    res=select(q)
    data['view']=res

    if 'action' in request.args:
        action=request.args['action']
        log_id=request.args['log_id']
    else:
        action=None

    if action=='accept':
        q="UPDATE `portal` set `status`='accepted',provider_id='%s' WHERE `portal_id`='%s'"%(session['pro_id'],log_id)
        print(q)
        update(q)
        return redirect(url_for('provider.provider_view_recommendation'))

    if action=='reject':
        q="UPDATE `portal` set `status`='rejected' WHERE `portal_id`='%s'"%(log_id)
        print(q)
        update(q)
        return redirect(url_for('provider.provider_view_recommendation'))



    # 
    return render_template('provider_view_recommendation.html',data=data)

@provider.route('/provider_modify_portal',methods=['get','post'])
def provider_modify_portal():
	data={}
	q="select * from portal inner join customer on customer.customer_id=portal.user_id"
	res=select(q)
	data['up']=res
	if 'submit' in request.form:
		port_id=request.args['log_id']
		price=request.form['price']
		q="update portal set modified_price='%s' ,provider_id='%s',status='modify' where portal_id='%s'"%(price,session['pro_id'],port_id)
		print(q)
		update(q)
		return redirect(url_for('provider.provider_modify_portal'))
	return render_template('provider_modify_portal.html',data=data)

@provider.route('/pro_portal_booking',methods=['get','post'])
def pro_portal_booking():
	data={}
	id=request.args['id']
	# q="SELECT * FROM `packages` INNER JOIN `booking` USING(`package_id`) INNER JOIN `customer` USING(`customer_id`) WHERE login_id='%s'"%(session['pro_id'])
	q="SELECT * FROM `portal` INNER JOIN `booking` USING(`portal_id`) INNER JOIN `customer` USING(`customer_id`) where portal_id='%s'"
	print(q)
	res=select(q)
	data['view']=res
	
	if 'action' in request.args:
		action=request.args['action']
		b_id=request.args['b_id']
		
	else:
		action=None

	if action=='accept':
		q="UPDATE `booking` SET `booking_status`='confirmed' WHERE `booking_id`='%s'"%(b_id)
		update(q)
		flash ("booking confirmed")
		return redirect(url_for('provider.pro_portal_booking'))
	if action=='reject':
		q="UPDATE `booking` SET `booking_status`='rejected' WHERE `booking_id`='%s'"%(b_id)
		update(q)
		flash ("booking rejected")
		return redirect(url_for('provider.pro_portal_booking'))
	return render_template('pro_portal_booking.html',data=data)