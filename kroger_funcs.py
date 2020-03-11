import requests
import json
import uuid

session = requests.Session()
token = False
#session.verify = False
#session.proxies = { 'https': 'http://127.0.0.1:8080' }

def update_headers(func):
	global session, token
	if token:
		session.headers.update(
			{
				"Authorization": "Bearer " + token
			}
		)
	session.headers.update(
		{
				"user-agent": "krogerco/20.2/iOS",
				"user-time-zone": "America/New_York",
				"x-correlation-id": str(uuid.uuid4()),
				"x-device-type": "iOS phone 2x",
				"accept-language": "en-US;q=1",
				"accept": "application/json",
				"content-type": "application/json",
				"accept-encoding": "br, gzip, deflate"				
				#"app-session-scope": "FCC57584-8352-4FD6-940F-60AB72C0DD0A"				
		}
	)
	if func == "create_kroger_account":
		session.headers.update(
			{
				"x-applicationauthorizationtoken": "20C2829F-8508-4B69-B420-840D31504DFE",
			}
		)
		return()
	if func == "do_kroger_login":
		session.headers.update(
			{
				"content-type": "application/x-www-form-urlencoded",
				"Authorization": "Basic a3JvZ2VyLW1vYmlsZS1pb3M6YzFkZjVlMTAtZDUxYy00ZWIzLWI2NWEtZTQ4ZmQ3ZTZiOWNj",
				"x-applicationauthorizationtoken": "c1df5e10-d51c-4eb3-b65a-e48fd7e6b9cc"
			}
		)
		return()
	if func == "link_kroger_altid":
		session.headers.update(
			{
				"x-applicationauthorizationtoken": "5DD35184-766C-4784-9DE3-4A36F3B79BD6",
			}
		)
		return()
	if func == "get_kroger_coupons":
		session.headers.update(
			{
				"x-applicationauthorizationtoken": "C7915B2C-47C3-4FA5-8522-3FE7CA2BC2ED"
			}
		)
		return()
	if func == "clip_kroger_coupons":
		session.headers.update(
			{
				"x-applicationauthorizationtoken": "C7915B2C-47C3-4FA5-8522-3FE7CA2BC2ED",
				"x-http-method-override": "PUT"
			}
		)
		return()
	if func == "unclip_kroger_coupons":
		session.headers.update(
			{
				"x-applicationauthorizationtoken": "C7915B2C-47C3-4FA5-8522-3FE7CA2BC2ED",
				"x-http-method-override": "DELETE"
			}
		)
		return()
	if func == "check_kroger_coupon":
		session.headers.update(
			{
				"x-applicationauthorizationtoken": "C7915B2C-47C3-4FA5-8522-3FE7CA2BC2ED",
				"x-http-method-override": "GET"
			}
		)
		return()	
def create_kroger_account (email, password, divisionNumber, storeNumber):
	global session, token
	update_headers("create_kroger_account")
	createurl = 'https://mobile.kroger.com/mobileprofile/api/v2/user/kroger'
	payload = {
									"defaultAdvertisingPreferenceOption": True,
									"defaultEmailPreferenceOption": False,
									"emailAddress": email,
									"password": password,
									"preferredStoreDivisionNumber": divisionNumber,
									"preferredStoreNumber": storeNumber
						}
	r = session.post(createurl, data=json.dumps(payload))
	#print (r.text)
	try:
		rjson = r.json()
	except:
		return (False)
	else:	
		if rjson.get("message"):
			print (rjson.get("message"))
			return (False)
		else:
			token = rjson["access_token"]
			return(rjson["access_token"])


def link_kroger_altid (firstName, lastName, divisionNumber, alternateId):
	global session
	update_headers("link_kroger_altid")
	linkurl = 'https://mobile.kroger.com/mobilerewards/api/v1/virtual-card/kroger'
	payload = {
									"alternateId": alternateId,
									"divisionNumber": divisionNumber,
									"firstName": firstName,
									"lastName": lastName
	}
	r = session.post(linkurl, data=json.dumps(payload))
	#print(r.text)
	try:
		rjson = r.json()
	except:
		return (False)
	else:	
		if rjson.get("message"):
			print (rjson.get("message"))
			return (False)
		else:
			return(rjson["virtualCardNumber"])

def do_kroger_login(username, password):
	global session, token
	update_headers("do_kroger_login")
	loginurl = "https://mobile.kroger.com/v1/connect/oauth2/token?pid=%s" % str(uuid.uuid4())
	payload = {
									"banner": "KROGER",
									"grant_type": "password",
									"password": password,
									"username": username
	}
	r = session.post(loginurl, data=payload)
	rjson = r.json()
	if rjson.get("error"):
		print(rjson.get("error_description"))
		return(False)
	else:
		token = rjson["access_token"] 
		return(True)

def get_kroger_coupons (division, store, clipped):
	global session, token
	if not token:
		print ("Not logged in!")
		return(False)
	update_headers("get_kroger_coupons")
	couponurl = 'https://mobile.kroger.com/mobilecoupons/api/v1/coupons/kroger/%s/%s?inclusions=modalities,upcs,monetization' % (division, store)
	r = session.get(couponurl)
	rjson = r.json()
	coupons = rjson.get("coupons")
	couponids = []
	if not coupons:
		print (r.text)
		return (False)
	else:
		for coupon in coupons:
			if clipped == coupon["addedToCard"]:
				couponids.append({"id": coupon["id"], "description": coupon["shortDescription"]})
	return(couponids)

def clip_kroger_coupons (coupons):
	global session, token
	if not token:
		print ("Not logged in!")
		return(False)
	update_headers("clip_kroger_coupons")
	clipurl = 'https://mobile.kroger.com/mobilecoupons/api/v1/coupon/kroger'
	for coupon in coupons:
		r = session.post('%s/%s' % (clipurl, coupon["id"]))
		if r.json()["httpStatus"] == 200:
			print("Successfully clipped coupon %s - %s" % (coupon["id"], coupon["description"]))
		else:
			print("Failed to clip coupon %s - %s - %s" % (coupon["id"], coupon["description"], r.json()["details"]))

def unclip_kroger_coupons (coupons):
	global session, token
	if not token:
		print ("Not logged in!")
		return(False)
	update_headers("unclip_kroger_coupons")
	clipurl = 'https://mobile.kroger.com/mobilecoupons/api/v1/coupon/kroger'
	for coupon in coupons:
		r = session.post('%s/%s' % (clipurl, coupon["id"]))
		if r.json()["httpStatus"] == 200:
			print("Successfully unclipped coupon %s - %s" % (coupon["id"], coupon["description"]))
		else:
			print("Failed to unclip coupon %s - %s - %s" % (coupon["id"], coupon["description"], r.json()["details"]))

def check_kroger_coupon (coupon):
	global session, token
	if not token:
		print ("Not logged in!")
		return(False)
	update_headers("check_kroger_coupon")
	clipurl = 'https://mobile.kroger.com/mobilecoupons/api/v1/coupon/kroger'
	r = session.post('%s/%s' % (clipurl, coupon))
	rjson = r.json()
	if rjson.get('addedToCard') is None:
		return1 = False
		return2 = rjson['details']
	else:
		return1 = rjson["addedToCard"]
		return2 = rjson["shortDescription"]
	return(return1, return2)