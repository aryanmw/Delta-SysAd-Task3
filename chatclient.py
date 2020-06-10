import socket
import threading
import time
import getpass
import mysql.connector
import re

connection = mysql.connector.connect(host="localhost",user="aryanw",password="aryanw",database="newrecentmessagesdb")

cursor = connection.cursor()

username = getpass.getuser()

tLock = threading.Lock()
shutdown = False

def receiving(name, sock):
	while not shutdown:
		try:
			tLock.acquire()
			while True:
				data, addr = sock.recvfrom(1024)
				print(str(data))
				cursor.execute("TRUNCATE "+username)
				connection.commit()


		except:
			pass
		finally:
			tLock.release()

host = '127.0.0.1'

port = 0

server = ('127.0.0.1', 5000)
chiefuser = ('127.0.0.1', 65432)
#46816
armygenuser = (host, 46816)
#43588
navymaruser = (host, 43588)
#58476
airuser = (host, 58476)
#35123
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if "ChiefComm" in username:
	s.bind((host,65432))
elif "ArmyGeneral" in username:
	s.bind((host, 46816))
elif "NavyMarshal" in username:
	s.bind((host, 43588))
elif "AirForceChief" in username:
	s.bind((host, 58476))
else:
	s.bind((host,port))

s.setblocking(0)

rT = threading.Thread(target=receiving, args=("RecvThread", s))
rT.start()


alias = username
recepient = "d"
if "Army" in alias:
	cursor.execute("SELECT message FROM "+ username)
	mess = cursor.fetchall()
	for m in mess:
		print (m)

	cursor.execute("truncate " + username)
	connection.commit()



if "ArmyGeneral" in alias or "NavyMarshal" in alias or "AirForceChief" in alias:
	print ("Please enter ChiefCommander to send a personal message else press enter")
	recepient = input("Recepient -> ")
	print ("Connection established")

print ("Enter quit to exit")
message = input(alias + "-> ")
while message != 'quit':
	if message != '':
		response = alias + ": " + message
		if "ChiefCommander" in recepient:
			s.sendto(response.encode(), chiefuser)

		elif "ArmyGeneral" in recepient:
			s.sendto(response.encode(), armygenuser)

		elif "NavyMarshal" in recepient:
			s.sendto(response.encode(), navymaruser)

		elif "AirForceChief" in recepient:
			s.sendto(response.encode(), airuser)

		else:
			s.sendto(response.encode(), server)


	tLock.acquire()
	message = input(alias + "-> ")
	tLock.release()
	time.sleep(0.2)
shutdown = True
rT.join()
s.close()
