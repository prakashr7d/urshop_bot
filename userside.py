import mysql.connector
from fuzzywuzzy import process
import urllib.request, json
import datetime
# import config
# import datetime


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="urshop"
)

cursor = mydb.cursor()


# deafult values

# table already created
# mycursor.execute("CREATE TABLE user(userid integer PRIMARY KEY,name text,pincode integer,mob integer,address text)")
# def swapPositions(list, pos1, pos2): 
#     first_ele = list.pop(pos1-1)    
#     second_ele = list.pop(pos2-1)      
#     list.insert(pos1, second_ele)   
#     list.insert(pos2, first_ele)         
#     return list

# #for first time users
# def user_insert(num):
#
# 	if num == 1:
# 		f=open("inputstring.txt" , "r")
# 		li=f.read().replace('\n' , '#').split("#")
# 		li=tuple(li)
# 		sql="INSERT INTO user(userid,name,pincode,mob,address) VALUES (%s,%s,%s,%s,%s)"
# 		li=list(li)
# 		li.insert(0 , key)
# 		li=swapPositions(li , 3, 4)
# 		val=tuple(li)
# 		user_cursor.execute(sql,val)
# 		key=key+1
# 		mydb.commit()
# 		return True
#
# 	#selection of type of shop
# 	if num == 2:
# 		mydb = mysql.connector.connect(
# 		host=config.host,
# 		user=config.user,
# 		passwd=config.passwd,
# 		database=config.database
# 		)
#
# 		key=config.user_key
# 		user_cursor=mydb.cursor()
#
# 		f=open("inputstring.txt" , "r")
# 		li=f.read().replace('\n' , '#').split("#")
# 		shop=li[-1]
#
# 		sql="SELECT name FROM client WHERE type==shop"
# 		result=user_cursor.execute(sql).fetchall()
# 		sql="SELECT clientid FROM client WHERE name==selected_shop"
# 		result=user_cursor.execute(sql).fetchone()
# 		return result

# selection of client id
# 	def shop_name(_shop_name_):

# 		sql="SELECT clientid FROM client WHERE name==selected_shop"
# 		result=user_cursor.execute(sql).fetchone
# 		return result

# 	def get_list(_list_):
# 		item_list=_list_

# 	def note(_note_):
# 		speacial_note=_note_

# 	def status(_status_):
# 		if(_status_=="Confirmed"):
# 			print("Order is Confirmed")
# 		if(_status_=="Cancelled"):
# 			print("Order is Cancelled")

# 	def amount(_amount_):
# 		tamount=_amount_
# 		print("Total amount"+_amount_)
# 		print("Payment Modes 1.COD 2.Online 3.Coupon 4.Cancel")

# 	def payment(_pmode_):
# 		pmode=_pmode_
# 		if pmode==1:
# 			print("Order is Confirmed")
# 		elif pmode==2:
# 			print("Order would be Confirmed after payment confirmation")
# 		elif pmode==3:
# 			print("Enter Coupon Code")
# 			check_coupon()
# 			if result:
# 				print("Coupon Applied")
# 				get_coupon()
# 				print("Discount"+disc_amt)
# 				print("Final amount"+tamount)
# 				print("Enter payment option")
# 				pmode=1
# 			else:
# 				print("Coupon Invalid")
# 		elif pmode==4:
# 			print("Are you sure")
# 			print("Order is Cancelled")

# 	def check_coupon(_coupon_):
# 		coupon=_coupon_
# 		sql="SELECT validity FROM coupon WHERE couponid==_coupon_"
# 		result=user_cursor.execute(sql).fetchone()

# 	def get_coupon(coupon):
# 		sql="SELECT price FROM coupon WHERE couponid==coupon"
# 		disc_amt=user_cursor.execute(sql).fetchone()
# 		tamount=tamount-disc_amount
# 		payment()

# 	def order_update():
# 		sql="INSERT INTO orders(client_id , user_id , order_date ,top , tod , order_list , note , payment ,coupon, disc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# 		val=(clientid,key,odate,odate,odate,item_list,speacial_note,pmode,couponid,disc_amt)
# 		user_cursor.execute(sql)

def check_is_shop_available(client_id):
    sql_query = "select close_hour from client where client_id = \""+client_id +"\""
    cursor.execute(sql_query)
    time_client = cursor.fetchone()[0]    
    time = datetime.datetime.now()
    time = time.strftime('%X').split(':')
    time = datetime.timedelta(seconds=int(time[2]),minutes=int(time[1]),hours=int(time[0]))
    print(time)
    if(time_client>time):
        return True
    elif(time_client<time):
        return False
    elif(time_client==time):
        return False

def user_update(name, address, mob, pincode, email):
    user_id = generate_user_id()
    sql = "INSERT INTO agent(user_id, name, address, mob, pincode, email_id) VALUES(%s, %s, %s, %s, %s, %s)"
    val = (user_id , name , address , mob , pincode, email)
    cursor.execute(sql ,val)
    mydb.commit()
    
def generate_user_id():
    sql = "SELECT user_id FROM user ORDER BY user_id DESC"
    cursor.execute(sql)
    result = cursor.fetchone()
    if(result == None): result=["UKA00000"]
    user_id = str(result[0])
    user_no = int(user_id[4:]) + 1
    user_id = user_id[0:3] + str(user_no).zfill(5)
    return user_id

def fuzzywuz(element, lis):
    match = process.extract(element, lis, limit=1)
    ratio = fuzz.ratio(match[0][0],element)
    if(ratio<70):
        return False
    else:
        return match[0][0]
    
def to_list(in_list):
    out_list=[]
    for type in in_list:
        out_list.append(type[0])
    return out_list 

def check_is_list_none(list_to_check):
    if(len(list_to_check)==0):
        return True
    else:
        return False

def client_type(pincode):
    sql="SELECT distinct type FROM client WHERE pincode="+str(pincode)
    cursor.execute(sql)
    result=cursor.fetchall()
    return to_list(result)

def validate_pincode(pincode):
    sql = "SELECT * FROM client WHERE pincode = %s"
    val = (pincode,)
    user_cursor.execute(sql, val)
    rows = user_cursor.fetchall()
    # The result of a "cursor.execute" can be iterated over by row
    try:
        result = True
        pincode = str(pincode)
        pincode_request = "https://api.postalpincode.in/pincode/" + pincode
        p = rows[0]
    except:
        result = False
    try:
        import urllib.request, json
        with urllib.request.urlopen(pincode_request) as url:
            data = json.loads(url.read().decode())
        msg = data.pop(0)
        city = msg['PostOffice'][0]["Name"]
    except:
        city = "wrong city selected"

    return result, city
def client_name_id(type, pincode):
    sql="SELECT name FROM client WHERE pincode="+str(pincode)+" AND type=\""+str(type)+"\""
    cursor.execute(sql)
    result_client_name=to_list(cursor.fetchall())
    sql="SELECT client_id FROM client WHERE pincode="+str(pincode)+" AND type=\""+str(type)+"\""
    cursor.execute(sql)
    result_client_id=to_list(cursor.fetchall())
    for i in range(len(result_client_id)):
        if(check_is_shop_available(result_client_id[i])):
            pass
        else:
            result_client_id.pop(i)
            result_client_name.pop(i)
    return result_client_name, result_client_id

def get_category(pincode):
    categories = client_type(pincode)
    categories = list(dict.fromkeys(categories))
    return categories

def get_client_id(name, pincode):
    sql="SELECT client_id FROM client WHERE pincode="+str(pincode)+" AND name=\""+str(name)+"\""
    cursor.execute(sql)
    result=cursor.fetchone()[0]
    return result

def get_shops(pincode, type):
    categories = client_type(pincode)
    match = fuzzywuz(type, categories)
    if(match is False):
        shop_list = ["Sorry to say!!, No shop available right now!!!"]
    shop_list = client_name_id(match, pincode)
    return shop_list, match

def convert_category_name(keyword):
    if(keyword=="GEN"):
        return "General store"
    elif(keyword=="GRO"):
        return "Grocery store"
    elif(keyword=="PHA"):
        return "Pharmacy store"
    elif(keyword=="STA"):
        return "Stationary store"
    else:
        return "Oops!! 😮 we lost this category"
def get_item_link(pincode, shop):
    sql_querry = "select item from client where pincode="+pincode+"name=\""+shop+"\""
    cursor.execute(sql_querry)
    item_link = cursor.fetchone()[0]
    return item_link

def get_item_name(sku):
    sql_querry = "select name from items where sku = {}".format(sku)
    cursor.execute(sql_querry)
    name = cursor.fetchone()[0]
    return name

def get_items(shop, type, pincode):
    shops, dumy = get_item_link(pincode, type)
    match = fuzzywuz(shop, shops)
    if(match is False):
        item_link = ["https://i.ibb.co/gPGsw0b/1.png"]
    else:
        item_link = get_item_link(pincode, match)
    return item_list, match

def get_sku(items):
    sku=[]
    for item in items:
        sql="SELECT sku FROM items WHERE name=' "+item+"'"
        cursor.execute(sql)
        result=cursor.fetchone()
    return result[0]

def get_items_type(sku, client_id):
    sql_query = "select type from {} where sku={}".format(client_id, sku)
    cursor.execute(sql_query)
    type = cursor.fetchone()[0]
    return type

def set_items_and_return_quantity_type(items, shop, pincode):
    try:
        items = items.split(',')
    except:
        pass
    client_id = get_client_id(shop, pincode)
    skus = []
    quantity_type = []
    wrong_items = []
    wrong_items_name = []
    available_item = []
    for i in range(len(items)):
        skus.append(get_sku(items[i]))
    for i in range(len(skus)):
        try:
            quantity_type.append(get_items_type(skus[i], client_id))
            available_item.append(get_item_name(skus[i]))
        except:
            wrong_items.append(skus[i])
    for i in range(len(wrong_items)):
        wrong_items_name.append(get_item_name(wrong_items[i]))
    d = {}
    for i in range(len(quantity_type)):
        try:
            print(d[quantity_type[i]])
            l = d[available_item[i]]
            l.append(quantity_type[i])
            d[available_item[i]] = l
        except:
            l = []
            l.append(quantity_type[i])
            d[available_item[i]] = l
    return wrong_items_name, available_item, d

def block_order(client_id , items , quantity):
    stock=[]
    for s in get_sku(items):
        sql="SELECT in_stock,sold_stock FROM  "+str(clientid)+" WHERE sku="+str(s)
        cursor.execute(sql)
        result=cursor.fetchone()
        stock.append(result)

    updated_stock=[]
    for count,each in enumerate(stock):
        update=list(each)
        update[0]=update[0]-quantity[count]
        update[1]=update[1]+quantity[count]
        updated_stock.append(tuple(update))

    for count,sku in enumerate(get_sku(items)):
        sql="UPDATE "+str(clientid)+" SET in_stock=%s ,sold_stock=%s WHERE sku=%s"
        sql_list=list(updated_stock[count])
        sql_list.append(sku)
        val=tuple(sql_list)
        cursor.execute(sql , val)
        mydb.commit()   
           
def get_quantity(quantity, shop, items, quantity_in_number, pincode):
    try:
        items = items.split(',')
        quantity = quantity.split(',')
        number = quantity_in_number.split(',')
    except:
        items = items
        quantity = quantity
        number = quantity_in_number
    try:
        
        if len(items) != len(quantity) or len(items) != len(number) or len(quantity) != len(number)  :
            return False, False, False
        client_id = get_client_id(shop, pincode)
        sql_update_query = "select type from {}".format(client_id)
        user_cursor.execute(sql_update_query)
        product = user_cursor.fetchall()
        quantity_list = []
        for i in range(len(product)):
            quantity_list.append(product[i][0])
        quan = []
        for i in range(len(quantity)):
            if fuzzywuz(match, quantity_list):
                quan.append(fuzzywuz(match, quantity_list))
            else:
                raise TypeError("Wrong entries")
        if(check_is_shop_available(client_id)):
            raise TypeError("shops closed")
        price_list = []
        for i in range(len(quan)):
            sku = get_sku(items[i])
            block_order(client_id, items[i], quan[i])
            sql_update_query = "select amount from {} where sku = %s and type = %s".format(client_id)
            val = (sku, quan[i])
        
            user_cursor.execute(sql_update_query, val)
            price = user_cursor.fetchone()
            price_list.append(price[0])
            sume = 0
        #block_order()
        for i in range(len(price_list)):
            number[i] = int(number[i])
            sume = sume + price_list[i] * number[i]

        return sume, price_list, quan
    except:
        return False, False, False




