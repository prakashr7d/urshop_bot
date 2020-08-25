
from instamojo_wrapper import Instamojo
import datetime

api = Instamojo(api_key="test_3dba2687364497f95df15b096ad", auth_token="test_d787d56dc327e9eeb394c9a49c6", endpoint='https://test.instamojo.com/api/1.1/');
# Create a new Payment Request
def create_payment_request(phone , amount , name):
	response = api.payment_request_create(
		send_sms=True, 
		phone =str(phone),
	    amount=str(amount),
	    buyer_name=str(name),
	    purpose='For your payment at UrShop',
	    redirect_url="https://wa.me/+14155238886?",
	    webhook='https://907f3a5b7051.ngrok.io/postjson',
	    send_email=False,
	    allow_repeated_payments=False,
	    # expires_at='2020-08-02T11:11:11'
	    )
	return response

print(create_payment_request(8382930122 , 120 , 'Aryan'))

# response=api.payment_request_status('71976bfef7bd48d68b1d337610fb8e6c')
# payment_request_id =response['payment_request']['id']
# payment_request_status=response['payment_request']['status']
# paymentid=response['payment_request']['payments'][0]['payment_id']
# payment_id_status=response['payment_request']['payments'][0]['payment_id']['status']

# print(payment_request_id)
# print(payment_request_status)
# print(paymentid)
# response = api.payment_request_payment_status('71976bfef7bd48d68b1d337610fb8e6c')
# longurl=response['payment_request']['longurl']
# print(longurl)
# paymentid=response['payment_request']['id']
# print(paymentid)
# print(response)

def create_transanction(order_id , amount , phone , name):
	import mysql.connector

	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="I@m@ry@n9044938983",
		database="UrShop"
	)
	cursor=mydb.cursor(buffered=True)
	now = datetime.datetime.now()
	trans_time=now.strftime("%H:%M:%S")
	trans_date=now.strftime("%y:%m:%d")
	response=create_payment_request(phone , amount , name)
	payment_request_id =response['payment_request']['id']
	print(response['payment_request']['longurl'])
	payment_request_status=str(response['payment_request']['status'])
	sql="INSERT INTO transanctions(order_id , trans_id , payment_mode , trans_date , trans_time ,trans_status , trans_amt) VALUES(%s , %s ,%s , %s ,%s , %s, %s)"
	val=(order_id  ,payment_request_id , "ONLINE" ,trans_date , trans_time,payment_request_status , amount )
	cursor.execute(sql, val)
	mydb.commit()
	return response['payment_request']['longurl']
	
# create_transanction("CKA001" , 120 , 8382930122 , "Aryan")

