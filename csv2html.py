import csv
import time

letters = "A B C D E F G H I J K L M N O".split()

running = True
atlasList = {}
totalPlayers = 0
htmlbody = ""


def htmlInit():
	f = open("index.html", "w")
	html = open("htmltop.html", "r")
	f.write(html.read())

htmlInit()

while(running == True):
	with open('atlasserver.txt', 'r') as atlasTXT:

		for line in atlasTXT:
			row = line.split(",")
			out = []
			if(len(row) > 2):
				sn1 = row[2].split()
				sn2 = str(sn1[0]).split("_")
				if(len(sn2) < 2):
					continue

				if(len(sn2[1]) < 10 and len(sn2[1]) < 4):
					out.append((int(row[0])/int(row[1]))*100)
					out.append(row[0])
					out.append(row[1])
					atlasList[sn2[1]] = out
			else:
				continue
		tplay = 0
		for x in range(0,15):
			rows = []
			for y in range(0,15):
				cols = []
				searchString = letters[x]+str(y+1)
				result = atlasList.get(searchString)
				if(result != None):
					tplay += int(result[1])
				print(searchString, result)

		totalPlayers = tplay
		print(totalPlayers)
		print("Total Len:"+str(len(atlasList)))
		#running = True
		time.sleep(5)


