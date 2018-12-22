import csv
import time

from PIL import Image

letters = "A B C D E F G H I J K L M N O".split()

running = True
atlasList = {}
totalPlayers = 0
htmlbody = ""


def htmlInit():
	f = open("index.html", "w")
	html = open("htmltop.html", "r")
	f.write(html.read())

def createImage():
	img = Image.new('RGB', (4096, 4096), color = 'red')
	img.save('static/hotspots.png')

while(running == True):
	with open('atlasserver.txt', 'r') as atlasTXT:

		spawnNETF = [0, 0]
		for line in atlasTXT:
			row = line.split(",")
			out = []
			if(len(row) > 2):
				if "Northeast Tropical Freeport" in row[2]:
					#print("WE FOUND EM BOIZZZZZZZZ"+row[0]+row[1]+row[2])
					spawnOut = []
					if(int(row[0]) > int(spawnNETF[0])):
						spawnNETF = row
					try:
						spawnOut.append((int(spawnNETF[0])/int(spawnNETF[1]))*100)
					except ValueError:
						spawnOut.append(0)
					except ZeroDivisionError:
						spawnOut.append(0)
					spawnOut.append(spawnNETF[0])
					spawnOut.append(spawnNETF[1])
				
					atlasList["M7"] = spawnOut
				else:
					sn1 = row[2].split()
					sn2 = str(sn1[0]).split("_")
					#print("SN2::")
					#print(sn2)
					if(len(sn2) > 1):
						if(len(sn2[1]) < 10 and len(sn2[1]) < 4):
							try:
								out.append((int(row[0])/int(row[1]))*100)
							except ValueError:
								out.append(0)
							except ZeroDivisionError:
								out.append(0)
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
					try:
						tplay += int(result[1])
					except ValueError:
						print("Error with playerCount for "+searchString)
						continue
				print(searchString, result)

		totalPlayers = tplay
		print(totalPlayers)
		print("Total Len:"+str(len(atlasList)))
		#running = True
		htmlInit()
		createImage()
		time.sleep(5)


