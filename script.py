import requests
import xml.etree.ElementTree as ET
import json

data = requests.get('https://www.megamillions.com/cmspages/utilservice.asmx/GetLatestDrawData')
temp = ET.fromstring(data.content)
j = json.loads(temp.text)
print(j["Jackpot"]["NextPrizePool"])


