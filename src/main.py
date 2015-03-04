#! /usr/bin/python2.7

import simplejson as json
from bottle import get, post, route, run,template,request # or route

#from flask import Flask, jsonify, abort, make_response, request

#app = Flask(__name__)

from dbOperations import Couch

#creating an object of couch
foo = Couch('localhost','5984')
pin_number = board_number = number = pin_attach_number = 1

#register the user
@route('/v1/reg', method='POST')
def register():
	global number
	print number
	body = '''
	{
			"name":"'''+ request.json['name']+'''",
			"username":"'''+request.json['username']+'''",
			"password":"'''+request.json['password']+'''"			
	}
	'''
	a = foo.saveDoc('userdb',body,'user'+str(number))
	b = json.loads(a)	
	print b['ok']
	number+=1
	return "user_id: "+b['id']+"\n"

#user login
@route('/v1/login', method='POST')
def login():
	
	a = foo.listDoc('userdb')
	print a
	b = json.loads(a)
	#print b['rows'][0]	
	for i in range(0,b['total_rows']):
		userdoc = b['rows'][i]['id']
		#print type(userdoc)
		c = foo.openDoc('userdb',userdoc)
		d = json.loads(c)
		print d
		username = d['username']
		print username		
		password = d['password']
		print password		
		print request.json['username']
		print request.json['password']
		if username == request.json['username'] and password == request.json['password']:
			return "user_id: "+d['_id']+"\n"
	else:
		return "wrong username or password \n"

#create board
@route('/v1/user/<user_id>/board', method='POST')
def create_board(user_id):
	global board_number
	#print board_number
	body = '''
	{
			"board_name":"'''+request.json['boardname']+'''",
			"user_id":"'''+user_id+'''"
	}
	'''
	a1 = foo.listDoc('userdb')
	b1 = json.loads(a1)
	for i in range(0,b1['total_rows']):
		userdoc = b1['rows'][i]['id']
		#print "user is "+userdoc
		c = foo.openDoc('userdb',userdoc)
		d = json.loads(c)
		#print d
		gotUser_id = d['_id']
		#print "entered id :"+user_id
		if gotUser_id == user_id:
			a = foo.saveDoc('boarddb',body,'board'+str(board_number))
			#print "saving and saved board :"+a
			b = json.loads(a)
			#print b['ok']
			board_number+=1
			return "board_id: "+b['id']+"\n"
	else:
		return "no such user_id " +user_id+" to create boards\n"

#upload pins(create)
@route('/v1/user/<user_id>/pin/upload', method='POST')
def upload_pin(user_id):
	global pin_number
	print pin_number
	body = '''
	{
		"pin_url":"'''+request.json['pinurl']+'''",
		"user_id":"'''+user_id+'''"
	}
	'''
	a1 = foo.listDoc('userdb')
	b = json.loads(a1)
	for i in range(0,b['total_rows']):
		userdoc = b['rows'][i]['id']
		print "user is "+userdoc
		c = foo.openDoc('userdb',userdoc)
		d = json.loads(c)
		print d
		gotUser_id = d['_id']
		print "entered user id :"+user_id
		if gotUser_id == user_id:
			a = foo.saveDoc('pindb',body,'pin'+str(pin_number))
			print "saving and saved board :"+a
			b = json.loads(a)
			print b['ok']
			pin_number+=1
			return "pin_id: "+b['id']+"\n"
	else:
		return "no such user_id " +user_id+" to upload pins\n"


# get all Pins
@route('/v1/pins',method='GET')
def getAllPins():
	allPins = []
	a1 = foo.listDoc('pindb')
	b = json.loads(a1)
	for i in range(0,b['total_rows']):
		pindoc = b['rows'][i]['id']
		print "pin is "+pindoc
		c = foo.openDoc('pindb',pindoc)
		allPins.append(c)
	return allPins

# get all Boards
@route('/v1/boards',method='GET')
def getAllBoards():
	allBoards = []
	a1 = foo.listDoc('boarddb')
	b = json.loads(a1)
	for i in range(0,b['total_rows']):
		boarddoc = b['rows'][i]['id']
		print "board is "+boarddoc
		c = foo.openDoc('boarddb',boarddoc)
		allBoards.append(c)
	return allBoards

# delete board
@route('/v1/user/<user_id>/board/<board_id>',method='DELETE')
def deleteBoard(user_id, board_id):
	a = foo.listDoc('boarddb')
	print a
	b = json.loads(a)
	#print b['rows'][0]	
	for i in range(0,b['total_rows']):
		userdoc = b['rows'][i]['id']
		print "user doc: "+userdoc
		#print type(userdoc)
		c = foo.openDoc('boarddb',userdoc)
		#print c
		d = json.loads(c)
		target_id = d['_id']
		targetUserId = d['user_id']
		delete_rev = d['_rev']
		print "board id :"+board_id
		print "target id :" + target_id
		print "revision :"+delete_rev
		#if
		if target_id == board_id and targetUserId == user_id:
			m = foo.deleteDoc('boarddb',board_id,delete_rev)
			print m
			return "Board deleted sucessfully \n"
	else:
		return "cant find board to delete \n"

# update --attach pin to board
@route('/v1/user/<user_id>/board/<board_id>',method='PUT')
def attachPin(user_id, board_id):
	#list of boards
	aBoard = foo.listDoc('boarddb')
	print aBoard
	bBoard = json.loads(aBoard)
	for i in range(0,bBoard['total_rows']):	
		boarddoc = bBoard['rows'][i]['id']
		print "board doc :" +boarddoc
		cBoard = foo.openDoc('boarddb',boarddoc)
		print cBoard
		dBoard = json.loads(cBoard)
		gotBoard_id = dBoard['_id']
		gotUser_id = dBoard['user_id']
		print "board id "+gotBoard_id
		if gotBoard_id == board_id and gotUser_id == user_id:
			print "this board exists "
			pin_id = request.json['pinid']		
			#list of pins
			a = foo.listDoc('pindb')
			print a
			b = json.loads(a)
			#print b['rows'][0]
			for i in range(0,b['total_rows']):
				userdoc = b['rows'][i]['id']
				print "user doc: "+userdoc
				#print type(userdoc)
				c = foo.openDoc('pindb',userdoc)
				print c
				d = json.loads(c)
				target_id = d['_id']
				update_rev = d['_rev']
				pin_url = d['pin_url']
				user_id = d['user_id']
				print d.get('board_id')
				concat_board_id = ''
				if d.get('board_id') != None :
					gotBoard_id = d['board_id']
					concat_board_id = gotBoard_id+","+board_id
				print "board id :"+board_id
				print "target id :" + target_id
				print "revision :"+update_rev
				print "pin url :"+pin_url
				#if
				body = '''
				{
						"user_id":"'''+user_id+'''",
						"pin_url":"'''+pin_url+'''",
						"_rev":"'''+update_rev+'''",
						"board_id":"'''+board_id+'''"
				}
				'''
				print board_id
				if target_id == pin_id:
					m = foo.updateDoc('pindb',body,pin_id,update_rev)
					print m
					return "pin: "+pin_id+" attached successfully \n"
			else:
				return "pin: "+pin_id+" doesn't exist\n"
	else:
		return "board id:"+board_id+" for this user:"+user_id+" doesn't exist\n"
#get specific board pins
@route('/v1/boards/<board_id>')
def getBoardPins(board_id):

	target_board = board_id
	pins = []
	output = []
	#list of pins
	a = foo.listDoc('pindb')
	print a
	b = json.loads(a)
	#looping pins to check for boardid
	for i in range(0,b['total_rows']):
		currentPinId = b['rows'][i]['id']
		print currentPinId
		#enter each pin docs by pinid
		c = foo.openDoc('pindb',currentPinId)
		print c
		d = json.loads(c)
		currentPinBoard = d['board_id']
		if currentPinBoard == target_board:
			pins.append(c)

	output.append(pins)
	return pins

#adding comment to specific pin
@route('/v1/user/<user_id>/pin/<pin_id>/comment', method ='POST')
def addComments(user_id, pin_id):

	#list of pins
	a = foo.listDoc('pindb')
	print a
	b = json.loads(a)
	#print b['rows'][0]
	for i in range(0,b['total_rows']):
		userdoc = b['rows'][i]['id']
		print "user doc: "+userdoc
		#print type(userdoc)
		c = foo.openDoc('pindb',userdoc)
		print c
		d = json.loads(c)
		target_id = d['_id']
		update_rev = d['_rev']
		pin_url = d['pin_url']
		board_idInside = d['board_id']
		user_idInside = d['user_id']
		#ter = request.json['comment']
		ter = user_id+":"+request.json['comment']
		print ter
		print "board id :"+user_idInside
		print "target id :" + target_id
		print "revision :"+update_rev
		print "pin url :"+pin_url
		#if
		body = '''
		{
			"user_id":"'''+user_idInside+'''",
			"pin_url":"'''+pin_url+'''",
			"_rev":"'''+update_rev+'''",
			"board_id":"'''+board_idInside+'''",
			"comments":"['''+ter+''']"
		}
		'''
		if target_id == pin_id:
			m = foo.updateDoc('pindb',body,pin_id,update_rev)
			print m
			return "User :"+user_id +" commented on pin : "+pin_id +" \" "+request.json['comment'] +" \"  \n"

# get specific Pins
@route('/v1/pin/<pin_id>',method='GET')
def getPin(pin_id):
	targPin = []
	a = foo.listDoc('pindb')
	b = json.loads(a)
	for i in range(0,b['total_rows']):
		pindoc = b['rows'][i]['id']
		print "pin is "+pindoc
		c = foo.openDoc('pindb',pindoc)
		d = json.loads(c)
		if d['_id'] == pin_id:
			targPin.append(c)
			return targPin
	else:
		return "Pin not found \n"

#get user info 
@route('/v1/user/<user_id>',method='GET')
def getUserInfo(user_id):
	a = foo.listDoc('userdb')
	b = json.loads(a)
	#userInfo =""
	for i in range(0,b['total_rows']):
		userdoc = b['rows'][i]['id']
		print "userdoc "+userdoc
		c = foo.openDoc('userdb',userdoc)
		print c
		d = json.loads(c)
		if d['_id'] == user_id:
			userInfo = "Name :"+d['name']+"\n"
			a1 = foo.listDoc('boarddb')
			b1 = json.loads(a1)
			for i in range(0,b1['total_rows']):
				boarddoc = b1['rows'][i]['id']			
				c1 = foo.openDoc('boarddb',boarddoc)
				d1 = json.loads(c1)
				if d1['user_id'] == user_id:
					userInfo = userInfo+"board id :"+d1['_id']+"\nboard name :"+d1['board_name']
			return "Information Retrieved: \n"+userInfo+"\n"
			
	else:
		return "no user id:"+user_id+" to retrieve\n"
run(host='localhost',port='8080')
