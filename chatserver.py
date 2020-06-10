import socket
import time
import re
import mysql.connector

connection = mysql.connector.connect(host="localhost", user="aryanw", password="aryanw")
cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS newrecentmessagesdb")

mydb = mysql.connector.connect(host="localhost", user="aryanw", password="aryanw", database="newrecentmessagesdb")
mycursor = mydb.cursor()

i=1
while i < 3:
	mycursor.execute("CREATE TABLE IF NOT EXISTS Army"+str(i)+" (message VARCHAR(300), user VARCHAR(20))")
	mycursor.execute("CREATE TABLE IF NOT EXISTS Navy"+str(i)+" (message VARCHAR(300), user VARCHAR(20))")
	mycursor.execute("CREATE TABLE IF NOT EXISTS AirForce"+str(i)+" (message VARCHAR(300), user VARCHAR(20))")
	i+=1

mycursor.execute("CREATE TABLE IF NOT EXISTS ArmyGeneral (message VARCHAR (300), user VARCHAR (20))")
mycursor.execute("CREATE TABLE IF NOT EXISTS NavyMarshal (message VARCHAR (300), user VARCHAR (20))")
mycursor.execute("CREATE TABLE IF NOT EXISTS AirForceChief (message VARCHAR (300), user VARCHAR (20))")
mycursor.execute("CREATE TABLE IF NOT EXISTS ChiefCommander (message VARCHAR (300), user VARCHAR (20))")

host = '127.0.0.1'
port = 5000

clients = []
clientsNavy = []
clientsAir = []
clientArmyGeneral = []
clientNavyMarshal = []
clientAirChief = []
clientChiefCommander = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

quitting = False
print ("Server Started!")

i = 1


while not quitting:
	try:
		data, addr = s.recvfrom(1024)
		while i < 2:
			s.sendto(data, addr)
			i+=1

		decodedString = data.decode('utf-8')[:9]
		usernameString = data.decode('utf-8')[:5]
		airDecoded = data.decode('utf-8')[:9]
		if "Quit" in str(data):
			quitting = True


		if addr not in clients:
			if "Army" in decodedString:
				if "ArmyGen" not in airDecoded:
					clients.append(addr)

				else:
#					clientArmyGeneral.append(addr)
					clients.append(addr)



		if addr not in clientsNavy:
			if "Navy" in decodedString:
				if "NavyMar" not in airDecoded:
					clientsNavy.append(addr)
				else:
#					clientNavyMarshal.append(addr)
					clientsNavy.append(addr)
#					clientArmyGeneral.append(addr)



		if addr not in clientsAir:
			if "Air" in decodedString:
				if "AirForceC" not in airDecoded:
					clientsAir.append(addr)
				else:
#					clientArmyGeneral.append(addr)
					clientsAir.append(addr)


		if "ChiefCom" in decodedString:
			chiefaddr = addr
			if chiefaddr not in clients:
#				clientArmyGeneral.append(chiefaddr)
				clients.append(chiefaddr)
				clientsNavy.append(chiefaddr)
				clientsAir.append(chiefaddr)


		print(time.ctime(time.time()) + str(addr) + ": :" + str(data))



		if "Army" in decodedString:
			j=1
			while j < 3:
				insert_string = "INSERT INTO Army"+str(j)+" (message, user) VALUES (%s, %s)"
				val = (str(data), decodedString)
				mycursor.execute(insert_string, val)
				mydb.commit()
				j+=1



			for c in clients:
				if "Army" in decodedString:
#						if addr != c:
					s.sendto(data, c)


		if ("ArmyGene" in decodedString) or ("NavyMars" in decodedString) or ("AirForceC" in decodedString) or ("ChiefComm" in decodedString):
			for g in clientArmyGeneral:
				if addr != chiefaddr:
					s.sendto(data, g)



		if "Navy" in decodedString:
			insert_navy = "INSERT INTO Navy (message, user) VALUES (%s, %s)"
			navyVal = (str(data), decodedString)
			mycursor.execute(insert_navy, navyVal)
			mydb.commit()
			if addr != chiefaddr:
				for nc in clientsNavy:
					if "Navy" in decodedString:
#						if addr != nc:
						s.sendto(data,nc)


		elif "Air" in decodedString:
			insert_air = "INSERT INTO AirForce (message, user) VALUES (%s, %s)"
			airVal = (str(data), airDecoded)
			mycursor.execute(insert_air, airVal)
			mydb.commit()
			if addr != chiefaddr:
				for ac in clientsAir:
					if "Air" in decodedString:
						if addr != ac:
							s.sendto(data,ac)





	except:
		pass
s.close()
