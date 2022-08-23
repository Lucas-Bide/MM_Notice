import requests
import xml.etree.ElementTree as ET
import json
from os.path import exists

data = requests.get("https://www.megamillions.com/cmspages/utilservice.asmx/GetLatestDrawData")
# Response format is <string> *json* </string>
xml = ET.fromstring(data.content)
jsn = json.loads(xml.text)

jackpot = jsn["Jackpot"]["NextPrizePool"]

# Whether that jackpot has been won
reset = False

# Initialize with 0 jackpot value
if not exists("jackpot.txt"):
	with open("jackpot.txt", "x") as f:
		f.write("300000000") # change later

f = open("jackpot.txt", "r+")

old_jackpot = f.readline()
f.seek(0)
f.truncate()
f.write(str(int(jackpot)))
f.close()

jold = int(old_jackpot)
jew = int(jackpot)

if jew >= 300000000 and jold < 300000000: #text to alert start of buy season
	print("Start buying. The current jackpot is $%d" %(jew))

if jold >= 300000000 and jew < jold: # text to alert that the jackpot was won
	print("The jackpot was won. Prize: $%d. Numbers: %d %d %d %d %d %d" %(jold, jsn["Drawing"]["N1"], jsn["Drawing"]["N2"], jsn["Drawing"]["N3"], jsn["Drawing"]["N4"], jsn["Drawing"]["N5"], jsn["Drawing"]["MBall"]))









